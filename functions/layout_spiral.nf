from packages import math

def layout_spiral(
    geometry: Geometry['Geometry'],
    count: Int['Count'] = 16,
    radius: Float['Radius'] = 1.0,
    turns: Float['Turns'] = 1.0,
    height: Float['Height'] = 0.0,
    start_radius: Float['Start Radius'] = 0.0,
    start_angle: Float['Start Angle'] = 0.0,
) -> Geometry['Geometry']:
    count_value = count * 1.0
    denominator = max(count_value - 1.0, 1.0)
    t = index() / denominator

    r = start_radius + (radius - start_radius) * t
    angle = start_angle + tau * turns * t
    pos = vector(cos(angle) * r, sin(angle) * r, height * t)

    geometry = set_position(geometry, pos)
    return geometry
