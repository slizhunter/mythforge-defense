import pygame
from .utils import Colors
from .map import TOWER_RECTS

class Tower:
    COST = 20

    def __init__(self, x_pos, y_pos, tower_size, tower_range, tower_rect, fire_rate=50):
        self.x = x_pos
        self.y = y_pos
        self.size = tower_size
        self.range = tower_range
        self.fire_rate = fire_rate
        self.rect = tower_rect
        self.is_hovered = False

    def draw(self, screen):
        if self.is_hovered:
            pygame.draw.circle(screen, Colors.GRAY, (self.x, self.y), self.range, 1)
        pygame.draw.rect(screen, Colors.RED, (self.x - self.size/2, self.y - self.size/2, self.size, self.size))

    def update_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.is_hovered = True
        else:
            self.is_hovered = False

    @classmethod
    def get_cost(cls):
        return cls.COST
