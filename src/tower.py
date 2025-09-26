import pygame
from .utils import Colors, TOWER_CONFIG
from .map import TOWER_RECTS
from .projectile import Projectile

class Tower:
    def __init__(self, x_pos, y_pos, tower_rect, tower_type='basic'):
        # Tower position
        self.x = x_pos
        self.y = y_pos
        self.rect = tower_rect

        # Tower stats
        tower_stats = TOWER_CONFIG[tower_type]
        self.size = TOWER_CONFIG['size']
        self.range = tower_stats['range']
        self.cost = tower_stats['cost']
        self.fire_rate = tower_stats['fire_rate']
        self.damage = tower_stats['damage']
        self.projectile_speed = tower_stats['projectile_speed']
        self.color = tower_stats['color']

        # Combat variables
        self.fire_timer = 0 # Time since last shot
        self.target = None

        # Tower management
        self.game = None  # Will be set when tower is added to the game
        self.is_hovered = False
    
    def update(self, dt):
        # First check if target is still valid
        if self.target and (
            self.target.is_dead() or 
            not self.detect_enemy(self.target.get_pos(), self.target.get_size()) or
            self.target not in self.game.enemies
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
            pygame.draw.circle(screen, Colors.GRAY, (self.x, self.y), self.range, 1)
        pygame.draw.rect(screen, self.color, (self.x - self.size/2, self.y - self.size/2, self.size, self.size))

    def update_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.is_hovered = True
        else:
            self.is_hovered = False

    def detect_enemy(self, enemy_pos, enemy_radius):
        center1 = pygame.math.Vector2((self.x, self.y))
        center2 = pygame.math.Vector2(enemy_pos)
        distance = center1.distance_to(center2)
        return distance < (self.range + enemy_radius)
    
    def set_target(self, enemy):
        self.target = enemy

    def get_target(self):
        return self.target
    
    def fire_at(self, enemy):
        new_projectile = Projectile(
            start_pos=(self.x, self.y),
            target_enemy=enemy,
            speed=self.projectile_speed,
            damage=self.damage
        )
        self.game.projectiles.add(new_projectile)

    def get_cost(self):
        return self.cost

class BasicTower(Tower):
    def __init__(self, x_pos, y_pos, tower_rect):
        super().__init__(x_pos, y_pos, tower_rect, 'basic')

class RapidTower(Tower):
    def __init__(self, x_pos, y_pos, tower_rect):
        super().__init__(x_pos, y_pos, tower_rect, 'rapid')

class SniperTower(Tower):
    def __init__(self, x_pos, y_pos, tower_rect):
        super().__init__(x_pos, y_pos, tower_rect, 'sniper')