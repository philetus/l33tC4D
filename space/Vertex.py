from l33tC4D.vector.Vector3 import Vector3

from Zone import Zone

class Vertex( Vector3, Zone ):
    """a point in 3d space
    """

    def __init__( self, *coords ):
        assert len( coords ) == 3
        Vector3.__init__( self, *coords )
        Zone.__init__( self, min_vertex=self, max_vertex=self )

        
    def __repr__( self ):
        return "<vertex x=%.2f y=%.2f z=%.2f />" % tuple( self._coords )
