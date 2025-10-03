from ..config.tower_config import TOWER_CONFIG

size = TOWER_CONFIG['size']

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
