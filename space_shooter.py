import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import random
import time
from DDA_line import *
from bresenham_line import *
from midpoint_circle import *
from midpoint_ellipse import *
from rotation import *
from scaling import *

WHITE = (1, 1, 1)
RED = (1, 0, 0)
GREEN = (0, 1, 0)
BLUE = (0, 0, 1)
YELLOW = (1, 1, 0)
CYAN = (0, 1, 1)

def draw_spaceship(x, y, angle=0, scale=1.0):
    center_x, center_y = int(round(x)), int(round(y))
    
    base_points = [
        (center_x, center_y + 30),
        (center_x - 20, center_y - 10),
        (center_x + 20, center_y - 10)
    ]
    
    scaled_points = scale_object(base_points, scale, scale, center_x, center_y)
    
    if angle != 0:
        rotated_points = []
        for px, py in scaled_points:
            rx, ry = rotate_point(px, py, angle, x, y)
            rotated_points.append((rx, ry))
        scaled_points = rotated_points
    
    draw_line_bresenham(scaled_points[0][0], scaled_points[0][1], 
                       scaled_points[1][0], scaled_points[1][1], CYAN)
    draw_line_bresenham(scaled_points[0][0], scaled_points[0][1], 
                       scaled_points[2][0], scaled_points[2][1], CYAN)
    draw_line_bresenham(scaled_points[1][0], scaled_points[1][1], 
                       scaled_points[2][0], scaled_points[2][1], CYAN)

def draw_asteroid(x, y, size, rotation=0, scale=1.0):
    scaled_size = size * scale
    if rotation != 0:
        x, y = rotate_point(x, y, rotation, x, y)
    draw_circle_midpoint(x, y, scaled_size, YELLOW)

def draw_enemy(x, y, pulse=0, scale=1.0):
    pulse_factor = pulse_scale(scale, pulse)
    rx = 15 * pulse_factor
    ry = 10 * pulse_factor
    draw_ellipse_midpoint(x, y, rx, ry, GREEN)

def draw_bullet(x, y):
    draw_line_dda(x, y, x, y + 10, RED)

def draw_text(x, y, text, font_size=18, color=(1, 1, 1)):
    glColor3f(*color)
    glWindowPos2f(x, y)
    font = GLUT_BITMAP_HELVETICA_18 if font_size == 18 else GLUT_BITMAP_TIMES_ROMAN_24 # type: ignore
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

def init():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluOrtho2D(0, display[0], 0, display[1])
    glPointSize(3)
    glutInit()

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

def game_loop():
    spaceship_x, spaceship_y = 400, 100
    spaceship_angle = 0
    spaceship_scale = 1.0
    bullets = []
    asteroids = [[random.randint(50, 750), random.randint(400, 550), 0] for _ in range(5)]
    enemies = [[random.randint(100, 700), random.randint(300, 500), 0] for _ in range(3)]
    score = 0
    lives = 3
    game_active = True
    level = 1
    start_time = time.time()
    clock = pygame.time.Clock()
    
    while game_active:
        current_time = time.time()
        level_time = current_time - start_time
        level = min(5, 1 + int(level_time / 30))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score, True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append([spaceship_x, spaceship_y])
                if event.key == pygame.K_ESCAPE:
                    return score, True
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if spaceship_x > 30:
                spaceship_x -= 5
            spaceship_angle = 15
            spaceship_scale = 1.1
        elif keys[pygame.K_RIGHT]:
            if spaceship_x < 770:
                spaceship_x += 5
            spaceship_angle = -15
            spaceship_scale = 1.1
        else:
            spaceship_angle *= 0.9
            spaceship_scale = 1.0
        
        for asteroid in asteroids:
            asteroid[2] = (asteroid[2] + 1) % 360 
        
        for enemy in enemies:
            enemy[2] += 0.1 
        
        for bullet in bullets[:]:
            bullet[1] += 10
            if bullet[1] > 600:
                bullets.remove(bullet)
        
        for asteroid in asteroids[:]:
            asteroid[1] -= 1 + level * 0.5
            if asteroid[1] < 0:
                asteroids.remove(asteroid)
                asteroids.append([random.randint(50, 750), 600, 0])
        
        for enemy in enemies[:]:
            enemy[1] -= 0.5 + level * 0.3
            if enemy[1] < 0:
                enemies.remove(enemy)
                enemies.append([random.randint(100, 700), 600, 0])
        
        for bullet in bullets[:]:
            for asteroid in asteroids[:]:
                if math.dist(bullet, asteroid[:2]) < 20:
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    asteroids.append([random.randint(50, 750), 600, 0])
                    score += 10
                    break
            
            for enemy in enemies[:]:
                if math.dist(bullet, enemy[:2]) < 25:
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    enemies.append([random.randint(100, 700), 600, 0])
                    score += 20
                    break
        
        for asteroid in asteroids[:]:
            if math.dist([spaceship_x, spaceship_y], asteroid[:2]) < 30:
                asteroids.remove(asteroid)
                asteroids.append([random.randint(50, 750), 600, 0])
                lives -= 1
                if lives <= 0:
                    return score, False
        
        for enemy in enemies[:]:
            if math.dist([spaceship_x, spaceship_y], enemy[:2]) < 30:
                enemies.remove(enemy)
                enemies.append([random.randint(100, 700), 600, 0])
                lives -= 1
                if lives <= 0:
                    return score, False
        
        glClear(GL_COLOR_BUFFER_BIT)
        
        draw_spaceship(spaceship_x, spaceship_y, spaceship_angle, spaceship_scale)
        
        for asteroid in asteroids:
            draw_asteroid(asteroid[0], asteroid[1], 15, asteroid[2], 1.0 + level * 0.1)
        
        for enemy in enemies:
            draw_enemy(enemy[0], enemy[1], enemy[2])
        
        for bullet in bullets:
            draw_bullet(bullet[0], bullet[1])
        
        draw_text(20, 580, f"Score: {score}")
        draw_text(20, 550, f"Lives: {lives}")
        draw_text(20, 520, f"Level: {level}")
        draw_text(20, 490, f"Time: {int(level_time)}s")
        
        pygame.display.flip()
        clock.tick(60)
    
    return score, False

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

if __name__ == "__main__":
    main()