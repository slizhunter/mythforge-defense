import pygame
import math
from .enemy import Enemy

class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_enemy, speed=400, damage=10):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill((255, 255, 0))  # Yellow projectile
        self.rect = self.image.get_rect(center=start_pos)
        
        # Movement variables
        self.pos = pygame.math.Vector2(start_pos)

        # Calculate lead position (simple prediction)
        enemy_pos = pygame.math.Vector2(target_enemy.get_pos())
        time_to_target = enemy_pos.distance_to(self.pos) / speed
        future_pos = pygame.math.Vector2(
            enemy_pos.x + target_enemy.speed * time_to_target * target_enemy.direction[0],
            enemy_pos.y + target_enemy.speed * time_to_target * target_enemy.direction[1]
        )
        
        self.target = future_pos
        self.direction = (self.target - self.pos).normalize()
        self.speed = speed
        
        # Combat stats
        self.damage = damage
        
    def update(self, dt):
        # Move projectile
        movement = self.direction * self.speed * dt
        self.pos += movement
        self.rect.center = self.pos
        
        # Check if projectile has reached or passed target
        if (self.target - self.pos).length() <= self.speed * dt:
            self.kill()