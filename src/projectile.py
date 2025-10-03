import pygame
from .utils import SCREEN_HEIGHT, SCREEN_WIDTH, PROJECTILE_CONFIG

class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_enemy, projectile_type='regular'):
        super().__init__()
        # Get stats from config
        projectile_stats = PROJECTILE_CONFIG[projectile_type]
        self.speed = projectile_stats['speed']
        self.damage = projectile_stats['damage']
        self.color = projectile_stats['color']
        self.size = projectile_stats['size']
        self.splash_radius = projectile_stats['splash_radius'] if 'splash_radius' in projectile_stats else 1

        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)
        # Center the rect on the projectile's position
        self.rect = self.image.get_rect(center=start_pos)
        # Make collision rect slightly larger than visual
        self.rect.inflate_ip(2, 2)  # Add 2 pixels to each side

        # Movement variables
        self.pos = pygame.math.Vector2(start_pos)

        # Targeting (how far to shoot ahead of moving target)
        self._calculate_lead(target_enemy)
        
    def update(self, dt):
        # Move projectile
        movement = self.direction * self.speed * dt
        self.pos += movement
        self.rect.center = self.pos
        
        # Check if projectile has gone off-screen
        if (self.pos.y < 0 or self.pos.y > SCREEN_HEIGHT or 
            self.pos.x < 0 or self.pos.x > SCREEN_WIDTH):
            self.kill()
            #print("Projectile went off-screen and was removed.")

    def _calculate_lead(self, target_enemy):
        # Calculate lead position (simple prediction)
        enemy_pos = pygame.math.Vector2(target_enemy.get_pos())
        time_to_target = enemy_pos.distance_to(self.pos) / self.speed
        future_pos = pygame.math.Vector2(
            enemy_pos.x + target_enemy.speed * time_to_target * target_enemy.direction[0],
            enemy_pos.y + target_enemy.speed * time_to_target * target_enemy.direction[1]
        )

        self.target = future_pos
        self.direction = (self.target - self.pos).normalize()
    
    def get_splash_damage(self, distance_to_impact):
        """Calculate damage based on distance from impact
        Closer enemies take more damage"""
        if distance_to_impact > self.splash_radius:
            return 0
        
        # Linear falloff: 100% damage at center, 50% at edge
        damage_multiplier = 1 - (distance_to_impact / self.splash_radius) * 0.5
        return int(self.damage * damage_multiplier)

class Regular(Projectile):
    def __init__(self, start_pos, target_enemy):
        super().__init__(start_pos, target_enemy, 'regular')
        # Regular target specific initialization if needed

class Rapid(Projectile):
    def __init__(self, start_pos, target_enemy):
        super().__init__(start_pos, target_enemy, 'rapid')
        # Rapid specific initialization if needed

class Sniper(Projectile):
    def __init__(self, start_pos, target_enemy):
        super().__init__(start_pos, target_enemy, 'sniper')
        # Sniper specific initialization if needed

class Shell(Projectile):
    def __init__(self, start_pos, target_enemy):
        super().__init__(start_pos, target_enemy, 'shell')
        # Shell specific initialization if needed