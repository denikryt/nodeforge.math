"""Contract tests for the nodeforge.math backend-only v2 system owner."""

from __future__ import annotations

from pathlib import Path

from NodeForge.extension_registry import ExtensionOwnerSession, capture_owner_code_snapshot
from NodeForge.nf_types import NFType


ROOT = Path(__file__).resolve().parents[1]
MATH_OWNER = ROOT / "systems" / "math"


def test_math_interface_normalizes_complete_v2_inventory():
    """The migrated Math owner exposes the expected v2 callable inventory and overload domains."""
    session = ExtensionOwnerSession(
        capture_owner_code_snapshot(("system", "nodeforge.math", "math"), MATH_OWNER)
    )
    families, refs = session.normalize_interface()
    names = {callable_id.name for callable_id in families}
    assert names == {
        "sin", "cos", "tan", "asin", "acos", "atan", "sqrt", "abs", "floor", "ceil",
        "round", "fract", "radians", "degrees", "exp", "min", "max", "pow", "log", "atan2",
        "mod", "ln", "clamp", "mix", "select", "map_range", "noise", "random_value",
    }
    select_id = next(callable_id for callable_id in families if callable_id.name == "select")
    assert {next(iter(spec.result.nf_types)) for spec in families[select_id]} == {
        NFType.FLOAT,
        NFType.INT,
        NFType.VECTOR,
        NFType.BOOL,
        NFType.GEOMETRY,
        NFType.STRING,
        NFType.BUNDLE,
    }
    assert refs[select_id].attribute == "select_node"


def test_math_physical_module_uses_only_public_extension_boundary():
    """Reference physical code does not regain access to retired compiler/package internals."""
    source = (MATH_OWNER / "operations.py").read_text(encoding="utf-8")
    assert "NodeForge.nodes" not in source
    assert "NodeForge.values" not in source
    assert "Compiler" not in source
    assert "NodeForge.extension_api" in source
