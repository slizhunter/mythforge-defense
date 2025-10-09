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
                {"count": 20, "type": 'fast', "interval": 0.8},
                {"count": 15, "type": 'flying', "interval": 1.0}
            ]
        },
    ]
}