import pygame
from .utils import Colors

# A simple zig-zag path for demo
PATH_POINTS = [
    (100, 100),
    (450, 100),
    (450, 400),
    (700, 400),
    (700, 650),
    (950, 650)
]

# Tower placement spots (x, y, width, height)
TOWER_POINTS = [
    # Top section
    (250, 150, 40, 40),   # Below first horizontal path
    (350, 150, 40, 40),
    
    # Middle section near first turn
    (500, 150, 40, 40),  # Right of first vertical path
    (500, 250, 40, 40),
    
    # Middle section
    (300, 350, 40, 40),  # Left of second horizontal path
    (300, 250, 40, 40),
    
    # Bottom section
    (500, 500, 40, 40),  # Between paths
    (600, 550, 40, 40),
    (800, 550, 40, 40),  # Near end of path
    (850, 500, 40, 40)
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

