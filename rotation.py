import math

def rotate_point(x, y, angle, cx=0, cy=0):
    angle_rad = math.radians(angle)
    x = float(x)
    y = float(y)
    cx = float(cx)
    cy = float(cy)
    x -= cx
    y -= cy
    new_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
    new_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
    return new_x + cx, new_y + cy