import pygame
from ..config.tower_config import TOWER_CONFIG
from ..entities.tower import Tower

class TowerManager:
    def __init__(self, game):
        self.game = game
        self.towers = []
        self.selected_tower_type = 'basic'

    def update(self, dt):
        """Update all towers and handle targeting"""
        for tower in self.towers:
            tower.update(dt)
            for enemy in self.game.enemies:
                if tower.detect_enemy(enemy.get_pos(), enemy.get_size()):
                    if not tower.get_target():
                        tower.set_target(enemy)
                else:
                    if tower.get_target() == enemy:
                        tower.set_target(None)

    def draw(self, screen):
        """Draw towers and range previews"""
        mouse_pos = pygame.mouse.get_pos()
        self._draw_tower_range_preview(screen, mouse_pos)
        
        for tower in self.towers:
            tower.update_hover(mouse_pos)
            tower.draw(screen)

    def place_tower(self, spot_index, tower_type='basic'):
        """Place a new tower if possible"""
        if spot_index >= len(self.game.current_map.get_tower_points()):
            return False

        spot_rect = self.game.current_map.get_tower_rects()[spot_index]
        
        # Check if spot is occupied
        if self._is_spot_occupied(spot_rect):
            print("Spot already occupied!")
            return False

        # Check if can afford
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
                    screen, 
                    tower_config['color'], 
                    (x, y), 
                    tower_config['range'],
                    1
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