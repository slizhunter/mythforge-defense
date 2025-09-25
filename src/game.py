import pygame, random
import time
from .enemy import Enemy
from .map import PATH_POINTS, TOWER_POINTS, TOWER_RECTS, draw_path, draw_tower_spots
from .tower import Tower
from .projectile import Projectile
from .wave_manager import WaveManager
from .utils import Colors

class Game:
    def __init__(self, screen):
        self.init_game(screen)

    def init_game(self, screen):
        # Screen info
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Spawning behavior
        self.wave_manager = WaveManager(PATH_POINTS)

        # Towers
        self.towers = []

        # Enemies
        self.enemies = pygame.sprite.Group()

        # Projectiles
        self.projectiles = pygame.sprite.Group()

        # Stats
        self.lives = 20
        self.money = 100
        self.speed_factor = 1.0
        
        # Game state
        self.state = "playing"  # "menu", "playing", "paused", "game_over", "victory"
        
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
            elif event.key == pygame.K_r and (self.state == "game_over" or self.state == "victory"):
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

    def update(self, dt):
        if self.state != "playing":
            return
        
        adjusted_dt = dt * self.speed_factor

        # Check for victory (all waves complete and no enemies left)
        if (self.wave_manager.current_wave >= len(self.wave_manager.waves) - 1 and 
            not self.wave_manager.wave_in_progress and 
            len(self.enemies) == 0):
            self.state = "victory"
            return

        # Spawn logic
        self.wave_manager.update(adjusted_dt, self.enemies)

        # Update every enemy
        self.enemies.update(adjusted_dt)

        # Handle goal reached / cleanup
        for enemy in list(self.enemies):
            if enemy.reached_goal:
                enemy.kill()  # Removes from all sprite groups
                self.lives -= 1
            elif enemy.is_dead():
                enemy.kill()
                self.money += enemy.get_value()
        
        # Check if enemy is in tower range
        for t, tower in enumerate(self.towers):
            tower.update(adjusted_dt)
            for e, enemy in enumerate(self.enemies):
                if tower.detect_enemy(enemy.get_pos(), enemy.get_size()):
                    if not tower.get_target():
                        tower.set_target(enemy)
                        print(f"Enemy{e} in range of tower{t}!")
                else:
                    if tower.get_target() == enemy:
                        tower.set_target(None)

        # Update projectiles
        self.projectiles.update(adjusted_dt)
        
        # Check projectile collisions with enemies
        hits = pygame.sprite.groupcollide(self.projectiles, self.enemies, True, False)
        for projectile, enemies_hit in hits.items():
            for enemy in enemies_hit:
                enemy.take_damage(projectile.damage)

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
        elif self.state == "victory":
            self.draw_victory()
    
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

        # --- projectiles ---
        self.projectiles.draw(self.screen)

        # Add wave information to UI
        wave_info = self.wave_manager.get_wave_info()
        wave_txt = self.font.render(f"Wave: {wave_info['current_wave']}/{wave_info['total_waves']}", True, (255,255,255))
        self.screen.blit(wave_txt, (700, 10))
        
        if wave_info['break_timer'] > 0:
            break_txt = self.font.render(f"Next wave in: {wave_info['break_timer']:.1f}", True, (255,255,255))
            self.screen.blit(break_txt, (self.screen_width//2 - 100, 50))

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

    def draw_victory(self):
        text = self.font.render("You Won! - Press R to restart", True, self.text_color)
        text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(text, text_rect)

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
        new_tower.game = self  # Link back to game for projectile management
        self.towers.append(new_tower)

        # Deduct tower cost
        self.money -= Tower.get_cost()
