import pygame
import math

class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos, speed=200, damage=10):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill((255, 255, 0))  # Yellow projectile
        self.rect = self.image.get_rect(center=start_pos)
        
        # Movement variables
        self.pos = pygame.math.Vector2(start_pos)
        self.target = pygame.math.Vector2(target_pos)
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