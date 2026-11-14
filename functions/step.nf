from packages import math

def step(
    edge: Float['Edge'] = 0.0,
    x: Float['X'] = 0.0,
) -> Float['Value']:
    return select(x >= edge, 1.0, 0.0)
