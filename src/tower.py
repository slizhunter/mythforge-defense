import pygame
from .utils import Colors, TOWER_CONFIG
from .map import TOWER_RECTS
from .projectile import Projectile

class Tower:
    def __init__(self, x_pos, y_pos, tower_rect):
        # Tower position
        self.x = x_pos
        self.y = y_pos
        self.rect = tower_rect

        # Tower stats
        self.size = TOWER_CONFIG['size']
        self.range = TOWER_CONFIG['basic']['range']
        self.cost = TOWER_CONFIG['basic']['cost']
        self.fire_rate = TOWER_CONFIG['basic']['fire_rate']  # shots per second
        self.damage = TOWER_CONFIG['basic']['damage']
        self.color = Colors.RED

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
        pygame.draw.rect(screen, Colors.RED, (self.x - self.size/2, self.y - self.size/2, self.size, self.size))

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
            target_enemy=enemy
        )
        self.game.projectiles.add(new_projectile)

    def get_cost(self):
        return self.cost

class BasicTower(Tower):
    def __init__(self, x_pos, y_pos, tower_rect):
        super().__init__(x_pos, y_pos, tower_rect)
        self.range = TOWER_CONFIG['basic']['range']
        self.cost = TOWER_CONFIG['basic']['cost']
        self.fire_rate = TOWER_CONFIG['basic']['fire_rate']
        self.damage = TOWER_CONFIG['basic']['damage']
        self.color = TOWER_CONFIG['basic']['color']

class RapidTower(Tower):
    def __init__(self, x_pos, y_pos, tower_rect):
        super().__init__(x_pos, y_pos, tower_rect)
        self.range = TOWER_CONFIG['rapid']['range']
        self.cost = TOWER_CONFIG['rapid']['cost']
        self.fire_rate = TOWER_CONFIG['rapid']['fire_rate']
        self.damage = TOWER_CONFIG['rapid']['damage']
        self.color = TOWER_CONFIG['rapid']['color']

class SniperTower(Tower):
    def __init__(self, x_pos, y_pos, tower_rect):
        super().__init__(x_pos, y_pos, tower_rect)
        self.range = TOWER_CONFIG['sniper']['range']
        self.cost = TOWER_CONFIG['sniper']['cost']
        self.fire_rate = TOWER_CONFIG['sniper']['fire_rate']
        self.damage = TOWER_CONFIG['sniper']['damage']
        self.color = TOWER_CONFIG['sniper']['color']