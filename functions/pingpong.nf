from packages import math

def pingpong(
    x: Float['X'] = 0.0,
    period: Float['Length'] = 1.0,
) -> Float['Value']:
    double_length = period * 2.0
    wrapped = mod(mod(x, double_length) + double_length, double_length)
    return period - abs(wrapped - period)
