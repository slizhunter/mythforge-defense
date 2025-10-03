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