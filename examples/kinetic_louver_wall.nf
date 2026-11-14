# Kinetic louver wall.
# Runtime grid dimensions create a facade of tilting zero-thickness blades driven by field math.
# No backing plate, no border frame, no blade size inputs.

from packages import math

def kinetic_louver_wall(
    columns: Int['Columns'] = 18,
    rows: Int['Rows'] = 9,
    spacing_x: Float['Spacing X'] = 0.4,
    spacing_y: Float['Spacing Y'] = 0.4,
    max_tilt: Float['Max Tilt'] = 0.95,
    phase: Float['Phase'] = 0.0,
    wave_x: Float['Wave X'] = 3.2,
    wave_y: Float['Wave Y'] = 1.8,
) -> Geometry['Geometry']:
    pts = grid_points(
        count=vector(columns, rows, 1),
        spacing=vector(spacing_x, spacing_y, 0),
        centered=True,
    )

    p = position()
    wave = sin(p.x * wave_x + p.y * wave_y + phase)
    cross_wave = cos(p.x * wave_y - p.y * wave_x * 0.45 - phase * 0.7)
    tilt = (wave * 0.75 + cross_wave * 0.25) * max_tilt

    blade_size = 0.4
    blade_thickness = 0.0
    blade = cube(size=vector(blade_size, blade_size, blade_thickness))

    geo = instance_on_points(
        blade,
        pts,
        rotation=vector(tilt, 0, 0),
        realize=True,
    )

    geo = store_named_attribute(geo, "louver_tilt", tilt, domain="POINT", type="FLOAT")
    geo = set_material(geo, "NodeForge Kinetic Louvers")
    return geo
