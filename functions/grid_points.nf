from packages import math

def grid_points(
    count: Vector['Count'] = vector(1, 1, 1),
    spacing: Vector['Spacing'] = vector(1, 1, 1),
    centered: Bool['Centered'] = False,
) -> Geometry['Geometry']:
    total = max(count.x, 0.0) * max(count.y, 0.0) * max(count.z, 0.0)
    geometry = points(total)
    geometry = layout_grid(geometry, count=count, spacing=spacing, centered=centered)
    return geometry
