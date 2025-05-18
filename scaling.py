from OpenGL.GL import *
from math import sin

def scale_point(x, y, scale_x, scale_y, center_x, center_y):
    x_new = center_x + (x - center_x) * scale_x
    y_new = center_y + (y - center_y) * scale_y
    return x_new, y_new

def scale_object(points, scale_x, scale_y, center_x, center_y):
    scaled_points = []
    for x, y in points:
        sx, sy = scale_point(x, y, scale_x, scale_y, center_x, center_y)
        scaled_points.append((sx, sy))
    return scaled_points

def pulse_scale(base_scale, time_factor, speed=1.0):
    return base_scale * (1 + sin(time_factor * speed) * 0.2)