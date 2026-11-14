from packages import math

def rotate2d(
    v: Vector['V'] = vector(1, 0, 0),
    angle: Float['Angle'] = 0.0,
) -> Vector['Vector']:
    cos_a = cos(angle)
    sin_a = sin(angle)
    out_x = v.x * cos_a - v.y * sin_a
    out_y = v.x * sin_a + v.y * cos_a
    return vector(out_x, out_y, v.z)
