from packages import math

def angle_between(
    a: Vector['A'] = vector(1, 0, 0),
    b: Vector['B'] = vector(0, 1, 0),
) -> Float['Value']:
    return acos(clamp(dot(normalize(a), normalize(b)), -1.0, 1.0))
