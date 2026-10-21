"""Declarative NodeForge Math extension contracts."""

from __future__ import annotations

from typing import Annotated, overload

from NodeForge import (
    Bool,
    Bundle,
    EvaluationMode,
    Float,
    Geometry,
    Int,
    String,
    Vector,
)


RUNTIME = EvaluationMode.RUNTIME_ONLY
MIXED = EvaluationMode.COMPILE_TIME_OR_RUNTIME
STATIC = EvaluationMode.COMPILE_TIME_ONLY
Numeric = Float | Int

EXTENSION_API = 2

EXTENSIONS = {
    "sin": ".operations:sin_node",
    "cos": ".operations:cos_node",
    "tan": ".operations:tan_node",
    "asin": ".operations:asin_node",
    "acos": ".operations:acos_node",
    "atan": ".operations:atan_node",
    "sqrt": ".operations:sqrt_node",
    "abs": ".operations:abs_node",
    "floor": ".operations:floor_node",
    "ceil": ".operations:ceil_node",
    "round": ".operations:round_node",
    "fract": ".operations:fract_node",
    "radians": ".operations:radians_node",
    "degrees": ".operations:degrees_node",
    "exp": ".operations:exp_node",
    "min": ".operations:min_node",
    "max": ".operations:max_node",
    "pow": ".operations:pow_node",
    "log": ".operations:log_node",
    "atan2": ".operations:atan2_node",
    "mod": ".operations:mod_node",
    "ln": ".operations:ln_node",
    "clamp": ".operations:clamp_node",
    "mix": ".operations:mix_node",
    "select": ".operations:select_node",
    "map_range": ".operations:map_range_node",
    "noise": ".operations:build_noise",
    "random_value": ".operations:build_random_value",
}


def sin(value: Annotated[Numeric, RUNTIME]) -> Float: ...
def cos(value: Annotated[Numeric, RUNTIME]) -> Float: ...
def tan(value: Annotated[Numeric, RUNTIME]) -> Float: ...
def asin(value: Annotated[Numeric, RUNTIME]) -> Float: ...
def acos(value: Annotated[Numeric, RUNTIME]) -> Float: ...
def atan(value: Annotated[Numeric, RUNTIME]) -> Float: ...
def sqrt(value: Annotated[Numeric, RUNTIME]) -> Float: ...
def abs(value: Annotated[Numeric, RUNTIME]) -> Float: ...
def floor(value: Annotated[Numeric, RUNTIME]) -> Float: ...
def ceil(value: Annotated[Numeric, RUNTIME]) -> Float: ...
def round(value: Annotated[Numeric, RUNTIME]) -> Float: ...
def fract(value: Annotated[Numeric, RUNTIME]) -> Float: ...
def radians(value: Annotated[Numeric, RUNTIME]) -> Float: ...
def degrees(value: Annotated[Numeric, RUNTIME]) -> Float: ...
def exp(value: Annotated[Numeric, RUNTIME]) -> Float: ...

def min(a: Annotated[Numeric, RUNTIME], b: Annotated[Numeric, RUNTIME]) -> Float: ...
def max(a: Annotated[Numeric, RUNTIME], b: Annotated[Numeric, RUNTIME]) -> Float: ...
def pow(a: Annotated[Numeric, RUNTIME], b: Annotated[Numeric, RUNTIME]) -> Float: ...
def log(a: Annotated[Numeric, RUNTIME], b: Annotated[Numeric, RUNTIME]) -> Float: ...
def atan2(a: Annotated[Numeric, RUNTIME], b: Annotated[Numeric, RUNTIME]) -> Float: ...
def mod(a: Annotated[Numeric, RUNTIME], b: Annotated[Numeric, RUNTIME]) -> Float: ...

def ln(value: Annotated[Numeric, RUNTIME]) -> Float: ...

def clamp(
    value: Annotated[Numeric, RUNTIME],
    min: Annotated[Numeric, RUNTIME],
    max: Annotated[Numeric, RUNTIME],
) -> Float: ...


@overload
def mix(
    a: Annotated[Float, RUNTIME],
    b: Annotated[Float, RUNTIME],
    factor: Annotated[Numeric, RUNTIME],
) -> Float: ...


