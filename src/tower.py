import pygame
from .utils import COLORS

class Tower:
    COST = 20

    def __init__(self, x_pos, y_pos, tower_size, fire_rate=50):
        self.x = x_pos
        self.y = y_pos
        self.size = tower_size
        self.fire_rate = fire_rate

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x - self.size/2, self.y - self.size/2, self.size, self.size))

    @classmethod
    def get_cost(cls):
        return cls.COST
