import pygame
from .utils import Colors, UI_CONFIG, UI_POSITIONS, TOWER_CONFIG

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        self.shop_towers = {}  # Dict with (name, rect) for tower shop options

        # Initialize fonts
        pygame.font.init()
        self.large_font = pygame.font.Font(None, UI_CONFIG["font_size_large"])
        self.medium_font = pygame.font.SysFont('Arial', UI_CONFIG["font_size_medium"])
        self.small_font = pygame.font.SysFont('Arial', UI_CONFIG["font_size_small"])
        
        # Colors
        self.bg_color = UI_CONFIG["bg_color"]
        self.text_color = UI_CONFIG["text_color"]
    
    def draw(self, game, wave_manager):
        # Draw game world elements
        self._draw_game_world()
        
        # Draw UI stats
        self._draw_ui_stats(game)
        
        # Draw wave info
        self._draw_wave_info(wave_manager)

        # Draw tower shop
        self._draw_tower_shop()

    def _draw_game_world(self):
        # --- draw game world ---
        title_txt = self.large_font.render("Myth-Forge Defense", True, self.text_color)
        self.screen.blit(title_txt, UI_POSITIONS["title"])

    def _draw_ui_stats(self, game):
        # --- UI text ---
        money_txt = self.large_font.render(f"Money: {game.money}", True, (255,255,255))
        self.screen.blit(money_txt, UI_POSITIONS["money"])
        lives_txt = self.large_font.render(f"Lives: {game.lives}", True, (255,255,255))
        self.screen.blit(lives_txt, UI_POSITIONS["lives"])
        speed_txt = self.large_font.render(f"Speed: {game.speed_factor}", True, (255,255,255))
        self.screen.blit(speed_txt, UI_POSITIONS["speed"])

    def _draw_wave_info(self, wave_manager):
        # --- wave info ---
        wave_info = wave_manager.get_wave_info()
        wave_txt = self.large_font.render(f"Wave: {wave_info['current_wave']}/{wave_info['total_waves']}", True, (255,255,255))
        self.screen.blit(wave_txt, UI_POSITIONS["wave"])
        
        if wave_info['break_timer'] > 0:
            break_txt = self.large_font.render(f"Next wave in: {wave_info['break_timer']:.1f}", True, (255,255,255))
            self.screen.blit(break_txt, (self.screen_width//2 - 100, 50))

    def _draw_tower_shop(self):
        # --- draw tower selection ---
        size = TOWER_CONFIG['size']
        tower_config = TOWER_CONFIG['type']
        # Draw tower shop area rectangle
        shop_rect = pygame.Rect(10, 200, size * 2, size * TOWER_CONFIG['type_count'] * 2.5)  # x, y, width, height
        pygame.draw.rect(self.screen, Colors.BLACK, shop_rect, 2)  # 2 is border thickness
        # Draw tower options
        next_tower = self.__draw_tower_option("Basic", shop_rect, tower_config['basic'], shop_rect.top)
        next_tower = self.__draw_tower_option("Rapid", shop_rect, tower_config['rapid'], next_tower)
        next_tower = self.__draw_tower_option("Sniper", shop_rect, tower_config['sniper'], next_tower)
        next_tower = self.__draw_tower_option("Cannon", shop_rect, tower_config['cannon'], next_tower)

    def __draw_tower_option(self, name, shop_rect, tower_config, top_y):
        size = TOWER_CONFIG['size']
        name_txt = self.medium_font.render(name, True, Colors.WHITE)
        name_rect = name_txt.get_rect(center=(shop_rect.centerx, top_y + 20))
        self.screen.blit(name_txt, name_rect)
        tower_rect = pygame.Rect(30, name_rect.bottom + 10, size, size)
        self.shop_towers[name] = tower_rect
        pygame.draw.rect(self.screen, tower_config['color'], tower_rect)
        cost_txt = self.small_font.render(f"${tower_config['cost']}", True, Colors.WHITE)
        cost_rect = cost_txt.get_rect(center=(tower_rect.centerx, tower_rect.top + size//2))
        self.screen.blit(cost_txt, cost_rect)
        return tower_rect.bottom + 10  # Return bottom y for next option

    def draw_paused(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        text = self.large_font.render("PAUSED - Press ESC to resume", True, self.text_color)
        text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(text, text_rect)

    def draw_over(self):
        text = self.large_font.render("Game Over - Press R to restart", True, self.text_color)
        text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(text, text_rect)

    def draw_victory(self):
        text = self.large_font.render("You Won! - Press R to restart", True, self.text_color)
        text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(text, text_rect)

    def get_shop_towers(self):
        """Return tower shop rectangles for click detection"""
        return self.shop_towers