from OpenGL.GL import *
from OpenGL.GLU import *

def draw_line_bresenham(x1, y1, x2, y2, color):
    glColor3f(*color)
    glBegin(GL_POINTS)
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    steep = dy > dx
    
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    error = dx // 2
    y_step = 1 if y1 < y2 else -1
    y = y1
    
    for x in range(x1, x2 + 1):
        if steep:
            glVertex2f(y, x)
        else:
            glVertex2f(x, y)
        error -= dy
        if error < 0:
            y += y_step
            error += dx
    glEnd()