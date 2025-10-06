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

ELEMENTAL_EFFECTS = {
    'pyro': {
        'type': 'burn',
        'damage_per_second': 5,  # Damage per second
        'duration': 3,          # Duration in seconds
        'color': (255, 69, 0)   # Orange Red
    },
    'glacier': {
        'type': 'slow',
        'slow_pct': 0.3,        # Slow enemy speed by 30%
        'duration': 2,          # Duration in seconds
        'color': (173, 216, 230) # Light Blue
    },
    'storm': {
        'chain_range': 80,      # Range to chain to next enemy
        'max_jumps': 3,         # Max number of jumps
        'damage_reduction': 0.2, # 20% damage reduction per jump
        'color': Colors.YELLOW
    }
}