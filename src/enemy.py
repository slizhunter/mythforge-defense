import pygame

class Enemy:
    def __init__(self, path_points, speed=120, max_hp=20):
        self.path = path_points
        self.current_wp = 0   # waypoint index
        self.x, self.y = self.path[self.current_wp]
        self.speed = speed  # pixels per second
        self.max_hp = max_hp
        self.hp = max_hp
        self.reached_goal = False

        # simple visuals
        self.color = (230, 70, 70)
        self.radius = 14

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
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def is_dead(self):
        return self.hp <= 0