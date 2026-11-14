from packages import math

def remap(
    x: Float['X'] = 0.0,
    in_min: Float['In Min'] = 0.0,
    in_max: Float['In Max'] = 1.0,
    out_min: Float['Out Min'] = 0.0,
    out_max: Float['Out Max'] = 1.0,
) -> Float['Value']:
    t = inverse_lerp(in_min, in_max, x)
    return out_min + t * (out_max - out_min)
