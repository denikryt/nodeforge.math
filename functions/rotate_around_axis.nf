from packages import math

def rotate_around_axis(
    v: Vector['V'] = vector(1, 0, 0),
    axis: Vector['Axis'] = vector(0, 0, 1),
    angle: Float['Angle'] = 0.0,
) -> Vector['Vector']:
    axis_n = normalize(axis)
    cos_a = cos(angle)
    sin_a = sin(angle)
    term_a = v * cos_a
    term_b = cross(axis_n, v) * sin_a
    term_c = axis_n * (dot(axis_n, v) * (1.0 - cos_a))
    return term_a + term_b + term_c
