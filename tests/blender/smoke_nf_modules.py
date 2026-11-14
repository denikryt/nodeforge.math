"""Blender 5.2 integration tests for the NodeForge Math typed .nf file modules.

Run: blender -b --factory-startup --python tests/blender/smoke_nf_modules.py
The NodeForge add-on must be importable, or set NODEFORGE_SOURCE to its source parent.
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import bpy

source_parent = os.environ.get("NODEFORGE_SOURCE")
if source_parent:
    sys.path.insert(0, source_parent)

from NodeForge import compiler, packages  # noqa: E402
from NodeForge.errors import CompileError  # noqa: E402

root = Path(__file__).resolve().parents[2]
packages.set_packages_dir_for_tests(Path(tempfile.mkdtemp(prefix="nf_math_pkgs_")))
record = packages.install_package_directory(root)
assert record.package_id == "nodeforge.math"
assert record.version == "2.3"


def _compose(label, source):
    """Compile into a new root, requiring a materialized Group Node."""
    tree = bpy.data.node_groups.new(label, "GeometryNodeTree")
    compiler.compose_source_initial(source, tree)
    groups = [node for node in tree.nodes if node.bl_idname == "GeometryNodeGroup"]
    assert len(groups) == 1, (label, [n.bl_idname for n in tree.nodes])
    assert groups[0].node_tree is not None
    return tree, groups[0].node_tree


for path in sorted((root / "functions").glob("*.nf")):
    required_geometry = path.stem in {
        "copy_by_offsets", "layout_circle", "layout_grid", "layout_spiral",
        "layout_random", "sierpinski_carpet",
    }
    call = f"math.{path.stem}(" + ("cube(1.0)" if required_geometry else "") + ")"
    _compose("Function " + path.stem, "from packages import math\nvalue = " + call + "\n")
    print("FUNCTION PASS", path.stem, flush=True)

for path in sorted((root / "examples").glob("*.nf")):
    _compose("Example " + path.stem, path.read_text(encoding="utf-8"))
    print("EXAMPLE PASS", path.stem, flush=True)

# Extension API v2 remains callable from a nested typed function.
_, nested = _compose(
    "Physical nested extension", "from packages import math\n"
    "def use_sine(x: Float = 0.5) -> Float:\n    return math.sin(x)\n"
)
assert any(node.bl_idname == "ShaderNodeMath" and node.operation == "SINE"
           for node in nested.nodes)

_, pingpong = _compose("Pingpong", "from packages import math\nvalue = math.pingpong(1.0)\n")
assert [s.name for s in pingpong.interface.items_tree if s.item_type == "SOCKET" and s.in_out == "INPUT"] == ["X", "Length"]

_, random_points = _compose(
    "Random points", "from packages import math\n"
    "value = math.random_points(12, min_value=vector(-1,-1,-1), max_value=vector(1,1,1))\n"
)
assert any(node.bl_idname == "GeometryNodeGroup" for node in random_points.nodes)

# Qualified file imports use the same export identities as a normal package import.
root_tree = bpy.data.node_groups.new("Update eligible", "GeometryNodeTree")
old_ptr = root_tree.as_pointer()
compiler.update_source_in_tree("from packages import math\nvalue = math.smoothstep(0.0,1.0,0.5)", root_tree)
assert root_tree.as_pointer() == old_ptr
assert len([n for n in root_tree.nodes if n.bl_idname == "GeometryNodeGroup"]) == 1
compiler.update_source_in_tree("from packages import math\nvalue = math.saturate(0.25)", root_tree)
assert root_tree.as_pointer() == old_ptr
assert len([n for n in root_tree.nodes if n.bl_idname == "GeometryNodeGroup"]) == 1

# The existing physical Extension API root restriction is intentionally unchanged.
raw = bpy.data.node_groups.new("Physical direct rejection", "GeometryNodeTree")
try:
    compiler.compose_source_initial("from packages import math\nvalue = math.sin(0.5)\n", raw)
except CompileError:
    assert len(raw.nodes) == 0
else:
    raise AssertionError("Direct physical Extension API execution was unexpectedly allowed")
print("MATH_MODULES_BLENDER_PASS", flush=True)
