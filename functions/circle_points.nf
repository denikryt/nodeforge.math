from packages import math

def circle_points(
    count: Int['Count'] = 16,
    radius: Float['Radius'] = 1.0,
    start_angle: Float['Start Angle'] = 0.0,
    end_angle: Float['End Angle'] = tau,
    include_endpoint: Bool['Include Endpoint'] = False,
) -> Geometry['Geometry']:
    count_value = count * 1.0
    pts = points(max(count_value, 0.0))

    raw_denominator = select(include_endpoint, count_value - 1.0, count_value)
    denominator = max(raw_denominator, 1.0)

    t = index() / denominator
    angle = start_angle + (end_angle - start_angle) * t
    pos = vector(cos(angle) * radius, sin(angle) * radius, 0)

    pts = set_position(pts, pos)
    return pts
