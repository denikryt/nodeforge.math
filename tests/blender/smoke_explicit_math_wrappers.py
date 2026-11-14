"""Blender 5.2 smoke test for all explicit Math Extension API v2 ShaderNodeMath wrappers."""

import ast
import importlib.util
import os
from pathlib import Path
import sys

import bpy

SOURCE_ROOT = Path(__file__).resolve().parents[2]
if os.environ.get("NODEFORGE_SOURCE"):
    sys.path.insert(0, os.environ["NODEFORGE_SOURCE"])

from NodeForge.extension_api import ExtensionBackendContext, ExtensionBackendValue, NFType

spec = importlib.util.spec_from_file_location("nodeforge_math_test_operations", SOURCE_ROOT / "systems/math/operations.py")
operations = importlib.util.module_from_spec(spec)
spec.loader.exec_module(operations)

interface_tree = ast.parse((SOURCE_ROOT / "systems/math/interface.py").read_text())
lookup = next(ast.literal_eval(s.value) for s in interface_tree.body
              if isinstance(s, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'EXTENSIONS' for t in s.targets))
assert len(lookup) == 28

unary = ('sin','cos','tan','asin','acos','atan','sqrt','abs','floor','ceil','round','fract','radians','degrees','exp')
binary = ('min','max','pow','log','atan2','mod')
operations_lookup = {
    'sin':'SINE','cos':'COSINE','tan':'TANGENT','asin':'ARCSINE','acos':'ARCCOSINE',
    'atan':'ARCTANGENT','sqrt':'SQRT','abs':'ABSOLUTE','floor':'FLOOR',
    'ceil':'CEIL','round':'ROUND','fract':'FRACT','radians':'RADIANS',
    'degrees':'DEGREES','exp':'EXPONENT', 'min':'MINIMUM','max':'MAXIMUM',
    'pow':'POWER','log':'LOGARITHM','atan2':'ARCTAN2','mod':'MODULO',
}

tree = bpy.data.node_groups.new('Math explicit wrapper regression', 'GeometryNodeTree')
source = tree.nodes.new('ShaderNodeValue')
source.outputs[0].default_value = 0.5
value = ExtensionBackendValue(source.outputs[0], NFType.FLOAT)

for index, name in enumerate(unary + binary):
    context = ExtensionBackendContext(group=tree, location=(index * 120., 0.), generated_resource_transaction=object())
    before = {n.as_pointer() for n in tree.nodes}
    method = getattr(operations, lookup[name].split(':')[1])
    result = method(context, value) if name in unary else method(context, value, value)
    created = [n for n in tree.nodes if n.as_pointer() not in before]
    assert len(created) == 1, (name, created)
    new = created[0]
    assert new.bl_idname == 'ShaderNodeMath' and new.operation == operations_lookup[name]
    assert result.typ == NFType.FLOAT and result.socket == new.outputs[0]
    for socket in new.inputs[:(1 if name in unary else 2)]:
        assert socket.is_linked, name

assert len([n for n in tree.nodes if n.bl_idname == 'ShaderNodeMath']) == 21
assert len(tree.links) == 27
print('EXPLICIT_MATH_WRAPPERS_BLENDER_PASS', len(unary), len(binary),len(lookup))
bpy.data.node_groups.remove(tree)
