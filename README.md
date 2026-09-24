# NodeForge Math

NodeForge Math is an installable package for the [NodeForge](https://github.com/denikryt/NodeForge) Blender add-on. It adds typed, compiler-backed math operations such as `sin()`, `cos()`, `sqrt()`, `clamp()`, `select()`, `noise()`, and `random_value()`, along with reusable `.nf` functions and example scripts.

## Compatibility

NodeForge Math 2.1 is compatible with NodeForge 0.59.0. Because the package contains executable Python extensions, Python permission must be enabled when it is imported.

## Installation

1. Install NodeForge 0.59.0.
2. Download `nodeforge.math-v<version>.zip` from the [NodeForge Math releases](https://github.com/denikryt/nodeforge.math/releases).
3. In Blender, open the **Geometry Nodes Editor** and press `N` to show its sidebar.
4. Open the **NodeForge** tab and find the **Packages** section.
5. Enable **Allow executable Python**.
6. Click **Import** and select the downloaded ZIP file.

The package's math operations, reusable functions, and examples become available after the import completes.

## Package contents

- `systems/math` provides the typed math operations available to NodeForge source.
- `functions` contains reusable `.nf` functions for interpolation, remapping, point layouts, rotations, and other common tasks.
- `examples` contains complete NodeForge scripts demonstrating procedural setups such as terrain, spirals, trusses, contours, and fractals.

## Development notes

The Math system uses NodeForge extension API v2. Its public signatures are declared in `systems/math/interface.py`, while `systems/math/operations.py` builds their Geometry Nodes representation through `NodeForge.extension_api` and Blender's public node-tree API.

The `examples/mandelbrot` example retains its hybrid NodeForge/Python layout because it creates or modifies a Blender material. It is separate from the backend-only Math system migration.

## Documentation

See the [NodeForge documentation](https://denikryt.github.io/NodeForgeDocs/) for language guides and package usage.

## Support the developer

Support NodeForge development on [Patreon](https://www.patreon.com/c/nachitima).
