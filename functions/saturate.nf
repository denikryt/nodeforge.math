from packages import math

def saturate(
    x: Float['X'] = 0.0,
) -> Float['Value']:
    return clamp(x, 0.0, 1.0)
