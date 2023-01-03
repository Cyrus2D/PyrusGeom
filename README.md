# PyrusGeom
## Geom2D | Soccer Math

PyrusGeom is a Python library for dealing with math and geometry in SS2D.


# Installation

Use the this  to install PyrusGeom.
```Bash
pip install PyrusGeom
```
or 
```sh
git clone https://github.com/Cyrus2D/PyrusGeom.git
./setup.py build
./setup.py install
```

# Usage

for importing you can use this options

import the desired class
```python
from pyrusgeom.vector_2d import Vector2D # for Vector2D
from pyrusgeom.polygon_2d import Polygon2D # for Polygon2D
```
Or use a Wildcard import like
```python
from pyrusgeom.soccer_math import *
from pyrusgeom.geom_2d import *
```

Examples

```python
vec_1 = Vector2D() # create Vector with default value.
vec_2 = Vector2D(20,30) # create Vector with 20 , 30 value directly.
line_1 = Line2D(vec1,vec2) # create line from 2 points.
circle_1 = Circle2D(3,3,5) # create circle with center point and radius value.
print(circle_1.intersection(line_1)) #  calculate the intersection with straight line.
```

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## TODO
triangulation | 
delaunay_triangulation | 
composite_region_2d | 
voronoi_diagram | 
circluar import | 
remaining eq,hash,reverse |
etc
