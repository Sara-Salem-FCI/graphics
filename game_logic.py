import math
import random
import time
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from draw_objects import *

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