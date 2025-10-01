import pygame
from .utils import Colors, TOWER_CONFIG

# A simple zig-zag path for demo
PATH_POINTS = [
    (100, 100),
    (450, 100),
    (450, 400),
    (700, 400),
    (700, 650),
    (950, 650)
]

size = TOWER_CONFIG['size']

# Tower placement spots (x, y, width, height)
TOWER_POINTS = [
    # Below path
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
    
    #Above path
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

TOWER_RECTS = [pygame.Rect(spot) for spot in TOWER_POINTS]

def draw_path(screen, path_points):
    # Draw main path (lighter center)
    if len(path_points) > 1:
        pygame.draw.lines(screen, (140, 140, 35), False, path_points, 41)
    
    # Draw connection points between path segments
    for pt in path_points[1:-1]:  # Skip first and last points
        # Darker outer circle
        pygame.draw.circle(screen, (140, 140, 35), pt, 20)
        # Lighter inner circle
        pygame.draw.circle(screen, (140, 140, 35), pt, 20)

def draw_spawn_point(screen, path_points):
    if path_points:
        spawn_pos = path_points[0]
        pygame.draw.circle(screen, Colors.GREEN, spawn_pos, 40)
        pygame.draw.circle(screen, Colors.DARK_GREEN, spawn_pos, 40, 2)

def draw_end_point(screen, path_points):
    if path_points:
        end_pos = path_points[-1]
        pygame.draw.circle(screen, Colors.RED, end_pos, 40)
        pygame.draw.circle(screen, Colors.DARK_RED, end_pos, 40, 2)

def draw_tower_spots(screen, tower_points):
    for spot in tower_points:
        pygame.draw.rect(screen, (200,200,50), spot, 1)

