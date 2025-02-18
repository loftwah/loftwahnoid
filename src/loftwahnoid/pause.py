import pygame_menu
from .constants import WIDTH, HEIGHT

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