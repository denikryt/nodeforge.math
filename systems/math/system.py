"""Package entrypoint for NodeForge Math callable constructors."""

CONSTRUCTORS = [
    "sin", "cos", "tan",
    "asin", "acos", "atan",
    "sqrt", "abs", "floor", "ceil", "round", "fract",
    "radians", "degrees", "exp",
    "min", "max", "pow", "log", "atan2", "mod",
    "ln", "clamp", "mix", "select", "map_range",
    "noise", "random_value",
]


def load_handlers():
    """Load runtime handlers lazily after constructor name discovery."""
    from .constructors import HANDLERS

    return HANDLERS


__all__ = ["CONSTRUCTORS", "load_handlers"]
