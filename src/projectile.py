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

        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)
        # Center the rect on the projectile's position
        self.rect = self.image.get_rect(center=start_pos)
        # Make collision rect slightly larger than visual
        self.rect.inflate_ip(2, 2)  # Add 2 pixels to each side

        # Movement variables
        self.pos = pygame.math.Vector2(start_pos)

        # Calculate lead position (simple prediction)
        enemy_pos = pygame.math.Vector2(target_enemy.get_pos())
        time_to_target = enemy_pos.distance_to(self.pos) / self.speed
        future_pos = pygame.math.Vector2(
            enemy_pos.x + target_enemy.speed * time_to_target * target_enemy.direction[0],
            enemy_pos.y + target_enemy.speed * time_to_target * target_enemy.direction[1]
        )

        self.target = future_pos
        self.direction = (self.target - self.pos).normalize()
        
    def update(self, dt):
        # Move projectile
        movement = self.direction * self.speed * dt
        self.pos += movement
        self.rect.center = self.pos
        
        # Check if projectile has gone off-screen
        if (self.pos.y < 0 or self.pos.y > SCREEN_HEIGHT or 
            self.pos.x < 0 or self.pos.x > SCREEN_WIDTH):
            self.kill()
            print("Projectile went off-screen and was removed.")

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

class Slow(Projectile):
    def __init__(self, start_pos, target_enemy):
        super().__init__(start_pos, target_enemy, 'slow')
        # Slow specific initialization if needed