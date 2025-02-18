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
        self.particles = []
        self.last_particle_time = pygame.time.get_ticks()

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
            
            # Add particles
            current_time = pygame.time.get_ticks()
            if current_time - self.last_particle_time > 50:  # Spawn every 50ms
                self.particles.append({
                    'x': self.x,
                    'y': self.y,
                    'life': 20,
                    'color': YELLOW
                })
                self.last_particle_time = current_time
            
            # Update particles
            for particle in self.particles[:]:
                particle['life'] -= 1
                if particle['life'] <= 0:
                    self.particles.remove(particle)

    def draw(self, screen):
        # Draw particles
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 20))
            particle_color = (*YELLOW[:3], alpha)
            surface = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(surface, particle_color, (2, 2), 2)
            screen.blit(surface, (int(particle['x'] - 2), int(particle['y'] - 2)))
        
        # Draw ball (no pulsing)
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                         self.radius * 2, self.radius * 2) 