"""Physical Geometry Nodes implementations for the NodeForge Math extension."""

from __future__ import annotations

import math

from NodeForge.extension_api import ExtensionBackendValue, NFType


_UNARY_OPERATIONS = {
    "sin": "SINE",
    "cos": "COSINE",
    "tan": "TANGENT",
    "asin": "ARCSINE",
    "acos": "ARCCOSINE",
    "atan": "ARCTANGENT",
    "sqrt": "SQRT",
    "abs": "ABSOLUTE",
    "floor": "FLOOR",
    "ceil": "CEIL",
    "round": "ROUND",
    "fract": "FRACT",
    "radians": "RADIANS",
    "degrees": "DEGREES",
    "exp": "EXPONENT",
}

_BINARY_OPERATIONS = {
    "min": "MINIMUM",
    "max": "MAXIMUM",
    "pow": "POWER",
    "log": "LOGARITHM",
    "atan2": "ARCTAN2",
    "mod": "MODULO",
}


def _new_node(context, bl_idname: str, *, dx: float = 0.0, dy: float = 0.0):
    """Create one node in the current candidate tree at a package-owned offset."""
    node = context.group.nodes.new(bl_idname)
    x, y = context.location
    node.location = (x + dx, y + dy)
    return node


def _link(context, value: ExtensionBackendValue, socket) -> None:
    """Link one package-facing runtime value into a Blender input socket."""
    if not isinstance(value, ExtensionBackendValue):
        raise TypeError("Math runtime argument must be ExtensionBackendValue")
    context.group.links.new(value.socket, socket)


def _wire_numeric(context, value, socket) -> None:
    """Wire a runtime numeric value or assign one detached numeric default."""
    if isinstance(value, ExtensionBackendValue):
        if value.typ not in {NFType.FLOAT, NFType.INT}:
            raise TypeError("Math numeric option must be Float or Int")
        context.group.links.new(value.socket, socket)
        return
    if type(value) not in {int, float}:
        raise TypeError("Math numeric option must be a detached int/float or runtime value")
    socket.default_value = float(value)


def _math(context, operation: str, values):
    """Create one Shader Math node for already-normalized numeric runtime values."""
    node = _new_node(context, "ShaderNodeMath")
    node.operation = operation
    for index, value in enumerate(values):
        _link(context, value, node.inputs[index])
    return context.value(node.outputs[0], NFType.FLOAT)


def _unary(context, operation: str, value):
    return _math(context, operation, (value,))


def _binary(context, operation: str, a, b):
    return _math(context, operation, (a, b))


def ln_node(context, value):
    """Realize natural logarithm as Blender LOGARITHM with an explicit e base."""
    base = _new_node(context, "ShaderNodeValue", dx=20, dy=-40)
    base.outputs[0].default_value = math.e
    node = _new_node(context, "ShaderNodeMath")
    node.operation = "LOGARITHM"
    _link(context, value, node.inputs[0])
    context.group.links.new(base.outputs[0], node.inputs[1])
    return context.value(node.outputs[0], NFType.FLOAT)


def clamp_node(context, value, min, max):
    """Realize clamp(value, min, max)."""
    node = _new_node(context, "ShaderNodeClamp")
    _link(context, value, node.inputs[0])
    _link(context, min, node.inputs[1])
    _link(context, max, node.inputs[2])
    return context.value(node.outputs[0], NFType.FLOAT)


def mix_node(context, a, b, factor):
    """Realize Float/Vector mix with the existing uniform clamped-factor behavior."""
    if a.typ is not b.typ or a.typ not in {NFType.FLOAT, NFType.VECTOR}:
        raise TypeError("mix() requires same-type Float or Vector branches")
    node = _new_node(context, "ShaderNodeMix")
    node.data_type = "VECTOR" if a.typ is NFType.VECTOR else "FLOAT"
    node.factor_mode = "UNIFORM"
    node.clamp_factor = True
    _link(context, factor, node.inputs[0])
    if a.typ is NFType.FLOAT:
        _link(context, a, node.inputs[2])
        _link(context, b, node.inputs[3])
        output = node.outputs[0]
    else:
        _link(context, a, node.inputs[4])
        _link(context, b, node.inputs[5])
        output = node.outputs[1]
    return context.value(output, a.typ)


_SWITCH_TYPES = {
    NFType.FLOAT: "FLOAT",
    NFType.INT: "INT",
    NFType.VECTOR: "VECTOR",
    NFType.BOOL: "BOOLEAN",
    NFType.GEOMETRY: "GEOMETRY",
    NFType.STRING: "STRING",
    NFType.BUNDLE: "BUNDLE",
}


