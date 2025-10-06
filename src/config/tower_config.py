from .ui_config import Colors

TOWER_CONFIG = {
    'size': 50,
    'sell_value_pct': 0.5,  # Percentage of cost returned on sell
    'targeting_modes': ['first', 'last', 'strongest', 'weakest', 'closest'],
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

ELEMENTAL_UPGRADES = {
    'pyro': {
        'color': (255, 69, 0),   # Orange Red
        'cost': 50
    },
    'glacier': {
        'color': (173, 216, 230), # Light Blue
        'cost': 50
    },
    'storm': {
        'color': Colors.YELLOW,
        'cost': 50
    }
}