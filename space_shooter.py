import pygame
from pygame.locals import *
from init import init
from game_logic import game_loop
from game_over_screen import game_over_screen

def main():
    init()
    quit_game = False
    
    while not quit_game:
        final_score, should_quit = game_loop()
        if should_quit:
            break
        
        restart, quit_game = game_over_screen(final_score)
        if not restart:
            break
    
    pygame.quit()

main() 