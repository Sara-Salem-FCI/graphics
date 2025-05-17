from OpenGL.GL import *
from OpenGL.GLU import *

# bresenham_line.py
def draw_line_bresenham(x1, y1, x2, y2, color):
    """رسم خط باستخدام خوارزمية بريزينهام مع دعم القيم العشرية"""
    x1, y1, x2, y2 = int(round(x1)), int(round(y1)), int(round(x2)), int(round(y2))
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    steep = dy > dx
    
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        dx, dy = dy, dx
    
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    error = dx // 2
    y_step = 1 if y1 < y2 else -1
    y = y1
    
    glColor3f(*color)
    glBegin(GL_POINTS)
    for x in range(x1, x2 + 1):
        if steep:
            glVertex2i(y, x)
        else:
            glVertex2i(x, y)
        error -= dy
        if error < 0:
            y += y_step
            error += dx
    glEnd()