def select_node(context, cond, true, false):
    """Realize select(cond, true, false) while preserving branch type exactly."""
    if cond.typ is not NFType.BOOL:
        raise TypeError("select() condition must be Bool")
    if true.typ is not false.typ or true.typ not in _SWITCH_TYPES:
        raise TypeError("select() true/false values must have the same supported type")
    node = _new_node(context, "GeometryNodeSwitch")
    node.input_type = _SWITCH_TYPES[true.typ]
    _link(context, cond, node.inputs[0])
    _link(context, false, node.inputs[1])
    _link(context, true, node.inputs[2])
    return context.value(node.outputs[0], true.typ)


def map_range_node(context, value, from_min, from_max, to_min, to_max):
    """Realize numeric map_range with the existing Float Map Range node."""
    node = _new_node(context, "ShaderNodeMapRange")
    node.data_type = "FLOAT"
    for index, item in enumerate((value, from_min, from_max, to_min, to_max)):
        _link(context, item, node.inputs[index])
    return context.value(node.outputs[0], NFType.FLOAT)


def build_noise(context, *args, **kwargs):
    """Realize noise() with optional runtime vector and mixed numeric options."""
    if len(args) > 1:
        raise TypeError("noise() physical adapter received invalid positional shape")
    node = _new_node(context, "ShaderNodeTexNoise")
    node.noise_dimensions = "3D"
    node.normalize = bool(kwargs["normalize"])

    if args:
        vector = args[0]
        _link(context, vector, node.inputs[0])
    else:
        position = _new_node(context, "GeometryNodeInputPosition", dx=20, dy=-80)
        context.group.links.new(position.outputs[0], node.inputs[0])

    for name, index in {
        "scale": 2,
        "detail": 3,
        "roughness": 4,
        "lacunarity": 5,
        "distortion": 8,
    }.items():
        _wire_numeric(context, kwargs[name], node.inputs[index])
    return context.value(node.outputs[0], NFType.FLOAT)


def _default_value_node(context, value: float, *, dy: float):
    """Create one explicit Float Value node used by zero-argument random_value()."""
    node = _new_node(context, "ShaderNodeValue", dx=20, dy=dy)
    node.outputs[0].default_value = float(value)
    return node.outputs[0]


def build_random_value(context, *args, **kwargs):
    """Realize zero/bounded Float or Vector random values with optional id/seed."""
    if len(args) not in {0, 2}:
        raise TypeError("random_value() physical adapter received invalid positional shape")
    node = _new_node(context, "FunctionNodeRandomValue")

    if not args:
        node.data_type = "FLOAT"
        context.group.links.new(_default_value_node(context, 0.0, dy=-80), node.inputs[0])
        context.group.links.new(_default_value_node(context, 1.0, dy=-120), node.inputs[1])
        output_type = NFType.FLOAT
    else:
        min_value, max_value = args
        if min_value.typ is NFType.VECTOR and max_value.typ is NFType.VECTOR:
            node.data_type = "FLOAT_VECTOR"
            output_type = NFType.VECTOR
        elif min_value.typ in {NFType.FLOAT, NFType.INT} and max_value.typ in {NFType.FLOAT, NFType.INT}:
            node.data_type = "FLOAT"
            output_type = NFType.FLOAT
        else:
            raise TypeError("random_value() bounds must both be numeric or both Vector")
        _link(context, min_value, node.inputs[0])
        _link(context, max_value, node.inputs[1])

    id_value = kwargs.get("id")
    if id_value is not None:
        _link(context, id_value, node.inputs[2])

    seed = kwargs["seed"]
    if isinstance(seed, ExtensionBackendValue):
        _link(context, seed, node.inputs[3])
    else:
        if type(seed) is not int:
            raise TypeError("random_value() seed must be NodeForge Int")
        node.inputs[3].default_value = int(seed)

    return context.value(node.outputs[0], output_type)


def _install_operation_wrappers() -> None:
    """Create package-private per-callable wrappers without exposing compiler metadata."""
    for public_name, operation in _UNARY_OPERATIONS.items():
        def unary(context, value, _operation=operation):
            return _unary(context, _operation, value)
        unary.__name__ = f"{public_name}_node"
        unary.__doc__ = f"Realize {public_name}() with one Blender Math node."
        globals()[unary.__name__] = unary
    for public_name, operation in _BINARY_OPERATIONS.items():
        def binary(context, a, b, _operation=operation):
            return _binary(context, _operation, a, b)
        binary.__name__ = f"{public_name}_node"
        binary.__doc__ = f"Realize {public_name}() with one Blender Math node."
        globals()[binary.__name__] = binary


_install_operation_wrappers()
