# NodeForge Math

NodeForge Math is an installable package for the [NodeForge](https://github.com/denikryt/NodeForge) Blender add-on. It adds typed, compiler-backed math operations such as `sin()`, `cos()`, `sqrt()`, `clamp()`, `select()`, `noise()`, and `random_value()`, along with reusable `.nf` functions and example scripts.

## Installation

1. Install a [NodeForge release](https://github.com/denikryt/NodeForge/releases) that meets the package's minimum NodeForge version.
2. Download `nodeforge.math-v<version>_nf-v<minimum-nodeforge-version>.zip` from the [NodeForge Math releases](https://github.com/denikryt/nodeforge.math/releases).
3. In Blender, open the **Geometry Nodes Editor** and press `N` to show its sidebar.
4. Open the **NodeForge** tab and find the **Packages** section.
5. Click **Install ZIP** and select the downloaded ZIP file.

The package's math operations, reusable functions, and examples become available after the import completes.

Import the package and call its functions through the package namespace:

```python
from packages import math

def evaluate(x: Float["X"] = 0.5) -> Float:
    return math.sin(x) + math.smoothstep(0.0, 1.0, x)
```

Each file under `functions/` defines one typed `.nf` function. Its filename
identifies the module, and the function name is its public package member.
For example, `functions/smoothstep.nf` declares `def smoothstep(...)` and is
called as `math.smoothstep(...)`. 

## Package contents

- `systems/math` provides the typed math operations available to NodeForge source.
- `functions` contains reusable `.nf` functions for interpolation, remapping, point layouts, rotations, and other common tasks.
- `examples` contains complete NodeForge scripts demonstrating procedural setups such as terrain, spirals, trusses, contours, and fractals.

## Compatibility

Version 2.3 requires NodeForge 0.90.2 or later and Blender 5.2 or later.

## Development notes

The Math system uses NodeForge extension API v2. Its public signatures are declared in `systems/math/interface.py`, while `systems/math/operations.py` builds their Geometry Nodes representation through `NodeForge.extension_api` and Blender's public node-tree API.

## Documentation

See the [NodeForge documentation](https://denikryt.github.io/NodeForgeDocs/) for language guides and package usage.

## Support the developer

Support NodeForge development on [Patreon](https://www.patreon.com/c/nachitima).
