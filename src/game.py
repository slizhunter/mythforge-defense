import pygame

from src.config.projectile_config import ELEMENTAL_EFFECTS

from .entities.map import MAPS
from .entities.tower import Tower
from .entities.projectile import Projectile
from .managers.wave_manager import WaveManager
from .managers.tower_manager import TowerManager
from .managers.ui_manager import UIManager
from .config.game_config import GAME_CONFIG
from .config.tower_config import ELEMENTAL_UPGRADES, TOWER_CONFIG
from .config.ui_config import UI_CONFIG

class Game:
    def __init__(self, screen):
        # Set starting map
        self.current_map = MAPS["level_2"]

        # Initialize game state
        self.init_game(screen)

    def init_game(self, screen):
        # Screen info
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Managers
        self.wave_manager = WaveManager(self, self.current_map.get_path())
        self.ui_manager = UIManager(self, self.screen, self.wave_manager)
        self.tower_manager = TowerManager(self)

        # Enemies
        self.enemies = pygame.sprite.Group()

        # Projectiles
        self.projectiles = pygame.sprite.Group()

        # Game stats
        self.lives = GAME_CONFIG["starting_lives"]
        self.money = GAME_CONFIG["starting_money"]
        self.speed_factor = GAME_CONFIG["initial_speed"]
        
        # Game state
        self.state = "menu"  # "menu", "playing", "paused", "game_over", "victory"
        
        # Colors for testing
        self.bg_color = UI_CONFIG["bg_color"]
    
    def reset_game(self, screen):
        self.enemies.empty()
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
            elif event.key == pygame.K_RETURN:
                if self.state == "menu":
                    self.state = "playing"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.state == "playing":
                if event.button == 1: # left mouse click
                    for i, rect in enumerate(self.current_map.get_tower_rects()):
                        if rect.collidepoint(event.pos):
                            if self.tower_manager._is_spot_occupied(rect):
                                # Check for upgrade if tower exists here
                                for tower in self.tower_manager.towers:
                                    if tower.rect.collidepoint(event.pos):
                                        if self.tower_manager.selected_upgrade_type:
                                            if tower.element == self.tower_manager.selected_upgrade_type:
                                                print("Tower already upgraded!")
                                            else:
                                                success = self.tower_manager.upgrade_tower(tower, self.tower_manager.selected_upgrade_type)
                                                if success:
                                                    print(f"Upgraded tower to {self.tower_manager.selected_upgrade_type}!")
                                            break
                                break  # Spot occupied, no placement
                            self.tower_manager.place_tower(i, self.tower_manager.selected_tower_type)
                            break
                    for name, rect in self.ui_manager.get_shop_towers().items():
                        if rect.collidepoint(event.pos):
                            if name.lower() in TOWER_CONFIG['type']:
                                self.tower_manager.selected_tower_type = name.lower()
                                print(f"Selected tower type: {self.tower_manager.selected_tower_type}")
                                break
                            if name.lower() in ELEMENTAL_UPGRADES:
                                self.tower_manager.selected_upgrade_type = name.lower()
                                print(f"Selected upgrade type: {self.tower_manager.selected_upgrade_type}")
                                break
                elif event.button == 3:  # Right click
                    # Check if clicked on a tower
                    for tower in self.tower_manager.towers:
                        if tower.rect.collidepoint(event.pos):
                            self.tower_manager.sell_tower(tower)
                            break
                elif event.button == 2:  # Middle click/scroll wheel
                # Change targeting mode
                    for tower in self.tower_manager.towers:
                        if tower.rect.collidepoint(event.pos):
                            self.tower_manager.cycle_tower_targeting(tower)
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

        if self.state == "playing":
            # Spawn logic
            self.wave_manager.update(adjusted_dt, self.enemies)

            self._update_enemies(adjusted_dt)
            self.tower_manager.update(adjusted_dt)
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

    def _update_projectiles(self, dt):
        # Update projectiles
        self.projectiles.update(dt)

        # Convert enemies to sprite group if not already
        enemy_sprites = pygame.sprite.Group(self.enemies)
        
        # Check projectile collisions with enemies
        hits = pygame.sprite.groupcollide(
            self.projectiles,           # Group 1: All projectiles
            enemy_sprites,              # Group 2: All enemies
            True,                       # Delete projectiles that hit
            False,                      # Don't delete enemies that get hit
            pygame.sprite.collide_rect  # Use rectangle collision
        )
        # Handle hits and apply damage
        for projectile, enemies_hit in hits.items():
            impact_pos = pygame.math.Vector2(projectile.pos)
            #print(f"Projectile hit! Type: {type(projectile).__name__}")  # Debug print

            for enemy in enemies_hit:
                enemy.take_damage(projectile.damage)
                if projectile.element:
                    effect_data = ELEMENTAL_EFFECTS[projectile.element]
                    if effect_data['type']:
                        enemy.apply_effect({
                            'type': effect_data['type'],
                            'duration': effect_data['duration'],
                            'damage_per_second': effect_data.get('damage_per_second', 0),
                            'slow_pct': effect_data.get('slow_pct', 0)
                        })
                #print(f"Enemy hit! Enemy took {projectile.damage} damage! HP left: {enemy.hp}")
            
            if projectile.type == 'shell':  # Check for splash damage
                #print(f"Processing Shell splash damage...")  # Debug print
                # Check all enemies for splash damage
                for enemy in self.enemies:
                    if enemy not in enemies_hit:  # Skip directly hit enemies
                        enemy_pos = pygame.math.Vector2(enemy.get_pos())  # Convert to Vector2
                        distance_to_impact = enemy_pos.distance_to(impact_pos)
                        #print(f"Checking enemy at distance {distance_to_impact}")  # Debug print
                        if distance_to_impact <= projectile.splash_radius:  # Add explicit radius check
                            splash_damage = projectile.get_splash_damage(distance_to_impact)
                            #print(f"Splash damage calculated: {splash_damage}")  # Debug print
                            if splash_damage > 0:
                                #print(f"Applying splash damage: {splash_damage} at distance {distance_to_impact}")
                                enemy.take_damage(splash_damage)

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
        elif self.state == "menu":
            self.ui_manager.draw_menu()
    
    def draw_playing(self):
        self.ui_manager.draw()
        self.current_map.draw_path(self.screen)
        self.current_map.draw_tower_spots(self.screen)
        self.tower_manager.draw(self.screen)
        self._draw_enemies()
        self.current_map.draw_spawn_point(self.screen)
        self.current_map.draw_end_point(self.screen)
        self.projectiles.draw(self.screen)

    def load_map(self, map_id):
        """Change to a different map"""
        if map_id in MAPS:
            self.current_map = MAPS[map_id]
            self.wave_manager.set_path(self.current_map.get_path())
            self.reset_game()

    def _draw_enemies(self):
        for enemy in self.enemies:
            enemy.draw(self.screen)