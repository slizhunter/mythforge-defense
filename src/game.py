import pygame
from .map import (PATH_POINTS, 
                  TOWER_POINTS, 
                  TOWER_RECTS, 
                  draw_path, 
                  draw_tower_spots, 
                  draw_spawn_point,
                  draw_end_point)
from .tower import Tower, BasicTower, RapidTower, SniperTower
from .wave_manager import WaveManager
from .ui_manager import UIManager
from .utils import GAME_CONFIG, TOWER_CONFIG, UI_CONFIG

class Game:
    def __init__(self, screen):
        self.init_game(screen)

    def init_game(self, screen):
        # Screen info
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Wave manager
        self.wave_manager = WaveManager(PATH_POINTS)
        self.wave_manager.set_game(self)  # Link back to game for bonuses

        # UI Manager
        self.ui_manager = UIManager(self.screen)

        # Towers
        self.selected_tower_type = 'basic'
        self.towers = []

        # Enemies
        self.enemies = pygame.sprite.Group()

        # Projectiles
        self.projectiles = pygame.sprite.Group()

        # Game stats
        self.lives = GAME_CONFIG["starting_lives"]
        self.money = GAME_CONFIG["starting_money"]
        self.speed_factor = GAME_CONFIG["initial_speed"]
        
        # Game state
        self.state = "playing"  # "menu", "playing", "paused", "game_over", "victory"
        
        # Colors for testing
        self.bg_color = UI_CONFIG["bg_color"]
    
    def reset_game(self, screen):
        self.enemies.empty()
        self.towers.clear()
        self.projectiles.empty()
        self.wave_manager.reset()
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
                for name, rect in self.ui_manager.get_shop_towers().items():
                    if rect.collidepoint(event.pos):
                        self.selected_tower_type = name.lower()
                        print(f"Selected tower type: {self.selected_tower_type}")
                        break
            elif event.button == 3:  # Right click
                # Check if clicked on a tower
                for tower in self.towers:
                    if tower.rect.collidepoint(event.pos):
                        self.sell_tower(tower)
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
                        #print(f"Enemy{e} in range of tower{t}!")
                else:
                    if tower.get_target() == enemy:
                        tower.set_target(None)

    def _update_projectiles(self, dt):
        # Update projectiles
        self.projectiles.update(dt)

        # Convert enemies to sprite group if not already
        enemy_sprites = pygame.sprite.Group(self.enemies)
        
        # Check projectile collisions with enemies
        hits = pygame.sprite.groupcollide(
            self.projectiles, 
            enemy_sprites, 
            True,  # Destroy projectile on hit
            False, # Do not destroy enemy on hit
            pygame.sprite.collide_rect
        )
        for projectile, enemies_hit in hits.items():
            for enemy in enemies_hit:
                enemy.take_damage(projectile.damage)
                #print(f"Enemy hit! Enemy took {projectile.damage} damage! HP left: {enemy.hp}")

    def draw(self):
        # Clear screen
        self.screen.fill(self.bg_color)
        
        # Draw based on current state
        if self.state == "playing":
            self.draw_playing()
        elif self.state == "paused":
            self.draw_playing()
            self.ui_manager.draw_paused()
        elif self.state == "game_over":
            self.ui_manager.draw_over()
        elif self.state == "victory":
            self.ui_manager.draw_victory()
    
    def draw_playing(self):
        self.ui_manager.draw(self, self.wave_manager)
        self._draw_towers()
        draw_path(self.screen, PATH_POINTS)
        self._draw_enemies()
        draw_spawn_point(self.screen, PATH_POINTS)
        draw_end_point(self.screen, PATH_POINTS)
        self.projectiles.draw(self.screen)

    def _draw_towers(self):
        # --- tower placement ---
        draw_tower_spots(self.screen, TOWER_POINTS)
        mouse_pos = pygame.mouse.get_pos()

        self.__draw_tower_range_preview(mouse_pos)
        for tower in self.towers:
            tower.update_hover(mouse_pos)
            tower.draw(self.screen)
    
    def __draw_tower_range_preview(self, mouse_pos):
        # Draw range preview on hover
        for i, rect in enumerate(TOWER_RECTS):
            if rect.collidepoint(mouse_pos):
                # Only show preview if spot is empty
                spot_empty = True
                for tower in self.towers:
                    if rect.collidepoint(tower.x, tower.y):
                        spot_empty = False
                        break
                        
                if spot_empty:
                    tower_config = TOWER_CONFIG[self.selected_tower_type]
                    # Draw range circle
                    x = rect.centerx
                    y = rect.centery
                    pygame.draw.circle(
                        self.screen, 
                        tower_config['color'], 
                        (x, y), 
                        tower_config['range'],
                        1  # Line width
                    )
                    # Add semi-transparent fill
                    range_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
                    pygame.draw.circle(
                        range_surface,
                        (*tower_config['color'], 30),  # Add alpha value
                        (x, y),
                        tower_config['range']
                    )
                    self.screen.blit(range_surface, (0, 0))
                break

    def _draw_enemies(self):
        for enemy in self.enemies:
            enemy.draw(self.screen)

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

    def sell_tower(self, tower):
        if tower in self.towers:
            self.money += tower.get_sell_value()
            self.towers.remove(tower)
            tower.sell()
            print(f"Sold tower. Money now: {self.money}")
        else:
            print("Tower not found!")

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