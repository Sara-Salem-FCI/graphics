from OpenGL.GL import *
from OpenGL.GLU import *

def draw_circle_midpoint(xc, yc, radius, color):
    glColor3f(*color)
    glBegin(GL_POINTS)
    x, y = 0, radius
    p = 1 - radius
    while x <= y:
        glVertex2f(xc + x, yc + y)
        glVertex2f(xc - x, yc + y)
        glVertex2f(xc + x, yc - y)
        glVertex2f(xc - x, yc - y)
        glVertex2f(xc + y, yc + x)
        glVertex2f(xc - y, yc + x)
        glVertex2f(xc + y, yc - x)
        glVertex2f(xc - y, yc - x)
        if p < 0:
            p += 2 * x + 3
        else:
            p += 2 * (x - y) + 5
            y -= 1
        x += 1
    glEnd()