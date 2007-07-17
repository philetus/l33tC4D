###
### test projecting vertex onto edge
###
from l33tC4D.space.Vertex import Vertex
from l33tC4D.space.Edge import Edge

a = Vertex( 0,0,0 )
b = Vertex( 4, 0, 0 )
c = Vertex( 2,2,0 )
ab = Edge( a, b )

d = c.project( ab )

assert d.x == 2.0
assert d.y == 0.0
assert d.z == 0.0
