import pygame
from ..constants import RED, GREEN, BLUE, YELLOW, WHITE, BLACK
import random

class Brick:
    NORMAL = 1
    TOUGH = 2
    
    def __init__(self, x, y, width, height, brick_type=NORMAL):
        self.rect = pygame.Rect(x, y, width, height)
        self.brick_type = brick_type
        self.hits_required = 2 if brick_type == self.TOUGH else 1
        self.hits = 0
        self.colors = [RED, GREEN, BLUE, YELLOW, (255, 165, 0), (128, 0, 128)]  # Added orange, purple
        self._color = random.choice(self.colors)  # Removed rainbow option as it was causing issues
        
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
        # 3D effect with shadow and highlight
        brick_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        
        # Base brick color
        pygame.draw.rect(brick_surface, self.color, (0, 0, self.rect.width, self.rect.height))
        
        # Add 3D effect
        # Top highlight
        highlight_color = (min(self.color[0] + 50, 255), 
                         min(self.color[1] + 50, 255), 
                         min(self.color[2] + 50, 255))
        pygame.draw.line(brick_surface, highlight_color, 
                        (0, 0), (self.rect.width - 1, 0))
        pygame.draw.line(brick_surface, highlight_color,
                        (0, 0), (0, self.rect.height - 1))
        
        # Shadow effect
        shadow_color = (max(self.color[0] - 50, 0), 
                       max(self.color[1] - 50, 0), 
                       max(self.color[2] - 50, 0))
        pygame.draw.line(brick_surface, shadow_color,
                        (self.rect.width - 1, 0), 
                        (self.rect.width - 1, self.rect.height - 1))
        pygame.draw.line(brick_surface, shadow_color,
                        (0, self.rect.height - 1), 
                        (self.rect.width - 1, self.rect.height - 1))
        
        if self.brick_type == self.TOUGH and self.hits == 0:
            pygame.draw.rect(brick_surface, WHITE, (0, 0, self.rect.width, self.rect.height), 2)
        
        screen.blit(brick_surface, (self.rect.x, self.rect.y)) 