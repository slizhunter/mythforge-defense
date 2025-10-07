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
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 980
FPS = 60

# Game world dimensions
GAME_WIDTH = 1024
GAME_HEIGHT = 768

UI_CONFIG = {
    'bg_color': (50, 50, 50),
    'text_color': (255, 255, 255),
    'font_size_large': 46,
    'font_size_medium': 24,
    'font_size_small': 18
}

UI_POSITIONS = {
    'title': (10, 10),
    'wave': (SCREEN_WIDTH//2 - 50, 10),
    'money': (SCREEN_WIDTH - 300, 10),
    'lives': (SCREEN_WIDTH - 125, 10),
    'speed': (10, SCREEN_HEIGHT - 40),
    'wave_timer': (SCREEN_WIDTH//2 - 100, 50),
    'tower_shop': (10, 100)  # Starting position for tower shop
}