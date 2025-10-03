# Game constants and helper functions
import pygame

def distance(pos1, pos2):
    """Calculate distance between two points."""
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

def load_image(path, scale=None):
    """Load and optionally scale an image."""
    try:
        image = pygame.image.load(path)
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error:
        # Return a placeholder colored rectangle if image not found
        surf = pygame.Surface((32, 32))
        surf.fill((255, 0, 255))  # Magenta placeholder
        return surf