import pygame

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Game state
        self.state = "playing"  # "menu", "playing", "paused", "game_over"
        
        # Colors for testing
        self.bg_color = (50, 50, 50)
        self.text_color = (255, 255, 255)
        
        # Initialize font
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = "paused" if self.state == "playing" else "playing"
    
    def update(self):
        # Game logic updates go here
        pass
    
    def draw(self):
        # Clear screen
        self.screen.fill(self.bg_color)
        
        # Draw based on current state
        if self.state == "playing":
            self.draw_playing()
        elif self.state == "paused":
            self.draw_paused()
    
    def draw_playing(self):
        # Placeholder: draw game world
        text = self.font.render("Myth-Forge Defense - Press ESC to pause", True, self.text_color)
        self.screen.blit(text, (10, 10))
        
        # Draw placeholder path
        pygame.draw.circle(self.screen, (100, 255, 100), (100, 100), 20)  # Start
        pygame.draw.circle(self.screen, (255, 100, 100), (900, 600), 20)  # End
    
    def draw_paused(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        text = self.font.render("PAUSED - Press ESC to resume", True, self.text_color)
        text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(text, text_rect)