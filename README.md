# Pentagrid

This module implements a coordinate system and navigation on the [{5,4}](https://en.wikipedia.org/wiki/Order-4_pentagonal_tiling), [{4,5}](https://en.wikipedia.org/wiki/Order-5_square_tiling) and [r{4,5}](https://en.wikipedia.org/wiki/Tetrapentagonal_tiling) tilings of the hyperbolic plane in python. It is based on the system introduced by [Margenstern](https://arxiv.org/abs/0909.2157). It might be useful for visualizations or games set in the hyperbolic plane.

## Installation

```
python setup.py install
```

If necessary, with root privileges.

## Usage

### {5,4}

The `Tile` class represent a right-angled pentagon in the order-4 pentagonal tiling (aka, {5,4}). The origin tile can be created with

```
import pentagrid as grid

origin = grid.Tile(0)
```

The five adjacent pentagons can be found with

```
adjacent = origin.adjacent()
```

which provides a list of 5 `Tile` objects.

### {4,5}

The `Vertex` class represent a vertex in the {5,4} where four pentagons meet. However, since {5,4} and {4,5} are dual, a `Vertex` is also a square in the {4,5} or order-5 square tiling. Accordingly, the `Tile` class also represents a vertex in the {4,5}.

The five vertices of a given pentagon `t` of the {5,4} (or equivalently, the five squares around a given vertex `t` of the {4,5}) can be found with the `.neighbours()` function; for example:

```
origin_pentagon = grid.Tile(0)
origin_square = origin_pentagon.neighbours()[0]
```

creates a `Vertex` (representing a square) that can be used as the origin tile for the {4,5} tiling.

The four adjacent squares can be found again with the `.adjacent()` method:

```
adjacent_squares = origin_square.adjacent()
```

### r{4,5}

Together, members of `Vertex` and `Tile` represent polygons of the r{4,5} or tetrapentagonal tiling in which squares and pentagons alternate; they indeed inherit from the `Node` class. Adjacency in the r{4,5} is given by the `.neighbours()` method of the `Node` class, which for a pentagon would give the five adjacent squares, and for a square the four adjacent pentagons. Essentially, to navigate the r{4,5}, start from the origin pentagon:

```
origin = grid.Tile(0)
```

and then navigate using `.neighbours()`:

```
origin_neighbours = origin.neighbours()
```

which is a list of four `Vertex` objects. Then again we can continue:

```
square = origin_neighbours[0]
square_neighbours = square.neighbours()
assert origin in square neighbours
```

`square_neighbours` is the list of 4 pentagons adjacent to `square`, and we verify the original pentagon is one of them.
