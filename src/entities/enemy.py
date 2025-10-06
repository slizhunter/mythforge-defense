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
        self.effects = []  # Active status effects (e.g., slowed, burning)
        self.burn_damage = 0  # Damage per second from burn effect
        self.burn_timer = 0  # Timer to track burn damage application
        
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
        
        self._update_effects(dt)
        self._process_effects(dt)

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
        
    def apply_effect(self, effect):
        """Apply a status effect to the enemy"""
        # Avoid stacking same effect type
        for existing_effect in self.effects:
            if existing_effect['type'] == effect['type']:
                return  # Effect already applied
        self.effects.append(effect)
        if effect['type'] == 'slow':
            self.speed *= (1 - effect['slow_pct'])  # Example: slow down by 50%
        if effect['type'] == 'burn':
            self.burn_damage = effect['damage_per_second']


    def _update_effects(self, dt):
        """Update status effects over time"""
        for effect in self.effects:
            effect['duration'] -= dt
            if effect['duration'] <= 0:
                if effect['type'] == 'slow':
                    self.speed /= (1 - effect['slow_pct'])  # Revert slow effect
                if effect['type'] == 'burn':
                    self.burn_damage = 0
                self.effects.remove(effect)

    def _process_effects(self, dt):
        """Process ongoing effects like burn damage"""
        for effect in self.effects:
            if effect['type'] == 'burn':
                self.burn_timer += dt
                if self.burn_timer >= 1.0:  # Apply damage every second
                    self.take_damage(self.burn_damage)
                    self.burn_timer = 0  # Reset timer

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
