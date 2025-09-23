import pygame

# A simple zig-zag path for demo
PATH_POINTS = [
    (100, 100),
    (450, 100),
    (450, 400),
    (700, 400),
    (700, 650),
    (950, 650)
]

TOWER_POINTS = [
    (200, 125, 30, 30),
    (650, 350, 30, 30)
]

TOWER_RECTS = [pygame.Rect(spot) for spot in TOWER_POINTS]

def draw_path(screen, path_points):
    if len(path_points) > 1:
        pygame.draw.lines(screen, (200,200,50), False, path_points, 6)
    for pt in path_points:
        pygame.draw.circle(screen, (150,200,255), pt, 12)

def draw_tower_spots(screen, tower_points):
    for spot in tower_points:
        pygame.draw.rect(screen, (200,200,50), spot, 1)