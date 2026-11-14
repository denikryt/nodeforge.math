# copy_by_offsets
#
# Pure NodeForge DSL function.
#
# Duplicates input Geometry into the 8 cells around the center of a 3x3 grid.
# This is the Sierpinski-carpet style offset pattern.
#
# Inputs:
#   Geometry - source geometry
#   Scale    - per-copy scale, default vector(1/3, 1/3, 1)

def copy_by_offsets(
    geo: Geometry['Geometry'],
    scale: Vector['Scale'] = vector(1/3, 1/3, 1),
) -> Geometry['Geometry']:
    geo = join([
        transform(geo, translation=vector(-2/3, -2/3, 0), scale=scale),
        transform(geo, translation=vector(0, -2/3, 0), scale=scale),
        transform(geo, translation=vector(2/3, -2/3, 0), scale=scale),

        transform(geo, translation=vector(-2/3, 0, 0), scale=scale),
        transform(geo, translation=vector(2/3, 0, 0), scale=scale),

        transform(geo, translation=vector(-2/3, 2/3, 0), scale=scale),
        transform(geo, translation=vector(0, 2/3, 0), scale=scale),
        transform(geo, translation=vector(2/3, 2/3, 0), scale=scale),
    ])

    return geo
