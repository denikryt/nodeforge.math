from packages import math

def layout_grid(
    geometry: Geometry['Geometry'],
    count: Vector['Count'] = vector(1, 1, 1),
    spacing: Vector['Spacing'] = vector(1, 1, 1),
    centered: Bool['Centered'] = False,
) -> Geometry['Geometry']:
    cx = max(count.x, 1.0)
    cy = max(count.y, 1.0)
    cz = max(count.z, 1.0)

    x_index = mod(index(), cx)
    y_index = mod(floor(index() / cx), cy)
    z_index = floor(index() / (cx * cy))
    pos = vector(x_index, y_index, z_index) * spacing

    extent = vector(cx - 1.0, cy - 1.0, cz - 1.0) * spacing * 0.5
    pos = select(centered, pos - extent, pos)

    geometry = set_position(geometry, pos)
    return geometry
