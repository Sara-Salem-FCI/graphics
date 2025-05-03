from OpenGL.GL import *
from OpenGL.GLU import *
def draw_circle_bresenham(xc, yc, radius, color):
    glColor3f(*color)
    glBegin(GL_POINTS)
    x = 0
    y = radius
    d = 3 - 2 * radius
    
    while x <= y:
        glVertex2f(xc + x, yc + y)
        glVertex2f(xc - x, yc + y)
        glVertex2f(xc + x, yc - y)
        glVertex2f(xc - x, yc - y)
        glVertex2f(xc + y, yc + x)
        glVertex2f(xc - y, yc + x)
        glVertex2f(xc + y, yc - x)
        glVertex2f(xc - y, yc - x)
        
        if d < 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
        x += 1
    glEnd()