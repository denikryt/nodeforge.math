# Runtime topographic contour stack.
# No compile-time range(), no geometry_builder(), no Python lists, no bottom plate.
# Rings are made from overlapping tangent segments on a runtime point grid.
# Wobble Frequency is an integer so each contour closes without a radial seam.

from packages import math

def topographic_contour_stack(
    rings: Int['Rings'] = 10,
    samples: Int['Samples Per Ring'] = 96,
    base_radius: Float['Base Radius'] = 0.35,
    ring_spacing: Float['Ring Spacing'] = 0.18,
    wobble: Float['Wobble'] = 0.12,
    vertical_step: Float['Vertical Step'] = 0.055,
    ellipse: Float['Ellipse'] = 0.72,
    frequency: Int['Wobble Frequency'] = 4,
    rotation: Float['Rotation'] = 0.0,
    line_thickness: Float['Line Thickness'] = 0.022,
    line_overlap: Float['Line Overlap'] = 1.22,
) -> Geometry['Geometry']:
    pts = grid_points(
        count=vector(samples, rings, 1),
        spacing=vector(1.0, 1.0, 0.0),
        centered=False,
    )

    p = position()
    sample_i = p.x
    ring_i = p.y + 1.0

    angle = tau * sample_i / samples + rotation
    radius0 = base_radius + ring_spacing * ring_i

    # Integer harmonics keep radius(angle = 0) equal to radius(angle = tau).
    primary = sin(angle * frequency + ring_i * 0.71 + rotation) * wobble
    secondary = cos(angle * (frequency + 2) - ring_i * 1.37) * wobble * 0.35
    tertiary = sin(angle * (frequency + 5) + ring_i * 0.23) * wobble * 0.18
    radius = radius0 + primary + secondary + tertiary
    z = vertical_step * ring_i

    contour_pos = vector(cos(angle) * radius, sin(angle) * radius * ellipse, z)
    contour_pts = set_position(pts, contour_pos)

    # Segment length follows circumference, so samples overlap and read as continuous closed contours.
    segment_length = radius * tau / samples * line_overlap
    segment = cube(size=1.0)
    contours = instance_on_points(
        segment,
        contour_pts,
        rotation=vector(0.0, 0.0, angle + tau * 0.25),
        scale=vector(segment_length, line_thickness, line_thickness),
        realize=True,
    )

    geo = contours
    geo = store_named_attribute(geo, "contour_ring", ring_i, domain="POINT", type="FLOAT")
    geo = store_named_attribute(geo, "contour_radius", radius, domain="POINT", type="FLOAT")
    geo = set_material(geo, "NodeForge Topographic Contours")
    return geo
