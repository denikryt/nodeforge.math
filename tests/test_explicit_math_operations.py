"""Verify that each Math extension wrapper is explicit and preserves its node operation."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from enum import Enum
import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
UNARY_OPERATIONS = {
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
BINARY_OPERATIONS = {
    "min": "MINIMUM",
    "max": "MAXIMUM",
    "pow": "POWER",
    "log": "LOGARITHM",
    "atan2": "ARCTAN2",
    "mod": "MODULO",
}


@pytest.fixture
def operations(monkeypatch):
    """Import the physical module against a tiny Extension API test double."""
    class NFType(Enum):
        FLOAT = "FLOAT"
        INT = "INT"
        VECTOR = "VECTOR"
        BOOL = "BOOL"
        GEOMETRY = "GEOMETRY"
        STRING = "STRING"
        BUNDLE = "BUNDLE"

    @dataclass(frozen=True)
    class ExtensionBackendValue:
        socket: object
        typ: NFType

    extension = ModuleType("NodeForge.extension_api")
    extension.ExtensionBackendValue = ExtensionBackendValue
    extension.NFType = NFType
    monkeypatch.setitem(sys.modules, "NodeForge", ModuleType("NodeForge"))
    monkeypatch.setitem(sys.modules, "NodeForge.extension_api", extension)

    spec = importlib.util.spec_from_file_location(
        "_nodeforge_math_explicit_operations_test",
        ROOT / "systems" / "math" / "operations.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, NFType, ExtensionBackendValue


class FakeGroup:
    """Record the public Blender calls used by ShaderNodeMath realization."""

    def __init__(self):
        self.created = []
        self.connected = []
        self.nodes = SimpleNamespace(new=self.new_node)
        self.links = SimpleNamespace(new=self.connect)

    def new_node(self, node_type):
        node = SimpleNamespace(
            bl_idname=node_type,
            operation=None,
            inputs=[object(), object()],
            outputs=[object()],
            location=(0, 0),
        )
        self.created.append(node)
        return node

    def connect(self, output_socket, input_socket):
        self.connected.append((output_socket, input_socket))


@pytest.mark.parametrize("name,opcode", list(UNARY_OPERATIONS.items()) + list(BINARY_OPERATIONS.items()))
def test_math_wrapper_creates_expected_blender_operation(operations, name, opcode):
    """Every callable emits the configured Math node and wires inputs in order."""
    module, NFType, BackendValue = operations
    group = FakeGroup()
    context = SimpleNamespace(
        group=group,
        location=(30, 40),
        value=lambda socket, typ: BackendValue(socket, typ),
    )
    count = 1 if name in UNARY_OPERATIONS else 2
    inputs = [BackendValue(object(), NFType.FLOAT) for _ in range(count)]

    result = getattr(module, f"{name}_node")(context, *inputs)

    assert len(group.created) == 1
    node = group.created[0]
    assert node.bl_idname == "ShaderNodeMath"
    assert node.operation == opcode
    assert node.location == (30, 40)
    assert group.connected == [(value.socket, node.inputs[i]) for i, value in enumerate(inputs)]
    assert result == BackendValue(node.outputs[0], NFType.FLOAT)


@pytest.mark.parametrize("name", ["sin", "min"])
def test_math_wrapper_rejects_untyped_runtime_value(operations, name):
    """The shared input validator remains active for unary and binary wrappers."""
    module, _, _ = operations
    context = SimpleNamespace(group=FakeGroup(), location=(0, 0))
    values = ("raw value",) if name == "sin" else ("raw value", "raw value")
    with pytest.raises(TypeError, match="ExtensionBackendValue"):
        getattr(module, f"{name}_node")(context, *values)


def test_all_public_operations_resolve_to_explicit_definitions():
    """The interface names each implementation through a discoverable def statement."""
    interface_ast = ast.parse((ROOT / "systems" / "math" / "interface.py").read_text())
    operations_ast = ast.parse((ROOT / "systems" / "math" / "operations.py").read_text())
    extension_table = next(
        ast.literal_eval(stmt.value)
        for stmt in interface_ast.body
        if isinstance(stmt, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "EXTENSIONS" for target in stmt.targets)
    )
    implementations = {stmt.name for stmt in operations_ast.body if isinstance(stmt, ast.FunctionDef)}

    assert len(extension_table) == 28
    assert {f"{name}_node" for name in UNARY_OPERATIONS | BINARY_OPERATIONS} <= implementations
    assert all(path.startswith(".operations:") and path.split(":")[1] in implementations
               for path in extension_table.values())
    assert "_install_operation_wrappers" not in implementations
