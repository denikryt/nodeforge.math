# Fibonacci / sunflower spiral using runtime points, index(), and instance_on_points().
# Count changes the number of generated instances at runtime.

from packages import math

def fibonacci_spiral(
    geo: Geometry['Geometry'],
    count: Int['Count'] = 120,
    scale: Float['Scale'] = 0.08,
    instance_scale: Float['Instance Scale'] = 0.08,
    turn: Float['Turn'] = 2.39996322973,
) -> Geometry['Geometry']:
    pts = points(count)

    i = index()
    a = i * turn
    r = sqrt(i) * scale

    pts = set_position(
        pts,
        vector(cos(a) * r, sin(a) * r, 0)
    )

    out = instance_on_points(
        geo,
        pts,
        scale=vector(instance_scale, instance_scale, instance_scale)
    )

    return out
