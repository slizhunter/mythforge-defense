import pygame
from ..config.tower_config import ELEMENTAL_UPGRADES, TOWER_CONFIG
from ..entities.tower import Tower

class TowerManager:
    def __init__(self, game):
        self.game = game
        self.towers = []
        self.selected_tower_type = 'basic'
        self.selected_upgrade_type = None  # 'pyro', 'glacier', 'storm'

    def update(self, dt):
        """Update all towers and handle targeting"""
        for tower in self.towers: # Update each tower
            tower.update(dt)
            self._get_tower_target(tower)

    def draw(self, screen, mouse_pos):
        """Draw towers and range previews"""
        #mouse_pos = pygame.mouse.get_pos()
        if self.game.state == 'playing':
            self._draw_tower_range_preview(screen, mouse_pos)
        
        for tower in self.towers:
            tower.update_hover(mouse_pos)
            tower.draw(screen)

    def place_tower(self, spot_index, tower_type='basic'):
        """Place a new tower if possible"""
        # Validate spot index
        if spot_index >= len(self.game.current_map.get_tower_points()):
            return False

        # Get tower spot rect
        spot_rect = self.game.current_map.get_tower_rects()[spot_index]
        
        # Check if spot is occupied
        if self._is_spot_occupied(spot_rect):
            print("Spot already occupied!")
            return False

        # Check if player can afford
        if self.game.money < TOWER_CONFIG['type'][tower_type]['cost']:
            print("Insufficient money!")
            return False

        x, y, width, height = self.game.current_map.get_tower_points()[spot_index]
        tower_x = x + width // 2
        tower_y = y + height // 2
        
        # Create and place tower
        new_tower = Tower(tower_x, tower_y, spot_rect, tower_type)
        new_tower.game = self.game
        self.towers.append(new_tower)
        
        # Deduct cost
        self.game.money -= new_tower.get_cost()
        print(f"Placed tower at spot {spot_index}. Money left: {self.game.money}")
        return True

    def sell_tower(self, tower):
        """Sell an existing tower"""
        if tower in self.towers:
            self.game.money += tower.get_sell_value()
            self.towers.remove(tower)
            tower.sell()
            print(f"Sold tower. Money now: {self.game.money}")
        else:
            print("Tower not found!")
    
    def upgrade_tower(self, tower, element_type):
        """Upgrade a tower with an elemental type"""
        if tower not in self.towers:
            print("Tower not found!")
            return False
        
        if element_type not in ELEMENTAL_UPGRADES:
            print("Invalid upgrade type!")
            return False
        
        if tower.element is not None:
            print("Tower already upgraded!")
            return False
        
        upgrade_cost = ELEMENTAL_UPGRADES[element_type]['cost']
        if self.game.money < upgrade_cost:
            print("Insufficient money for upgrade!")
            return False
        
        # Apply upgrade
        tower.upgrade(element_type)
        self.game.money -= upgrade_cost
        print(f"Upgraded tower to {element_type}. Money left: {self.game.money}")
        return True

    def _get_tower_target(self, tower):
        enemies_list = list(self.game.enemies)
        if tower.targeting_mode == 'first':
                for enemy in enemies_list:
                    if enemy.flying and TOWER_CONFIG['type'][tower.type].get('can_target_flying', False) is False:
                        continue
                    if tower.detect_enemy(enemy.get_pos(), enemy.get_size()): # Detects first enemy in range
                        if not tower.get_target(): # Assign target if none
                            tower.set_target(enemy)
                    else:
                        if tower.get_target() == enemy: # Clear target if out of range
                            tower.set_target(None)
        elif tower.targeting_mode == 'last':
            for enemy in reversed(enemies_list):
                if enemy.flying and TOWER_CONFIG['type'][tower.type].get('can_target_flying', False) is False:
                        continue
                if tower.detect_enemy(enemy.get_pos(), enemy.get_size()):
                    if not tower.get_target():
                        tower.set_target(enemy)
                else:
                    if tower.get_target() == enemy:
                        tower.set_target(None)
        elif tower.targeting_mode == 'strongest':
            strongest_enemy = None
            max_hp = -1
            for enemy in enemies_list:
                if enemy.flying and TOWER_CONFIG['type'][tower.type].get('can_target_flying', False) is False:
                        continue
                if tower.detect_enemy(enemy.get_pos(), enemy.get_size()):
                    if enemy.hp > max_hp:
                        max_hp = enemy.hp
                        strongest_enemy = enemy
            tower.set_target(strongest_enemy)
        elif tower.targeting_mode == 'weakest':
            weakest_enemy = None
            min_hp = float('inf')
            for enemy in enemies_list:
                if enemy.flying and TOWER_CONFIG['type'][tower.type].get('can_target_flying', False) is False:
                        continue
                if tower.detect_enemy(enemy.get_pos(), enemy.get_size()):
                    if enemy.hp < min_hp:
                        min_hp = enemy.hp
                        weakest_enemy = enemy
            tower.set_target(weakest_enemy)
        elif tower.targeting_mode == 'closest':
            closest_enemy = None
            min_dist = float('inf')
            for enemy in self.game.enemies:
                if enemy.flying and TOWER_CONFIG['type'][tower.type].get('can_target_flying', False) is False:
                        continue
                if tower.detect_enemy(enemy.get_pos(), enemy.get_size()):
                    dist = pygame.math.Vector2((tower.x, tower.y)).distance_to(pygame.math.Vector2(enemy.get_pos()))
                    if dist < min_dist:
                        min_dist = dist
                        closest_enemy = enemy
            tower.set_target(closest_enemy)

    def _is_spot_occupied(self, spot_rect):
        """Check if a tower spot is already occupied"""
        return any(spot_rect.collidepoint(tower.x, tower.y) for tower in self.towers)
        

    def _draw_tower_range_preview(self, screen, mouse_pos):
        """Draw range preview when hovering over tower spots"""
        for rect in self.game.current_map.get_tower_rects():
            if rect.collidepoint(mouse_pos) and not self._is_spot_occupied(rect):
                tower_config = TOWER_CONFIG['type'][self.selected_tower_type]
                x, y = rect.center
                
                # Draw range circle outline
                pygame.draw.circle(
                    screen,                 # Surface
                    tower_config['color'],  # Color
                    (x, y),                 # Center
                    tower_config['range'],  # Radius
                    1                       # Width (1 for outline)
                )
                
                # Draw semi-transparent fill
                range_surface = pygame.Surface(
                    (screen.get_width(), screen.get_height()), 
                    pygame.SRCALPHA
                )
                pygame.draw.circle(
                    range_surface,
                    (*tower_config['color'], 30),
                    (x, y),
                    tower_config['range']
                )
                screen.blit(range_surface, (0, 0))
                break
    
    def cycle_tower_targeting(self, tower):
        """Cycle through available targeting modes"""
        modes = ['first', 'last', 'strongest', 'weakest', 'closest']
        current_index = modes.index(tower.targeting_mode)
        next_index = (current_index + 1) % len(modes)
        tower.set_targeting_mode(modes[next_index])
        print(f"Changed targeting mode to: {modes[next_index]}")