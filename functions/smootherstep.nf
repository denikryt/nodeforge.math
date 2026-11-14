from packages import math

def smootherstep(
    edge0: Float['Edge0'] = 0.0,
    edge1: Float['Edge1'] = 1.0,
    x: Float['X'] = 0.0,
) -> Float['Value']:
    t = saturate(inverse_lerp(edge0, edge1, x))
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)
