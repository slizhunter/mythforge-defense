import pygame
import sys
from src.game import Game

def main():
    pygame.init()
    
    # Game settings
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    FPS = 60
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Myth-Forge Defense')
    clock = pygame.time.Clock()
    
    # Initialize game
    game = Game(screen)
    
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)
        
        dt = clock.tick(FPS) / 1000 
        game.update(dt)
        game.draw()
        pygame.display.flip()
        #clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()