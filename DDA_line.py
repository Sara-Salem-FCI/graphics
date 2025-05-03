from OpenGL.GL import *
from OpenGL.GLU import *
def draw_line_dda(x1, y1, x2, y2, color):
    glColor3f(*color)
    glBegin(GL_POINTS)
    dx, dy = x2 - x1, y2 - y1
    steps = max(abs(dx), abs(dy))
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x1, y1
    for _ in range(steps + 1):
        glVertex2f(round(x), round(y))
        x += x_inc
        y += y_inc
    glEnd()