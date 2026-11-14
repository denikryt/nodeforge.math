"""Static regression tests for NodeForge 0.90.2 file-module authoring contracts."""

from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _sources(namespace: str):
    """Yield all shipped .nf modules in a package library namespace."""
    return sorted((ROOT / namespace).glob("*.nf"))


def test_package_retains_one_typed_function_per_file():
    """Every public .nf file exports a same-named typed definition."""
    assert len(_sources("functions")) == 24
    assert len(_sources("examples")) == 9
    for path in (*_sources("functions"), *_sources("examples")):
        module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        declarations = [statement for statement in module.body if isinstance(statement, ast.FunctionDef)]
        assert len(declarations) == 1, path
        assert declarations[0].name == path.stem, path
        assert declarations[0].returns is not None, path
        assert all(isinstance(parameter.annotation, ast.Subscript)
                   and isinstance(parameter.annotation.slice, ast.Constant)
                   and isinstance(parameter.annotation.slice.value, str)
                   for parameter in declarations[0].args.args), path
        assert isinstance(declarations[0].body[-1], ast.Return), path
        assert all(isinstance(statement, (ast.Import, ast.ImportFrom, ast.FunctionDef))
                   for statement in module.body), path
        for statement in ast.walk(declarations[0]):
            if isinstance(statement, ast.Call) and isinstance(statement.func, ast.Name):
                assert statement.func.id not in {
                    "input_float", "input_int", "input_vector", "input_bool",
                    "input_geometry", "input_rotation", "input_string", "output",
                }, (path, statement.lineno)


def test_migration_preserves_special_socket_labels_and_public_names():
    """Typed labels retain legacy socket names when identifiers differ."""
    expected = {
        "functions/pingpong.nf": (("period", "Length"),),
        "functions/layout_random.nf": (("min_value", "Min"), ("max_value", "Max")),
        "functions/copy_by_offsets.nf": (("geo", "Geometry"),),
        "examples/parametric_truss_bridge.nf": (("member", "Structural Member Thickness"),),
    }
    for name, pairs in expected.items():
        statement = ast.parse((ROOT / name).read_text(encoding="utf-8")).body[-1]
        assert isinstance(statement, ast.FunctionDef)
        for identifier, label in pairs:
            parameter = next(a for a in statement.args.args if a.arg == identifier)
            assert isinstance(parameter.annotation, ast.Subscript)
            assert isinstance(parameter.annotation.slice, ast.Constant)
            assert parameter.annotation.slice.value == label


def test_manifest_targets_new_module_version_without_restricting_extension_api():
    """Only the package version and minimum NodeForge compatibility advance."""
    manifest = json.loads((ROOT / "nodeforge_package.json").read_text(encoding="utf-8"))
    assert manifest["version"] == "2.3"
    assert manifest["nodeforge_min_version"] == "0.90.2"
    assert manifest["contents"] == {
        "functions": "functions", "examples": "examples", "systems": "systems",
    }
    assert manifest["permissions"] == {"python": True}
    assert manifest["import_name"] == "math"
