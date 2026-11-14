from packages import math

def wrap(
    x: Float['X'] = 0.0,
    min_value: Float['Min'] = 0.0,
    max_value: Float['Max'] = 1.0,
) -> Float['Value']:
    size = max_value - min_value
    return min_value + mod(mod(x - min_value, size) + size, size)
