from .ui_config import Colors

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