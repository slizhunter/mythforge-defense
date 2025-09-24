import pygame, random
import time
from .enemy import Enemy
from .map import PATH_POINTS, TOWER_POINTS, TOWER_RECTS, draw_path, draw_tower_spots
from .tower import Tower
from .utils import Colors

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

        # Towers
        self.towers = []

        # Enemies
        self.enemies = []

        # Stats
        self.lives = 20
        self.money = 100
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left mouse click
                for i, rect in enumerate(TOWER_RECTS):
                    if rect.collidepoint(event.pos):
                        self.place_tower(i)
                        break
    
    def place_tower(self, spot_index):
        if spot_index >= len(TOWER_POINTS):
            return False
        
        spot_rect = TOWER_RECTS[spot_index]
        for existing_tower in self.towers:
            if spot_rect.collidepoint(existing_tower.x, existing_tower.y):
                print("Spot already occupied!")
                return False

        if self.money < Tower.get_cost():
            print("Insufficient money!")
            return False

        x, y, width, height = TOWER_POINTS[spot_index]
        
        # Center the tower in the spot
        tower_x = x + width // 2
        tower_y = y + height // 2
        
        # Create tower
        new_tower = Tower(tower_x, tower_y, width, 200, TOWER_RECTS[spot_index])
        self.towers.append(new_tower)

        # Deduct tower cost
        self.money -= Tower.get_cost()

    def update(self, dt):
        if self.state != "playing":
            return
        
        adjusted_dt = dt * self.speed_factor

        # Spawn logic
        self.spawn_timer += adjusted_dt
        if self.spawn_timer >= self.spawn_interval:
            self.enemies.append(Enemy(PATH_POINTS))
            self.spawn_timer = 0

        # Update every enemy
        for enemy in self.enemies:
            enemy.update(adjusted_dt)

        # Handle goal reached / cleanup
        for enemy in self.enemies[:]:
            if enemy.reached_goal:
                self.enemies.remove(enemy)
                self.lives -= 1
            elif enemy.is_dead():
                self.enemies.remove(enemy)
        
        # Check if enemy is in tower range
        for t, tower in enumerate(self.towers):
            for e, enemy in enumerate(self.enemies):
                if tower.detect_enemy(enemy.get_pos(), enemy.get_size()):
                    print(f"Enemy{e} in range of tower{t}!")

        # Game-over check
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
        text = self.font.render("Myth-Forge Defense", True, self.text_color)
        self.screen.blit(text, (10, 10))

        # --- tower placement ---
        draw_tower_spots(self.screen, TOWER_POINTS)
        mouse_pos = pygame.mouse.get_pos()
        for tower in self.towers:
            tower.update_hover(mouse_pos)
            tower.draw(self.screen)

        # --- path + enemies ---
        draw_path(self.screen, PATH_POINTS)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # --- UI text ---
        money_txt = self.font.render(f"Money: {self.money}", True, (255,255,255))
        self.screen.blit(money_txt, (500, 10))
        lives_txt = self.font.render(f"Lives: {self.lives}", True, (255,255,255))
        self.screen.blit(lives_txt, (900, 10))
        speed_txt = self.font.render(f"Speed: {self.speed_factor}", True, (255,255,255))
        self.screen.blit(speed_txt, (10, 740))
    
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
