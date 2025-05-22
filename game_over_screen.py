import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from draw_objects import *

def game_over_screen(score):
    glClear(GL_COLOR_BUFFER_BIT)
    draw_text(350, 300, "GAME OVER", 24, RED)
    draw_text(350, 250, f"Score: {score}", 24)
    draw_text(300, 200, "Press R to Restart", 24)
    draw_text(300, 150, "Press Q to Quit", 24)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True, False
                if event.key == pygame.K_q:
                    return False, True