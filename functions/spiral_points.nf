from packages import math

def spiral_points(
    count: Int['Count'] = 16,
    radius: Float['Radius'] = 1.0,
    turns: Float['Turns'] = 1.0,
    height: Float['Height'] = 0.0,
    start_radius: Float['Start Radius'] = 0.0,
    start_angle: Float['Start Angle'] = 0.0,
) -> Geometry['Geometry']:
    count_value = count * 1.0
    geometry = points(max(count_value, 0.0))
    geometry = layout_spiral(
        geometry,
        count=count,
        radius=radius,
        turns=turns,
        height=height,
        start_radius=start_radius,
        start_angle=start_angle,
    )
    return geometry
