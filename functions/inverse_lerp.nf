
def inverse_lerp(
    a: Float['A'] = 0.0,
    b: Float['B'] = 1.0,
    x: Float['X'] = 0.0,
) -> Float['Value']:
    return (x - a) / (b - a)
