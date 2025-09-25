import pygame
from .enemy import Enemy

class WaveManager:
    def __init__(self, path_points):
        self.path_points = path_points
        self.current_wave = -1  # No wave started yet
        self.spawn_timer = 0
        self.wave_timer = 0
        self.wave_interval = 5  # seconds between waves
        self.enemies_spawned = 0
        self.wave_in_progress = False

        # Define waves as lists of enemy types
        self.waves = [
            {"count": 5, "interval": 1.5, "hp": 20, "speed": 120},  # Wave 1
            {"count": 8, "interval": 1.2, "hp": 25, "speed": 130},  # Wave 2
            {"count": 10, "interval": 1.0, "hp": 30, "speed": 140}, # Wave 3
            # Add more waves as needed
        ]

        # Start first wave immediately
        self.start_next_wave()

    def start_next_wave(self):
        # Only increment if we haven't reached the last wave
        if self.current_wave + 1 < len(self.waves):
            self.current_wave += 1
            self.wave_in_progress = True
            self.enemies_spawned = 0
            self.spawn_timer = 0
        else:
            print("All waves completed!")  # Optional: add game victory condition

    def update(self, dt, enemy_list):
        # Don't continue if we've completed all waves
        if self.current_wave >= len(self.waves) - 1 and not self.wave_in_progress:
            return
        
        if not self.wave_in_progress:
            self.wave_timer += dt
            if self.wave_timer >= self.wave_interval:
                self.start_next_wave()
            return
            
        if self.current_wave >= len(self.waves):
            return
            
        wave = self.waves[self.current_wave]
        self.spawn_timer += dt
        
        if self.spawn_timer >= wave["interval"] and self.enemies_spawned < wave["count"]:
            new_enemy = Enemy(
                self.path_points,
                speed=wave["speed"],
                max_hp=wave["hp"]
            )
            enemy_list.add(new_enemy)
            self.enemies_spawned += 1
            self.spawn_timer = 0
            
        # Check if wave is complete
        if self.enemies_spawned >= wave["count"] and len(enemy_list) == 0:
            self.wave_in_progress = False
            self.wave_timer = 0
    
    def get_wave_info(self):
        return {
            "current_wave": self.current_wave + 1,
            "total_waves": len(self.waves),
            "break_timer": max(0, self.wave_interval - self.wave_timer) if not self.wave_in_progress else 0
        }