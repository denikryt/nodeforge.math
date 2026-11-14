from packages import math

def layout_random(
    geometry: Geometry['Geometry'],
    min_value: Vector['Min'] = vector(-1, -1, -1),
    max_value: Vector['Max'] = vector(1, 1, 1),
    seed: Int['Seed'] = 0,
) -> Geometry['Geometry']:
    pos = random_value(min_value, max_value, seed=seed, id=index())
    geometry = set_position(geometry, pos)
    return geometry
