# Cube

`cube` is a Python toolkit for representing, manipulating, and visualizing **NxN Rubik’s Cubes**.  
It provides a programmatic cube model, standard cube rotations, state inspection, and utilities useful for simulations, solvers, and visualizations.

The library is designed to be:
- **Flexible** — supports arbitrary cube sizes
- **Explicit** — clear cubelet orientation and face mapping
- **Composable** — easy to build solvers or UIs on top


## Installation

Clone the repository and install dependencies:

```bash
pip install numpy attridict
```
## Quick Start

### Create a Cube
```python
from cube.cube import Cube

cube = Cube()        # Default 3x3 solved cube
cube2 = Cube(size=2) # 2x2 cube
```

### Initialize from a state string
```python
state = "yyyyyyyyybbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwww"
cube = Cube(size=3, state=state)
```
The state string must be exactly 6 × size² characters long.


## Cube State Representation

The cube state is stored internally as a flat string in this face order:
```
U L F R B D
```

Each face is written row-by-row.


### Color encoding

| Letter | Color  |
| ------ | ------ |
| y      | Yellow |
| w      | White  |
| r      | Red    |
| o      | Orange |
| b      | Blue   |
| g      | Green  |


## Visualizing the Cube
```python
print(cube)
```

Example output (3×3):
```python
    |yyy|
    |yyy|
    |yyy|
|bbb|rrr|ggg|ooo|
|bbb|rrr|ggg|ooo|
|bbb|rrr|ggg|ooo|
    |www|
    |www|
    |www|
```

## Performing Rotations
### Using Standard Notation
```python
cube.rotate("u")
cube.rotate("r'")
cube.rotate("f2")
```

Supported notation:

- `U, D, L, R, F, B` - clockwise
- `'` - counter-clockwise
- `2` - double turn

## Multiple Moves
```python
cube.rotate("r u r' u'")
```

Moves are space-separated, case-insensitive.


## Direct Rotation Methods

Each face has a corresponding method:

```python
cube.rotate_u()
cube.rotate_d()
cube.rotate_l()
cube.rotate_r()
cube.rotate_f()
cube.rotate_b()
```

With parameters:

```python
cube.rotate_u(times_to_move=2)      # U2
cube.rotate_r(times_to_move=-1)     # R'
cube.rotate_f(index_to_move=1)      # Inner slice (NxN)
```

## Whole-Cube Rotations

Rotate the entire cube along an axis:
```python
cube.rotate_all_u()
cube.rotate_all_r(times_to_move=2)
cube.rotate_all_f(times_to_move=-1)
```

Useful for changing cube orientation without altering relative state.

## Checking if the Cube Is Solved
```python
cube.solved()
```
Returns True if all faces are uniform (orientation-independent).


## Move History

Every rotation is recorded:
```python
cube.path
```
Example:
```python
[('r', 1), ('u', 1), ('r', 3), ('u', 3)]
```

Equality between cubes (`cube1 == cube2`) compares state only, not move history.

## Copying a Cube
```python
cube_copy = cube.copy()
```

Creates a deep copy, so the two cubes are completely independent.

## Accessing Faces Programmatically

You can extract faces using:
```python
faces = cube.group_sides()
```

Returns a dictionary:
```python
{
  "u": [...],
  "d": [...],
  "l": [...],
  "r": [...],
  "f": [...],
  "b": [...]
}
```
Each face is a 2D array of color letters.

## Cubelets
Internally, the cube is made of Cubelets, each tracking its orientation:
```python
cube.cube[x][y][z].pos
```

Example cubelet position:
```python
{
  "u": "yellow",
  "d": None,
  "l": "blue",
  "r": None,
  "f": "red",
  "b": None
}
```

This makes the library suitable for:
- Solver development
- Accurate 3D renderering
- State validation
- Algorithm analysis

## Constants & Utilities
### Slice Helpers

The `SLICE` utility abstracts NumPy slicing:
```python
from cube.constants import SLICE

cube.cube[SLICE.U(0)]  # Top slice
cube.cube[SLICE.F(1)]  # Inner front slice
```
## Example: Simple Scramble
```python
cube = Cube()
cube.rotate("r u r' u'")
print(cube)
```
## Example: Random Scramble
```python
import random

moves = ["u", "u'", "u2", "r", "r'", "r2", "f", "f'", "f2"]
scramble = " ".join(random.choice(moves) for _ in range(20))

cube.rotate(scramble)
```

## License
MIT License
