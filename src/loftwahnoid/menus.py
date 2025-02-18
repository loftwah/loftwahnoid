import pygame
import pygame_menu
from .constants import WIDTH, HEIGHT
from .game import game_loop

def pause_menu(screen):
    resume = [True]

    def resume_game():
        resume[0] = True
        menu.disable()

    def quit_to_menu():
        resume[0] = False
        menu.disable()

    menu = pygame_menu.Menu('Paused', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Resume', resume_game)
    menu.add.button('Quit to Main Menu', quit_to_menu)
    menu.mainloop(screen)
    return resume[0]

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Loftwahnoid Supreme")
    menu = pygame_menu.Menu('Loftwahnoid Supreme', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    menu.add.label("Welcome to Loftwahnoid!")
    menu.add.button('Play', lambda: game_loop(screen))
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen) 