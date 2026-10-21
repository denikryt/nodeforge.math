"""Contract tests for the nodeforge.math backend-only v2 system owner."""

from __future__ import annotations

import json
from pathlib import Path

from NodeForge import packages
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


def test_math_271_manifest_targets_nodeforge_065x():
    """The Math 2.7.1 manifest admits the NodeForge 0.65.x patch line."""
    manifest = packages.validate_package_root(ROOT)
    raw = json.loads((ROOT / "nodeforge_package.json").read_text(encoding="utf-8"))
    assert manifest.version == "2.7.1"
    assert manifest.import_name == "math"
    assert raw["nodeforge_min_version"] == "0.65.0"
    assert raw["nodeforge_max_version"] == "0.65.1"


def test_math_package_ships_only_supported_v2_python_owner():
    """The reference Math package retains its backend-only Extension API v2 owner."""
    assert (MATH_OWNER / "interface.py").is_file()
    assert (MATH_OWNER / "operations.py").is_file()
    assert "NodeForge.extension_api" in (MATH_OWNER / "operations.py").read_text(encoding="utf-8")


def test_math_package_ships_no_v1_execution_artifact():
    """No shipped Python source depends on the physically removed v1 compiler APIs."""
    assert not (ROOT / "examples" / "mandelbrot").exists()
    forbidden = (
        "BACKEND_BUILTINS",
        "NodeForge.statements",
        "NodeForge.compiler",
        "NodeForge.runtime",
        "NodeForge.expression_compiler",
        "NodeForge.statement_compiler",
    )
    for path in ROOT.rglob("*.py"):
        if ".git" in path.parts or "tests" in path.parts:
            continue
        source = path.read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in source, (path.relative_to(ROOT), token)


def test_math_manifest_no_longer_caps_at_nodeforge_0621():
    """The coordinated package metadata cannot remain pinned to the pre-cutover core patch."""
    raw = json.loads((ROOT / "nodeforge_package.json").read_text(encoding="utf-8"))
    assert raw["nodeforge_max_version"] != "0.62.1"
