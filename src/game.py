import pygame, random
import time
from .enemy import Enemy
from .map import PATH_POINTS, draw_path

class Game:
    def __init__(self, screen):
        self.init_game(screen)

    def init_game(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Spawning behavior
        self.spawn_timer = 0
        self.spawn_interval = 1.5 # seconds

        # Enemies
        self.enemies = []

        # Stats
        self.lives = 20
        self.speed_factor = 1.0
        
        # Game state
        self.state = "playing"  # "menu", "playing", "paused", "game_over"
        
        # Colors for testing
        self.bg_color = (50, 50, 50)
        self.text_color = (255, 255, 255)
        
        # Initialize font
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
    
    def reset_game(self, screen):
        self.init_game(screen)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state == "playing":
                    self.state = "paused"
                elif self.state == "paused":
                    self.state = "playing"
            elif event.key == pygame.K_r and self.state == "game_over":
                    self.reset_game(self.screen)
            elif event.key == pygame.K_RIGHT:
                if self.state == "playing":
                    self.speed_factor *= 2.0
            elif event.key == pygame.K_LEFT:
                if self.state == "playing":
                    self.speed_factor /= 2.0
    
    def update(self, dt):
        if self.state != "playing":
            return
        
        adjusted_dt = dt * self.speed_factor

        # 1. Spawn logic
        self.spawn_timer += adjusted_dt
        if self.spawn_timer >= self.spawn_interval:
            self.enemies.append(Enemy(PATH_POINTS))
            self.spawn_timer = 0

        # 2. Update every enemy
        for enemy in self.enemies:
            enemy.update(adjusted_dt)

        # 3. Handle goal reached / cleanup
        for enemy in self.enemies[:]:
            if enemy.reached_goal:
                self.enemies.remove(enemy)
                self.lives -= 1
            elif enemy.is_dead():
                self.enemies.remove(enemy)

        # 4. Game-over check
        if self.lives <= 0:
            self.state = "game_over"
    
    def draw(self):
        # Clear screen
        self.screen.fill(self.bg_color)
        
        # Draw based on current state
        if self.state == "playing":
            self.draw_playing()
        elif self.state == "paused":
            self.draw_paused()
        elif self.state == "game_over":
            self.draw_over()
    
    def draw_playing(self):
        # Placeholder: draw game world
        text = self.font.render("Myth-Forge Defense - Press ESC to pause", True, self.text_color)
        self.screen.blit(text, (10, 10))

        # --- path + enemies ---
        draw_path(self.screen, PATH_POINTS)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        # --- UI text ---
        lives_txt = self.font.render(f"Lives: {self.lives}", True, (255,255,255))
        self.screen.blit(lives_txt, (900, 10))
        speed_txt = self.font.render(f"Speed: {self.speed_factor}", True, (255,255,255))
        self.screen.blit(speed_txt, (10, 740))
        
        # Draw placeholder path
        #pygame.draw.circle(self.screen, (100, 255, 100), (100, 100), 20)  # Start
        #pygame.draw.circle(self.screen, (255, 100, 100), (900, 600), 20)  # End
    
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
    
    def draw_over(self):
        text = self.font.render("Game Over - Press R to restart", True, self.text_color)
        text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(text, text_rect)
