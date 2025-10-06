import pygame
from ..config.ui_config import Colors, UI_CONFIG, UI_POSITIONS
from ..config.tower_config import ELEMENTAL_UPGRADES, TOWER_CONFIG

class UIManager:
    def __init__(self, game, screen, wave_manager):
        self.game = game
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.wave_manager = wave_manager
        
        self.shop_towers = {}  # Dict with (name, rect) for tower shop options

        # Initialize fonts
        pygame.font.init()
        self.large_font = pygame.font.Font(None, UI_CONFIG["font_size_large"])
        self.medium_font = pygame.font.SysFont('Arial', UI_CONFIG["font_size_medium"])
        self.small_font = pygame.font.SysFont('Arial', UI_CONFIG["font_size_small"])
        
        # Colors
        self.bg_color = UI_CONFIG["bg_color"]
        self.text_color = UI_CONFIG["text_color"]
    
    def draw(self):
        # Draw game world elements
        self._draw_game_world()
        
        # Draw UI stats
        self._draw_ui_stats()
        
        # Draw wave info
        self._draw_wave_info()

        # Draw tower shop
        self._draw_tower_shop()

    def _draw_game_world(self):
        # --- draw game world ---
        title_txt = self.large_font.render("Myth-Forge Defense", True, self.text_color)
        self.screen.blit(title_txt, UI_POSITIONS["title"])

    def _draw_ui_stats(self):
        # --- UI text ---
        money_txt = self.large_font.render(f"Money: {self.game.money}", True, (255,255,255))
        self.screen.blit(money_txt, UI_POSITIONS["money"])
        lives_txt = self.large_font.render(f"Lives: {self.game.lives}", True, (255,255,255))
        self.screen.blit(lives_txt, UI_POSITIONS["lives"])
        speed_txt = self.large_font.render(f"Speed: {self.game.speed_factor}", True, (255,255,255))
        self.screen.blit(speed_txt, UI_POSITIONS["speed"])

    def _draw_wave_info(self):
        # --- wave info ---
        wave_info = self.wave_manager.get_wave_info()
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
        # Calculate space needed for each tower option
        PADDING = 10
        NAME_HEIGHT = self.medium_font.get_height()
        TOWER_HEIGHT = size
        
        # Space per tower = padding + name + padding + tower + padding + cost + padding
        SPACE_PER_TOWER = PADDING + NAME_HEIGHT + PADDING + TOWER_HEIGHT + PADDING
        
        # Total height = space per tower * number of towers
        total_height = SPACE_PER_TOWER * len(tower_config)
        
        # Draw tower shop area rectangle
        shop_rect = pygame.Rect(
            UI_POSITIONS['tower_shop'][0],           # x position
            UI_POSITIONS['tower_shop'][1],           # y position
            size * 2,                                # width
            total_height                             # calculated height
        )
        pygame.draw.rect(self.screen, Colors.BLACK, shop_rect, 2)  # 2 is border thickness
        # Draw tower options
        next_y = shop_rect.top
        for tower_name, stats in tower_config.items():
            next_y = self.__draw_tower_option(
                name=tower_name.capitalize(),
                shop_rect=shop_rect,
                tower_config=stats,
                top_y=next_y
            )
        # Draw upgrade shop
        self._draw_upgrade_shop()
        
    def _draw_upgrade_shop(self):
        size = TOWER_CONFIG['size']
        upgrade_config = ELEMENTAL_UPGRADES

        PADDING = 10
        NAME_HEIGHT = self.medium_font.get_height()
        UPGRADE_HEIGHT = size

        # Space per tower = padding + name + padding + tower + padding + cost + padding
        SPACE_PER_UPGRADE = PADDING + NAME_HEIGHT + PADDING + UPGRADE_HEIGHT + PADDING
        
        # Total height = space per tower * number of towers
        total_height = SPACE_PER_UPGRADE * len(upgrade_config)

        # Draw upgrade shop area rectangle
        shop_rect = pygame.Rect(
            UI_POSITIONS['tower_shop'][0] + size * 2,           # x position
            UI_POSITIONS['tower_shop'][1],           # y position
            size * 2,                                # width
            total_height                             # calculated height
        )
        pygame.draw.rect(self.screen, Colors.BLACK, shop_rect, 2)  # 2 is border thickness
        # Draw upgrade options
        next_y = shop_rect.top
        for element_name, stats in upgrade_config.items():
            next_y = self.__draw_upgrade_option(
                name=element_name.capitalize(),
                shop_rect=shop_rect,
                tower_config=stats,
                top_y=next_y
        )

    def __draw_tower_option(self, name, shop_rect, tower_config, top_y):
        size = TOWER_CONFIG['size']
        # Draw tower name
        name_txt = self.medium_font.render(name, True, Colors.WHITE)
        name_rect = name_txt.get_rect(center=(shop_rect.centerx, top_y + 20))
        self.screen.blit(name_txt, name_rect)
        # Draw tower representation (simple square for now)
        tower_rect = pygame.Rect(shop_rect.centerx - size//2, name_rect.bottom + 10, size, size)
        self.shop_towers[name] = tower_rect
        pygame.draw.rect(self.screen, tower_config['color'], tower_rect)
        # Draw cost on tower
        cost_txt = self.small_font.render(f"${tower_config['cost']}", True, Colors.WHITE)
        cost_rect = cost_txt.get_rect(center=(tower_rect.centerx, tower_rect.top + size//2))
        self.screen.blit(cost_txt, cost_rect)

        return tower_rect.bottom + 10  # Return bottom y for next option
    
    def __draw_upgrade_option(self, name, shop_rect, tower_config, top_y):
        size = TOWER_CONFIG['size']
        # Draw tower name
        name_txt = self.medium_font.render(name, True, Colors.WHITE)
        name_rect = name_txt.get_rect(center=(shop_rect.centerx, top_y + 20))
        self.screen.blit(name_txt, name_rect)
        # Draw tower representation (simple circle for now)
        tower_rect = pygame.Rect(shop_rect.centerx - size//2, name_rect.bottom + 10, size, size)
        self.shop_towers[name] = tower_rect
        pygame.draw.circle(self.screen, tower_config['color'], tower_rect.center, size//2)
        # Draw cost on tower
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