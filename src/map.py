import pygame
from .config.tower_config import TOWER_CONFIG
from .config.ui_config import Colors

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

size = TOWER_CONFIG['size']

LEVEL_1 = {
    'name': "The First Trial",
    'path_points': [
        (100, 100),
        (450, 100),
        (450, 400),
        (700, 400),
        (700, 650),
        (950, 650)
    ],
    'tower_points': [
        (150, 150, size, size),
        (200, 150, size, size),
        (250, 150, size, size),   
        (300, 150, size, size),
        (350, 150, size, size),

        (350, 200, size, size),  
        (350, 250, size, size),
        (350, 300, size, size),
        (350, 350, size, size),
        (350, 400, size, size),
        (350, 450, size, size),

        (400, 450, size, size),
        (450, 450, size, size),
        (500, 450, size, size),
        (550, 450, size, size),
        (600, 450, size, size),

        (600, 500, size, size),
        (600, 550, size, size),
        (600, 600, size, size),
        (600, 650, size, size),
        
        (500, 100, size, size),
        (500, 150, size, size),
        (500, 200, size, size),
        (500, 250, size, size),
        (500, 300, size, size),

        (550, 300, size, size),
        (600, 300, size, size),
        (650, 300, size, size),
        (700, 300, size, size),
        (750, 300, size, size),

        (750, 350, size, size),
        (750, 400, size, size),
        (750, 450, size, size),
        (750, 500, size, size),
        (750, 550, size, size),

        (800, 550, size, size),
        (850, 550, size, size),
    ]
}

LEVEL_2 = {
    'name': "Valley of Death",
    'path_points': [
        (100, 650),  # Start bottom left
        (300, 650),
        (300, 100),  # Up
        (600, 100),  # Right
        (600, 650),  # Down
        (900, 650),  # End bottom right
    ],
    'tower_points': [
        (200, 550, size, size),
        (200, 500, size, size),
        (200, 450, size, size),
        (200, 400, size, size),
        (200, 350, size, size),
        (200, 300, size, size),
        (200, 250, size, size),
        (200, 200, size, size),
        (200, 150, size, size),
        (200, 100, size, size),

        (350, 550, size, size),
        (350, 500, size, size),
        (350, 450, size, size),
        (350, 400, size, size),
        (350, 350, size, size),
        (350, 300, size, size),
        (350, 250, size, size),
        (350, 200, size, size),
        (350, 150, size, size),

        (350, 150, size, size),
        (400, 150, size, size),
        (450, 150, size, size),
        (500, 150, size, size),

        (500, 200, size, size),
        (500, 250, size, size),
        (500, 300, size, size),
        (500, 350, size, size),
        (500, 400, size, size),
        (500, 450, size, size),
        (500, 500, size, size),
        (500, 550, size, size),

        (650, 100, size, size),
        (650, 150, size, size),
        (650, 200, size, size),
        (650, 250, size, size),
        (650, 300, size, size),
        (650, 350, size, size),
        (650, 400, size, size),
        (650, 450, size, size),
        (650, 500, size, size),
        (650, 550, size, size),

        (700, 550, size, size),
        (750, 550, size, size),
        (800, 550, size, size),
    ]
}

# Create map instances
MAPS = {
    "level_1": Map(LEVEL_1['path_points'], LEVEL_1['tower_points'], LEVEL_1['name']),
    "level_2": Map(LEVEL_2['path_points'], LEVEL_2['tower_points'], LEVEL_2['name']),
    # Add more maps as needed
}