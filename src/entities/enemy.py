import pygame
from ..config.enemy_config import ENEMY_CONFIG

class Enemy(pygame.sprite.Sprite):
    def __init__(self, path_points, enemy_type='basic'):
        super().__init__()
        self.path = path_points
        self.current_wp = 0   # waypoint index
        self.x, self.y = self.path[self.current_wp]

        # Get stats from config
        enemy_stats = ENEMY_CONFIG['types'][enemy_type]
        self.type = enemy_type
        for stat_name, value in enemy_stats.items():
            setattr(self, stat_name, value)
        self.hp = self.max_hp
        
        self.direction = (0, 0)
        self.reached_goal = False
        
        # Create sprite image and rect
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, dt):
        if self.reached_goal:
            return
        
        if self.current_wp + 1 >= len(self.path):
            self.reached_goal = True
            return
        
        target_x, target_y = self.path[self.current_wp + 1]
        dx = target_x - self.x
        dy = target_y - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        # Step size this frame
        step = self.speed * dt

        if dist < step:
            # Snap to waypoint, advance to next segment
            self.x, self.y = target_x, target_y
            self.current_wp += 1
        else:
            # Move toward next waypoint
            self.x += step * dx / dist
            self.y += step * dy / dist
            self.rect.center = (self.x, self.y)
        
        self.direction = (dx / dist, dy / dist) if dist != 0 else (0, 0)
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

        # Draw health bar
        health_pct = self.hp / self.max_hp
        bar_width = self.radius * 2
        bar_height = 4
        bar_pos = (int(self.x - self.radius), int(self.y - self.radius - 8))
        
        # Background (red)
        pygame.draw.rect(surface, (255,0,0), 
            (bar_pos[0], bar_pos[1], bar_width, bar_height))
        # Foreground (green)
        pygame.draw.rect(surface, (0,255,0), 
            (bar_pos[0], bar_pos[1], int(bar_width * health_pct), bar_height))

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def is_dead(self):
        return self.hp <= 0
    
    def get_value(self):
        return self.value
    
    def get_pos(self):
        return (self.x, self.y)
    
    def get_size(self):
        return self.radius
