from OpenGL.GL import *
from OpenGL.GLU import *
def draw_line_midpoint(x1, y1, x2, y2, color):
    glColor3f(*color)
    glBegin(GL_POINTS)
    
    dx = x2 - x1
    dy = y2 - y1
    d = dy - (dx / 2)
    x = x1
    y = y1
    
    glVertex2f(x, y)
    
    while x < x2:
        x += 1
        if d < 0:
            d += dy
        else:
            d += dy - dx
            y += 1
        glVertex2f(x, y)
    glEnd()