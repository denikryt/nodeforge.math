# Runtime helix ladder built from point grids and instancing.
# Step count is a runtime input, so the node graph does not grow with a compile-time range().

from packages import math

def helix_ladder(
    steps: Int['Steps'] = 24,
    radius: Float['Radius'] = 1.5,
    rise: Float['Rise'] = 0.18,
    turn: Float['Turn'] = 0.45,
    tread_width: Float['Tread Width'] = 0.18,
    tread_thickness: Float['Tread Thickness'] = 0.055,
    post_size: Float['Post Size'] = 0.075,
    phase: Float['Phase'] = 0.0,
) -> Geometry['Geometry']:
    # One point per stair.  The point count is driven by the runtime Steps input.
    pts = grid_points(
        count=vector(steps, 1, 1),
        spacing=vector(1.0, 0.0, 0.0),
        centered=False,
    )

    i = index()
    angle = phase + turn * i
    z = rise * i

    outer_pos = vector(cos(angle) * radius, sin(angle) * radius, z)
    mid_pos = vector(cos(angle) * radius * 0.5, sin(angle) * radius * 0.5, z)

    rung_pts = set_position(pts, mid_pos)
    post_pts = set_position(pts, outer_pos)

    # Rungs are radial bars.  Rotation is field-driven, so the shape updates without recompiling.
    rung = cube(size=vector(radius, tread_width, tread_thickness))
    rungs = instance_on_points(
        rung,
        rung_pts,
        rotation=vector(0, 0, angle),
        realize=True,
    )

    post = cube(size=post_size)
    posts = instance_on_points(post, post_pts, realize=True)

    center_post = cube(size=vector(post_size, post_size, rise * steps))
    center_post = transform(center_post, translation=vector(0, 0, rise * steps * 0.5))

    geo = join([rungs, posts, center_post])
    geo = store_named_attribute(geo, "helix_step_index", i, domain="POINT", type="FLOAT")
    geo = set_material(geo, "NodeForge Helix Ladder")
    return geo
