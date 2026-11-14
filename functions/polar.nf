from packages import math

def polar(
    radius: Float['Radius'] = 1.0,
    angle: Float['Angle'] = 0.0,
) -> Vector['Vector']:
    return vector(cos(angle) * radius, sin(angle) * radius, 0.0)
