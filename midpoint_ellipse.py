from OpenGL.GL import *
from OpenGL.GLU import *

def draw_ellipse_midpoint(xc, yc, a, b, color):
    glColor3f(*color)
    glBegin(GL_POINTS)
    x, y = 0, b
    a_sq, b_sq = a * a, b * b
    p = b_sq - a_sq * b + 0.25 * a_sq
    while 2 * b_sq * x <= 2 * a_sq * y:
        glVertex2f(xc + x, yc + y)
        glVertex2f(xc - x, yc + y)
        glVertex2f(xc + x, yc - y)
        glVertex2f(xc - x, yc - y)
        if p < 0:
            p += 2 * b_sq * x + b_sq
        else:
            p += 2 * b_sq * x - 2 * a_sq * y + b_sq
            y -= 1
        x += 1
    # المنطقة الثانية
    p = b_sq * (x + 0.5)**2 + a_sq * (y - 1)**2 - a_sq * b_sq
    while y >= 0:
        glVertex2f(xc + x, yc + y)
        glVertex2f(xc - x, yc + y)
        glVertex2f(xc + x, yc - y)
        glVertex2f(xc - x, yc - y)
        if p > 0:
            p += -2 * a_sq * y + a_sq
        else:
            p += 2 * b_sq * x - 2 * a_sq * y + a_sq
            x += 1
        y -= 1
    glEnd()