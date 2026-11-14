from packages import math

def random_points(
    count: Int['Count'] = 16,
    min_value: Vector['Min'] = vector(-1, -1, -1),
    max_value: Vector['Max'] = vector(1, 1, 1),
    seed: Int['Seed'] = 0,
) -> Geometry['Geometry']:
    count_value = count * 1.0
    geometry = points(max(count_value, 0.0))
    geometry = layout_random(geometry, min_value=min_value, max_value=max_value, seed=seed)
    return geometry
