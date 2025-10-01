import pygame
from .enemy import BasicEnemy, FastEnemy, TankEnemy
from .utils import WAVE_CONFIG, ENEMY_CONFIG, GAME_CONFIG

class WaveManager:
    def __init__(self, path_points):
        self.path_points = path_points # Path enemies will follow, based on map.py
        self.current_wave = -1  # No wave started yet
        self.spawn_timer = 0    # Timer between individual enemy spawns
        self.waves = WAVE_CONFIG['waves'] # List of wave definitions
        self.wave_timer = 0     # Counts time between waves
        self.wave_interval = WAVE_CONFIG['wave_interval']  # seconds between waves
        self.wave_in_progress = False # Is a wave currently active?
        self.current_enemy_group = 0 # Index of current enemy group in wave
        self.remaining_spawns = 0 # Total enemies left to spawn in current wave group

        # Dynamically create enemy type mapping
        self.ENEMY_TYPES = {}
        for enemy_type, stats in ENEMY_CONFIG['types'].items():
            class_name = stats['class']
            # Get the class from the enemy module
            enemy_class = globals()[class_name]
            self.ENEMY_TYPES[enemy_type] = enemy_class

    def update(self, dt, enemy_list):
        # Don't continue if we've completed all waves
        if self.current_wave >= len(self.waves) - 1 and not self.wave_in_progress:
            print("All waves completed!")
            return
        
        if not self.wave_in_progress:                   # Between waves
            self.wave_timer += dt                       # Increment break timer
            if self.wave_timer >= self.wave_interval:   # Time for next wave?
                self._start_next_wave()                 # Start it
            return
            
        wave = self.waves[self.current_wave]            # Current wave details
        groups = wave["groups"]

        # Check if we've finished all enemy groups in this wave
        if (self.current_enemy_group >= len(groups) and 
            self.remaining_spawns <= 0 and 
            len(enemy_list) == 0):
            print(f"Wave {self.current_wave + 1} completed!")
            self.wave_in_progress = False
            self.wave_timer = 0
            self.current_enemy_group = 0
            return

        current_group = groups[self.current_enemy_group]
        self.spawn_timer += dt                          # Increment spawn timer
        
        if (self.spawn_timer >= current_group["interval"] and 
            self.remaining_spawns > 0):                 # Time to spawn next enemy?
            new_enemy = self._spawn_enemy(current_group["type"])
            enemy_list.add(new_enemy)
            self.remaining_spawns -= 1
            self.spawn_timer = 0
            
        # Move to next enemy type if current one is done
        if self.remaining_spawns <= 0:
            #print(f"Finished spawning group {self.current_enemy_group + 1} of wave {self.current_wave + 1}")
            if self.current_enemy_group + 1 < len(groups):
                #print(f"Preparing to spawn group {self.current_enemy_group + 2} of wave {self.current_wave + 1}")
                self.current_enemy_group += 1
                self.remaining_spawns = groups[self.current_enemy_group]["count"]
                self.spawn_timer = 0 # Reset spawn timer for next group
            else:
                # Wait for all enemies to die before completing wave
                if len(enemy_list) == 0:
                    print(f"Wave {self.current_wave + 1} completed!")
                    self.wave_in_progress = False
                    self.wave_timer = 0
                    self.current_enemy_group = 0
    
    def reset(self):
        """Reset wave manager to initial state"""
        self.current_wave = -1  # No wave started yet
        self.spawn_timer = 0
        self.wave_timer = 0
        self.wave_in_progress = False
        self.enemies_spawned = 0
        self.current_enemy_group = 0
        self.remaining_spawns = 0
    
    def _start_next_wave(self):
        # Only increment if we haven't reached the last wave
        if self.current_wave + 1 < len(self.waves): # Check if more waves are available
            self.current_wave += 1                  # Move to next wave
            self.wave_in_progress = True            # Reset spawn variables
            self.spawn_timer = 0                    # Reset spawn timer
            self.current_enemy_group = 0            # Start with first enemy group
            self.remaining_spawns = self.waves[self.current_wave]["groups"][0]["count"]
            print(f"Starting wave {self.current_wave + 1}")
        else:
            print("All waves completed!")
    
    def _spawn_enemy(self, enemy_type):
        """Create a new enemy of specified type"""
        enemy_class = self.ENEMY_TYPES.get(enemy_type)
        if not enemy_class:
            raise ValueError(f"Unknown enemy type: {enemy_type}")
        
        return enemy_class(
            self.path_points
        )

    def get_wave_info(self):
        if self.current_wave == -1:  # First wave hasn't started
            return {
                "current_wave": 1,  # Show as wave 1
                "total_waves": len(self.waves),
                "break_timer": self.wave_interval - self.wave_timer
            }
        return {
            "current_wave": self.current_wave + 1,
            "total_waves": len(self.waves),
            "break_timer": max(0, self.wave_interval - self.wave_timer) if not self.wave_in_progress else 0
        }