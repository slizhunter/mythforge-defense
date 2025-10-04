import pygame
from ..config.tower_config import TOWER_CONFIG
from ..config.ui_config import UI_CONFIG, UI_POSITIONS, Colors
from .projectile import Projectile

class Tower:
    def __init__(self, x_pos, y_pos, tower_rect, tower_type='basic'):
        # Tower position
        self.x = x_pos
        self.y = y_pos
        self.rect = tower_rect

        # Tower stats
        tower_stats = TOWER_CONFIG['type'][tower_type]
        self.size = TOWER_CONFIG['size']
        self.sell_value_pct = TOWER_CONFIG['sell_value_pct']
        self.targeting_mode = 'first'  # Could be 'first', 'last', 'strongest', 'weakest', 'closest'
        self.type = tower_type
        for stat_name, value in tower_stats.items():
            setattr(self, stat_name, value)

        # Combat variables
        self.fire_timer = 0 # Time since last shot
        self.target = None

        # Tower management
        self.game = None  # Will be set when tower is added to the game
        self.is_hovered = False

        # Initialize fonts
        pygame.font.init()
        self.small_font = pygame.font.SysFont('Arial', UI_CONFIG["font_size_small"])
    
    def update(self, dt):
        # First check if target is still valid
        if self.target and (            # Check if target exists
            self.target.is_dead() or    # Check if target is dead
            not self.detect_enemy(self.target.get_pos(), self.target.get_size()) or # Check if target is out of range
            self.target not in self.game.enemies # Check if target is still in game
        ):
            self.target = None
            return

        self.fire_timer += dt
        
        # Check if we can fire
        if self.target and self.fire_timer >= 1.0 / self.fire_rate:
            self.fire_at(self.target)
            self.fire_timer = 0

    def draw(self, screen):
        if self.is_hovered:
            # Draw range circle
            pygame.draw.circle(screen, Colors.GRAY, (self.x, self.y), self.range, 1)

            # Show targeting mode
            targeting_txt = self.small_font.render(f"{self.targeting_mode}", True, Colors.WHITE)
            text_bg = pygame.Rect(
                self.x - targeting_txt.get_width()//2 - 5,
                self.y + self.size//2 + 5,
                targeting_txt.get_width() + 10,
                targeting_txt.get_height()
            )
            pygame.draw.rect(screen, Colors.BLACK, text_bg)
            screen.blit(targeting_txt, (self.x - targeting_txt.get_width()//2, self.y + self.size//2 + 5))

        # Draw tower (simple square for now)
        pygame.draw.rect(screen, self.color, (self.x - self.size/2, self.y - self.size/2, self.size, self.size))

    def update_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.is_hovered = True
        else:
            self.is_hovered = False

    def detect_enemy(self, enemy_pos, enemy_radius):
        center1 = pygame.math.Vector2((self.x, self.y)) # Tower center
        center2 = pygame.math.Vector2(enemy_pos)        # Enemy center
        distance = center1.distance_to(center2)         # Distance between centers
        return distance < (self.range + enemy_radius)   # Check if within range
    
    def fire_at(self, enemy):
        """Create appropriate projectile type based on tower's projectile_type"""
        new_projectile = Projectile(
            start_pos=(self.x, self.y),
            target_enemy=enemy,
            projectile_type=self.projectile_type
        )
        self.game.projectiles.add(new_projectile)

    def set_targeting_mode(self, mode):
        if mode in ['first', 'last', 'strongest', 'weakest', 'closest']:
            self.targeting_mode = mode

    def set_target(self, enemy):
        self.target = enemy

    def get_target(self):
        return self.target

    def get_cost(self):
        return self.cost
    
    def get_sell_value(self):
        return int(self.cost * self.sell_value_pct)
    
    def sell(self):
        self.target = None
        self.game = None  # Remove reference to game