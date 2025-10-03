# Game constants and helper functions
import pygame

# Colors
class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    DARK_RED = (139, 0, 0)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 100, 0)
    BLUE = (0, 0, 255)
    GRAY = (128, 128, 128)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)
    PURPLE = (160, 32, 240)
    BROWN = (139, 69, 19)
    CYAN = (0, 255, 255)

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
            'max_hp': 25,
            'value': 1,
            'color': (70, 130, 180),  # Steel blue
            'radius': 14
        },
        'fast': {
            'class': 'FastEnemy',
            'speed': 250,
            'max_hp': 15,
            'value': 2,
            'color': (255, 165, 0),  # Orange
            'radius': 10
        },
        'tank': {
            'class': 'TankEnemy',
            'speed': 70,
            'max_hp': 100,
            'value': 5,
            'color': (139, 69, 19),  # Saddle brown
            'radius': 20
        }
    }
}

WAVE_CONFIG = {
    'wave_interval': 5,  # seconds between waves
    'completion_bonus': {
        'base': 20,          # Base bonus for completing a wave
        'increment': 10,     # Additional bonus per wave
    },
    'waves': [
        {# Wave 1
            'groups': [
                {"count": 5, "type": 'basic', "interval": 1.5},
                {"count": 8, "type": 'basic', "interval": 1.2},
                {"count": 10, "type": 'basic', "interval": 1.0},
            ]
        },
        {# Wave 2
            "groups": [
                {"count": 10, "type": 'basic', "interval": 1.0},
                {"count": 12, "type": 'fast', "interval": 1.0},
                {"count": 15, "type": 'basic', "interval": 1.0},
            ]
        },
        {# Wave 3
            "groups": [
                {"count": 15, "type": 'basic', "interval": 0.8},
                {"count": 15, "type": 'fast', "interval": 0.6},
                {"count": 10, "type": 'tank', "interval": 1.2},
            ]
        },
        {# Wave 4
            "groups": [
                {"count": 15, "type": 'fast', "interval": 0.8},
                {"count": 30, "type": 'basic', "interval": 0.3},
                {"count": 10, "type": 'tank', "interval": 1.2},
                {"count": 20, "type": 'fast', "interval": 0.8}
            ]
        },
    ]
}

TOWER_CONFIG = {
    'size': 50,
    'sell_value_pct': 0.5,  # Percentage of cost returned on sell
    'type_count': 4,
    'type': {
        'basic': {
            'cost': 40,
            'range': 150,
            'fire_rate': 1.0,  # shots per second
            'projectile_speed': 300,
            'projectile_type': 'regular',
            'color': Colors.RED
        },
        'rapid': {
            'cost': 60,
            'range': 120,
            'fire_rate': 3.0,  # shots per second
            'projectile_type': 'rapid',
            'color': Colors.PURPLE
        },
        'sniper': {
            'cost': 100,
            'range': 300,
            'fire_rate': 0.5,  # shots per second
            'projectile_type': 'sniper',
            'color': Colors.GREEN
        },
        'cannon': {
            'cost': 80,
            'range': 180,
            'fire_rate': 0.8,  # shots per second
            'projectile_type': 'shell',
            'color': Colors.ORANGE
        }
    }
}

PROJECTILE_CONFIG = {
    'regular': {
        'speed': 400,
        'damage': 20,
        'color': Colors.RED,
        'size': 6,
        'splash_radius': 1  # Area damage radius
    },
    'rapid': {
        'speed': 600,
        'damage': 7,
        'color': Colors.PURPLE,
        'size': 5,
        'splash_radius': 1  # Area damage radius
    },
    'sniper': {
        'speed': 700,
        'damage': 50,
        'color': Colors.GREEN,
        'size': 7,
        'splash_radius': 1  # Area damage radius
    },
    'shell': {
        'speed': 300,
        'damage': 20,
        'color': Colors.ORANGE,
        'size': 8,
        'splash_radius': 100  # Area damage radius
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
    'wave': (SCREEN_WIDTH//2 - 50, 10),
    'money': (SCREEN_WIDTH - 300, 10),
    'lives': (SCREEN_WIDTH - 125, 10),
    'speed': (10, SCREEN_HEIGHT - 40),
    'wave_timer': (SCREEN_WIDTH//2 - 100, 50)
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