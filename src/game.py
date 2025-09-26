import pygame, random
import time
from .enemy import Enemy
from .map import PATH_POINTS, TOWER_POINTS, TOWER_RECTS, draw_path, draw_tower_spots
from .tower import Tower, BasicTower, RapidTower, SniperTower
from .projectile import Projectile
from .wave_manager import WaveManager
from .utils import Colors, GAME_CONFIG, TOWER_CONFIG, UI_CONFIG, UI_POSITIONS

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
        self.selected_tower_type = 'basic'
        self.towers = []

        # Enemies
        self.enemies = pygame.sprite.Group()

        # Projectiles
        self.projectiles = pygame.sprite.Group()

        # Stats
        self.lives = GAME_CONFIG["starting_lives"]
        self.money = GAME_CONFIG["starting_money"]
        self.speed_factor = GAME_CONFIG["initial_speed"]
        
        # Game state
        self.state = "playing"  # "menu", "playing", "paused", "game_over", "victory"
        
        # Colors for testing
        self.bg_color = UI_CONFIG["bg_color"]
        self.text_color = UI_CONFIG["text_color"]
        
        # Initialize font
        pygame.font.init()
        self.large_font = pygame.font.Font(None, UI_CONFIG["font_size_large"])
        self.medium_font = pygame.font.SysFont('Arial', UI_CONFIG["font_size_medium"])
        self.small_font = pygame.font.SysFont('Arial', UI_CONFIG["font_size_small"])
    
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
                        self.place_tower(i, self.selected_tower_type)
                        break
        ''' --- Alternate tower placement ---
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left mouse click
                self.place_tower_anywhere()
        '''

    def update(self, dt):
        if self.state != "playing":
            return
        
        adjusted_dt = dt * self.speed_factor

        if self._check_victory():
            return

        # Spawn logic
        self.wave_manager.update(adjusted_dt, self.enemies)

        self._update_enemies(adjusted_dt)
        self._update_towers(adjusted_dt)
        self._update_projectiles(adjusted_dt)

        # Game-over check
        if self.lives <= 0:
            self.state = "game_over"
    
    def _check_victory(self):
        # Check for victory (all waves complete and no enemies left)
        if (self.wave_manager.current_wave >= len(self.wave_manager.waves) - 1 and 
            not self.wave_manager.wave_in_progress and 
            len(self.enemies) == 0):
            self.state = "victory"
            return True
        return False
    
    def _update_enemies(self, dt):
        # Update every enemy
        self.enemies.update(dt)

        # Handle goal reached / cleanup
        for enemy in list(self.enemies):
            if enemy.reached_goal:
                enemy.kill()  # Removes from all sprite groups
                self.lives -= 1
            elif enemy.is_dead():
                enemy.kill()
                self.money += enemy.get_value()
        
    def _update_towers(self, dt):
        # Check if enemy is in tower range
        for t, tower in enumerate(self.towers):
            tower.update(dt)
            for e, enemy in enumerate(self.enemies):
                if tower.detect_enemy(enemy.get_pos(), enemy.get_size()):
                    if not tower.get_target():
                        tower.set_target(enemy)
                        print(f"Enemy{e} in range of tower{t}!")
                else:
                    if tower.get_target() == enemy:
                        tower.set_target(None)

    def _update_projectiles(self, dt):
        # Update projectiles
        self.projectiles.update(dt)
        
        # Check projectile collisions with enemies
        hits = pygame.sprite.groupcollide(self.projectiles, self.enemies, True, False)
        for projectile, enemies_hit in hits.items():
            for enemy in enemies_hit:
                enemy.take_damage(projectile.damage)

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
        self._draw_game_world()
        self._draw_towers()
        draw_path(self.screen, PATH_POINTS)
        self._draw_enemies()
        self.projectiles.draw(self.screen)
        self._draw_wave_info()
        self._draw_ui_stats()

    def _draw_game_world(self):
        # --- draw game world ---
        title_txt = self.large_font.render("Myth-Forge Defense", True, self.text_color)
        self.screen.blit(title_txt, UI_POSITIONS["title"])

        # --- draw tower selection ---
        # Draw tower shop area rectangle
        shop_rect = pygame.Rect(10, 200, TOWER_CONFIG['size'] * 2, TOWER_CONFIG['size'] * 7)  # x, y, width, height
        pygame.draw.rect(self.screen, Colors.BLACK, shop_rect, 2)  # 2 is border thickness
        # Draw basic tower option
        basic_name_txt = self.medium_font.render("Basic", True, Colors.WHITE)
        basic_name_rect = basic_name_txt.get_rect(center=(shop_rect.centerx, shop_rect.top + 20))
        self.screen.blit(basic_name_txt, basic_name_rect)
        basic_tower_rect = pygame.Rect(30, basic_name_rect.bottom + 10, TOWER_CONFIG['size'], TOWER_CONFIG['size'])
        pygame.draw.rect(self.screen, TOWER_CONFIG['basic']['color'], basic_tower_rect)
        basic_cost_txt = self.small_font.render(f"${TOWER_CONFIG['basic']['cost']}", True, Colors.WHITE)
        basic_cost_rect = basic_cost_txt.get_rect(center=(basic_tower_rect.centerx, basic_tower_rect.top + TOWER_CONFIG['size']//2))
        self.screen.blit(basic_cost_txt, basic_cost_rect)
        # Draw rapid tower option
        rapid_name_txt = self.medium_font.render("Rapid", True, Colors.WHITE)
        rapid_name_rect = rapid_name_txt.get_rect(center=(shop_rect.centerx, basic_tower_rect.bottom + 20))
        self.screen.blit(rapid_name_txt, rapid_name_rect)
        rapid_tower_rect = pygame.Rect(30, rapid_name_rect.bottom + 10, TOWER_CONFIG['size'], TOWER_CONFIG['size'])
        pygame.draw.rect(self.screen, TOWER_CONFIG['rapid']['color'], rapid_tower_rect)
        rapid_cost_txt = self.small_font.render(f"${TOWER_CONFIG['rapid']['cost']}", True, Colors.WHITE)
        rapid_cost_rect = rapid_cost_txt.get_rect(center=(rapid_tower_rect.centerx, rapid_tower_rect.top + TOWER_CONFIG['size']//2))
        self.screen.blit(rapid_cost_txt, rapid_cost_rect)
        # Draw sniper tower option
        sniper_name_txt = self.medium_font.render("Sniper", True, Colors.WHITE)
        sniper_name_rect = sniper_name_txt.get_rect(center=(shop_rect.centerx, rapid_tower_rect.bottom + 20))
        self.screen.blit(sniper_name_txt, sniper_name_rect)
        sniper_tower_rect = pygame.Rect(30, sniper_name_rect.bottom + 10, TOWER_CONFIG['size'], TOWER_CONFIG['size'])
        pygame.draw.rect(self.screen, TOWER_CONFIG['sniper']['color'], sniper_tower_rect)
        cost_txt = self.small_font.render(f"${TOWER_CONFIG['sniper']['cost']}", True, Colors.WHITE)
        cost_rect = cost_txt.get_rect(center=(sniper_tower_rect.centerx, sniper_tower_rect.top + TOWER_CONFIG['size']//2))
        self.screen.blit(cost_txt, cost_rect)


    def _draw_towers(self):
        # --- tower placement ---
        draw_tower_spots(self.screen, TOWER_POINTS)
        mouse_pos = pygame.mouse.get_pos()
        for tower in self.towers:
            tower.update_hover(mouse_pos)
            tower.draw(self.screen)
    
    def _draw_enemies(self):
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
    def _draw_wave_info(self):
        # --- wave info ---
        wave_info = self.wave_manager.get_wave_info()
        wave_txt = self.large_font.render(f"Wave: {wave_info['current_wave']}/{wave_info['total_waves']}", True, (255,255,255))
        self.screen.blit(wave_txt, UI_POSITIONS["wave"])
        
        if wave_info['break_timer'] > 0:
            break_txt = self.large_font.render(f"Next wave in: {wave_info['break_timer']:.1f}", True, (255,255,255))
            self.screen.blit(break_txt, (self.screen_width//2 - 100, 50))
    
    def _draw_ui_stats(self):
        # --- UI text ---
        money_txt = self.large_font.render(f"Money: {self.money}", True, (255,255,255))
        self.screen.blit(money_txt, UI_POSITIONS["money"])
        lives_txt = self.large_font.render(f"Lives: {self.lives}", True, (255,255,255))
        self.screen.blit(lives_txt, UI_POSITIONS["lives"])
        speed_txt = self.large_font.render(f"Speed: {self.speed_factor}", True, (255,255,255))
        self.screen.blit(speed_txt, UI_POSITIONS["speed"])
    
    def draw_paused(self):
        self.draw_playing()

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

    def place_tower(self, spot_index, tower_type='basic'):
        if spot_index >= len(TOWER_POINTS):
            return False
        
        spot_rect = TOWER_RECTS[spot_index]
        for existing_tower in self.towers:
            if spot_rect.collidepoint(existing_tower.x, existing_tower.y):
                print("Spot already occupied!")
                return False

        if self.money < TOWER_CONFIG[tower_type]['cost']:
            print("Insufficient money!")
            return False

        x, y, width, height = TOWER_POINTS[spot_index]
        
        # Center the tower in the spot
        tower_x = x + width // 2
        tower_y = y + height // 2
        
        # Create tower
        if tower_type == 'basic':
            new_tower = BasicTower(tower_x, tower_y, TOWER_RECTS[spot_index])
        elif tower_type == 'rapid':
            new_tower = RapidTower(tower_x, tower_y, TOWER_RECTS[spot_index])
        elif tower_type == 'sniper':
            new_tower = SniperTower(tower_x, tower_y, TOWER_RECTS[spot_index])
        new_tower.game = self  # Link back to game for projectile management
        self.towers.append(new_tower)

        # Deduct tower cost
        self.money -= new_tower.get_cost()
        print(f"Placed tower at spot {spot_index}. Money left: {self.money}")

    def place_tower_anywhere(self):
        if self.money < Tower.get_cost():
            print("Insufficient money!")
            return False
        
        mouse_pos = pygame.mouse.get_pos()
        for existing_tower in self.towers:
            if existing_tower.rect.collidepoint(mouse_pos):
                print("Spot already occupied!")
                return False
            
        tower_x, tower_y = mouse_pos
        width = 40  # Default tower size
        
        # Create tower
        new_tower = Tower(tower_x, tower_y, width, 200, pygame.Rect(tower_x - width//2, tower_y - width//2, width, width))
        new_tower.game = self  # Link back to game for projectile management
        self.towers.append(new_tower)

        # Deduct tower cost
        self.money -= new_tower.get_cost()
        print(f"Placed tower. Money left: {self.money}")