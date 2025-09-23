import pygame

# A simple zig-zag path for demo
PATH_POINTS = [
    (100, 100),
    (400, 100),
    (400, 300),
    (700, 300),
    (700, 550),
    (950, 550)
]

def draw_path(screen, path_points):
    if len(path_points) > 1:
        pygame.draw.lines(screen, (200,200,50), False, path_points, 6)
    for pt in path_points:
        pygame.draw.circle(screen, (150,200,255), pt, 12)