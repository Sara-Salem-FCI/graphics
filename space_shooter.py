import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
from DDA_line import *
from bresenham_line import *
from midpoint_circle import *
from midpoint_ellipse import *
WHITE = (1, 1, 1)
RED = (1, 0, 0)
GREEN = (0, 1, 0)
BLUE = (0, 0, 1)
YELLOW = (1, 1, 0)
CYAN = (0, 1, 1)

def draw_spaceship(x, y):
    # Ship body (triangle) using Bresenham lines
    draw_line_bresenham(x, y, x - 20, y - 30, CYAN)  # Left wing
    draw_line_bresenham(x, y, x + 20, y - 30, CYAN)   # Right wing
    draw_line_bresenham(x - 20, y - 30, x + 20, y - 30, RED)  # Base

def draw_asteroid(x, y, size):
    draw_circle_midpoint(x, y, size, (0.5, 0.5, 0.5))

def draw_enemy(x, y):
    draw_ellipse_midpoint(x, y, 15, 10, RED)

def init():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluOrtho2D(0, display[0], 0, display[1])
    glPointSize(3)

def main():
    init()
    spaceship_x, spaceship_y = 400, 100
    bullets = []
    asteroids = [[random.randint(50, 750), random.randint(400, 550)] for _ in range(5)]
    enemies = [[random.randint(100, 700), random.randint(300, 500)] for _ in range(3)]
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append([spaceship_x, spaceship_y])
        
        # Handle key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and spaceship_x > 30:
            spaceship_x -= 5
        if keys[pygame.K_RIGHT] and spaceship_x < 770:
            spaceship_x += 5
        
        # Update bullets
        for bullet in bullets[:]:
            bullet[1] += 10
            if bullet[1] > 600:
                bullets.remove(bullet)
        
        # Update asteroids
        for asteroid in asteroids[:]:
            asteroid[1] -= 1
            if asteroid[1] < 0:
                asteroids.remove(asteroid)
                asteroids.append([random.randint(50, 750), 600])
        
        # Collision detection
        for bullet in bullets[:]:
            for asteroid in asteroids[:]:
                if math.dist(bullet, asteroid) < 20:
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    asteroids.append([random.randint(50, 750), 600])
                    break
        
        # Drawing
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Draw spaceship
        draw_spaceship(spaceship_x, spaceship_y)
        
        # Draw asteroids
        for asteroid in asteroids:
            draw_asteroid(asteroid[0], asteroid[1], 15)
        
        # Draw enemies
        for enemy in enemies:
            draw_enemy(enemy[0], enemy[1])
        
        # Draw bullets (using DDA algorithm)
        for bullet in bullets:
            draw_line_dda(bullet[0], bullet[1], bullet[0], bullet[1] + 10, YELLOW)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()