@overload
def mix(
    a: Annotated[Vector, RUNTIME],
    b: Annotated[Vector, RUNTIME],
    factor: Annotated[Numeric, RUNTIME],
) -> Vector: ...


def mix(*args, **kwargs): ...


@overload
def select(
    cond: Annotated[Bool, RUNTIME],
    true: Annotated[Float, RUNTIME],
    false: Annotated[Float, RUNTIME],
) -> Float: ...


@overload
def select(
    cond: Annotated[Bool, RUNTIME],
    true: Annotated[Int, RUNTIME],
    false: Annotated[Int, RUNTIME],
) -> Int: ...


@overload
def select(
    cond: Annotated[Bool, RUNTIME],
    true: Annotated[Vector, RUNTIME],
    false: Annotated[Vector, RUNTIME],
) -> Vector: ...


@overload
def select(
    cond: Annotated[Bool, RUNTIME],
    true: Annotated[Bool, RUNTIME],
    false: Annotated[Bool, RUNTIME],
) -> Bool: ...


@overload
def select(
    cond: Annotated[Bool, RUNTIME],
    true: Annotated[Geometry, RUNTIME],
    false: Annotated[Geometry, RUNTIME],
) -> Geometry: ...


@overload
def select(
    cond: Annotated[Bool, RUNTIME],
    true: Annotated[String, RUNTIME],
    false: Annotated[String, RUNTIME],
) -> String: ...


@overload
def select(
    cond: Annotated[Bool, RUNTIME],
    true: Annotated[Bundle, RUNTIME],
    false: Annotated[Bundle, RUNTIME],
) -> Bundle: ...


def select(*args, **kwargs): ...


def map_range(
    value: Annotated[Numeric, RUNTIME],
    from_min: Annotated[Numeric, RUNTIME],
    from_max: Annotated[Numeric, RUNTIME],
    to_min: Annotated[Numeric, RUNTIME],
    to_max: Annotated[Numeric, RUNTIME],
) -> Float: ...


@overload
def noise(
    *,
    scale: Annotated[Numeric, MIXED] = 5.0,
    detail: Annotated[Numeric, MIXED] = 2.0,
    roughness: Annotated[Numeric, MIXED] = 0.5,
    lacunarity: Annotated[Numeric, MIXED] = 2.0,
    distortion: Annotated[Numeric, MIXED] = 0.0,
    normalize: Annotated[Bool, STATIC] = False,
) -> Float: ...


@overload
def noise(
    vector: Annotated[Vector, RUNTIME],
    /,
    *,
    scale: Annotated[Numeric, MIXED] = 5.0,
    detail: Annotated[Numeric, MIXED] = 2.0,
    roughness: Annotated[Numeric, MIXED] = 0.5,
    lacunarity: Annotated[Numeric, MIXED] = 2.0,
    distortion: Annotated[Numeric, MIXED] = 0.0,
    normalize: Annotated[Bool, STATIC] = False,
) -> Float: ...


def noise(*args, **kwargs): ...


@overload
def random_value(*, seed: Annotated[Int, MIXED] = 0) -> Float: ...


@overload
def random_value(
    *,
    seed: Annotated[Int, MIXED] = 0,
    id: Annotated[Int, RUNTIME],
) -> Float: ...


@overload
def random_value(
    min: Annotated[Numeric, RUNTIME],
    max: Annotated[Numeric, RUNTIME],
    /,
    *,
    seed: Annotated[Int, MIXED] = 0,
) -> Float: ...


@overload
def random_value(
    min: Annotated[Numeric, RUNTIME],
    max: Annotated[Numeric, RUNTIME],
    /,
    *,
    seed: Annotated[Int, MIXED] = 0,
    id: Annotated[Int, RUNTIME],
) -> Float: ...


@overload
def random_value(
    min: Annotated[Vector, RUNTIME],
    max: Annotated[Vector, RUNTIME],
    /,
    *,
    seed: Annotated[Int, MIXED] = 0,
) -> Vector: ...


@overload
def random_value(
    min: Annotated[Vector, RUNTIME],
    max: Annotated[Vector, RUNTIME],
    /,
    *,
    seed: Annotated[Int, MIXED] = 0,
    id: Annotated[Int, RUNTIME],
) -> Vector: ...


def random_value(*args, **kwargs): ...
