import pygame
from ..config.ui_config import Colors
from ..maps.level_1 import LEVEL_1
from ..maps.level_2 import LEVEL_2

class Map:
    def __init__(self, path_points, tower_points, name="Unnamed Map"):
        self.name = name
        self.path_points = path_points
        self.tower_points = tower_points
        self.tower_rects = [pygame.Rect(spot) for spot in tower_points]

    def draw_path(self, screen):
        if len(self.path_points) > 1:
            pygame.draw.lines(screen, (140, 140, 35), False, self.path_points, 41)

        # Draw connection points between path segments
        for pt in self.path_points[1:-1]:  # Skip first and last points
            pygame.draw.circle(screen, (140, 140, 35), pt, 20)

    def draw_spawn_point(self, screen):
        if self.path_points:
            spawn_pos = self.path_points[0]
            pygame.draw.circle(screen, Colors.GREEN, spawn_pos, 40)
            pygame.draw.circle(screen, Colors.DARK_GREEN, spawn_pos, 40, 2)

    def draw_end_point(self, screen):
        if self.path_points:
            end_pos = self.path_points[-1]
            pygame.draw.circle(screen, Colors.RED, end_pos, 40)
            pygame.draw.circle(screen, Colors.DARK_RED, end_pos, 40, 2)

    def draw_tower_spots(self, screen):
        for spot in self.tower_points:
            pygame.draw.rect(screen, (200,200,50), spot, 1)

    def get_path(self):
        return self.path_points

    def get_tower_points(self):
        return self.tower_points

    def get_tower_rects(self):
        return self.tower_rects
    
# Create map instances
MAPS = {
    "level_1": Map(LEVEL_1['path_points'], LEVEL_1['tower_points'], LEVEL_1['name']),
    "level_2": Map(LEVEL_2['path_points'], LEVEL_2['tower_points'], LEVEL_2['name']),
    # Add more maps as needed
}