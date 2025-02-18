import pygame
from ..constants import RED, GREEN, BLUE, YELLOW, WHITE
import random

class Brick:
    NORMAL = 1
    TOUGH = 2
    
    def __init__(self, x, y, width, height, brick_type=NORMAL):
        self.rect = pygame.Rect(x, y, width, height)
        self.brick_type = brick_type
        self.hits_required = 2 if brick_type == self.TOUGH else 1
        self.hits = 0
        self._color = random.choice([RED, GREEN, BLUE])  # Store initial color
        
    @property
    def color(self):
        if self.brick_type == self.TOUGH:
            return BLUE if self.hits == 0 else GREEN
        return self._color
            
    def hit(self):
        """Returns True if brick should be destroyed"""
        self.hits += 1
        return self.hits >= self.hits_required

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.brick_type == self.TOUGH and self.hits == 0:
            pygame.draw.rect(screen, WHITE, self.rect, 2) 