import pygame
import random
from ..constants import WIDTH, YELLOW

class Ball:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.vel_x = 0  # Start with no velocity
        self.vel_y = 0  # Start with no velocity
        self.started = False  # Ball starts inactive
        self.stuck_to_paddle = False  # Add this new flag

    def start(self):
        self.vel_x = random.choice([-1, 1]) * self.speed
        self.vel_y = -self.speed
        self.started = True
        self.stuck_to_paddle = False  # Reset stuck status when starting

    def update(self):
        if not self.stuck_to_paddle:  # Only update position if not stuck
            self.x += self.vel_x
            self.y += self.vel_y
            # Bounce off left/right walls
            if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
                self.vel_x = -self.vel_x
            # Bounce off top wall
            if self.y - self.radius <= 0:
                self.vel_y = -self.vel_y

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                         self.radius * 2, self.radius * 2) 