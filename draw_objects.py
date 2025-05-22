from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from DDA_line import *
from bresenham_line import *
from midpoint_circle import *
from midpoint_ellipse import *
from rotation import *
from scaling import *
from constants import *

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