import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, path_points, speed=120, max_hp=20, value = 5):
        super().__init__()
        self.path = path_points
        self.current_wp = 0   # waypoint index
        self.x, self.y = self.path[self.current_wp]
        self.speed = speed  # pixels per second
        self.direction = (0, 0)  # Will be set in update
        self.max_hp = max_hp
        self.hp = max_hp
        self.value = value  # money given when killed
        self.reached_goal = False

        # simple visuals
        self.color = (230, 70, 70)
        self.radius = 14
        
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