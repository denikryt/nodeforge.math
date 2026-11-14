from packages import math

def sign(
    x: Float['X'] = 0.0,
) -> Float['Value']:
    positive_or_zero = select(x > 0.0, 1.0, 0.0)
    return select(x < 0.0, -1.0, positive_or_zero)
