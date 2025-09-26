import pygame
from .utils import Colors
from .map import TOWER_RECTS
from .projectile import Projectile

class Tower:
    COST = 20

    def __init__(self, x_pos, y_pos, tower_size, tower_range, tower_rect, fire_rate=2):
        self.x = x_pos
        self.y = y_pos
        self.size = tower_size
        self.range = tower_range
        self.fire_rate = fire_rate
        self.fire_timer = 0 # Time since last shot
        self.game = None  # Will be set when tower is added to the game
        self.rect = tower_rect
        self.target = None
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

    @classmethod
    def get_cost(cls):
        return cls.COST
