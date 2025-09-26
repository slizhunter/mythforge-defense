# Game constants and helper functions
import pygame

# Colors
class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (128, 128, 128)

# Game settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

GAME_CONFIG = {
    'starting_lives': 20,
    'starting_money': 100,
    'initial_speed': 1.0,
}

ENEMY_CONFIG = {
    'spawn_interval': 2.0,  # seconds between spawns
    'base_speed': 100,      # pixels per second
    'base_hp': 20,
    'base_value': 5,         # money given when killed
    'types': {
        'basic': {
            'class': 'BasicEnemy',
            'speed': 100,
            'hp': 20,
            'value': 5,
            'color': (70, 130, 180),  # Steel blue
            'radius': 14
        },
        'fast': {
            'class': 'FastEnemy',
            'speed': 200,
            'hp': 15,
            'value': 7,
            'color': (255, 165, 0),  # Orange
            'radius': 10
        },
        'tank': {
            'class': 'TankEnemy',
            'speed': 70,
            'hp': 60,
            'value': 15,
            'color': (139, 69, 19),  # Saddle brown
            'radius': 20
        }
    }
}

WAVE_CONFIG = {
    'wave_interval': 5,  # seconds between waves
    'waves': [
        {# Wave 1
            'enemies': [
                {"count": 5, "type": 'basic', "interval": 1.5},
                {"count": 8, "type": 'fast', "interval": 1.2},
                {"count": 10, "type": 'tank', "interval": 1.0},
            ]
        },
        {# Wave 2
            "enemies": [
                {"count": 10, "type": 'basic', "interval": 1.0},
                {"count": 12, "type": 'fast', "interval": 0.8},
                {"count": 5, "type": 'tank', "interval": 1.5},
            ]
        },
        {# Wave 3
            "enemies": [
                {"count": 15, "type": 'basic', "interval": 0.8},
                {"count": 15, "type": 'fast', "interval": 0.6},
                {"count": 10, "type": 'tank', "interval": 1.2},
            ]
        }
    ]
}

TOWER_CONFIG = {
    'size': 40,
    'type_count': 3,
    'basic': {
        'cost': 20,
        'range': 150,
        'fire_rate': 1.0,  # shots per second
        'damage': 10,
        'projectile_speed': 300,
        'color': Colors.RED
    },
    'rapid': {
        'cost': 30,
        'range': 120,
        'fire_rate': 3.0,  # shots per second
        'damage': 5,
        'projectile_speed': 400,
        'color': Colors.BLUE
    },
    'sniper': {
        'cost': 50,
        'range': 300,
        'fire_rate': 0.5,  # shots per second
        'damage': 40,
        'projectile_speed': 500,
        'color': Colors.GREEN
    }
}

UI_CONFIG = {
    'bg_color': (50, 50, 50),
    'text_color': (255, 255, 255),
    'font_size_large': 36,
    'font_size_medium': 24,
    'font_size_small': 18
}

UI_POSITIONS = {
    'title': (10, 10),
    'wave': (700, 10),
    'money': (500, 10),
    'lives': (900, 10),
    'speed': (10, 740)
}

def distance(pos1, pos2):
    """Calculate distance between two points."""
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

def load_image(path, scale=None):
    """Load and optionally scale an image."""
    try:
        image = pygame.image.load(path)
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error:
        # Return a placeholder colored rectangle if image not found
        surf = pygame.Surface((32, 32))
        surf.fill((255, 0, 255))  # Magenta placeholder
        return surf