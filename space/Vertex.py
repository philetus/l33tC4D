from l33tC4D.vector.Vector3 import Vector3

from Zone import Zone

class Vertex( Vector3, Zone ):
    """a point in 3d space
    """

    def __init__( self, x, y, z ):
        Vector3.__init__( self, x=x, y=y, z=z )
        Zone.__init__( self, min_vertex=self, max_vertex=self )

        
    def __repr__( self ):
        return "<vertex x=%.2f y=%.2f z=%.2f />" % tuple( self._coords )

    def interfere( self, space ):
        """determines if this zone intersects or contains given space

           returns true if zone contains space
           returns false if zone intersects given space
           otherwise returns none
        """
        # vertex never contains anything, just check for intersection
        if self.bounds_intersect_space( space ):
            return False

        return None

    def distance( self, vertex ):
        """returns distance from this vertex to another vertex
        """
        d = self - vertex
        return d.magnitude

    def project( self, edge ):
        """returns new vertex projected onto given edge
        """
        leg = Vector3( *(self - edge[0]) )
        base = Vector3( *(edge[1] - edge[0]) )
        t = leg.project( base )
        delta = t + (edge[0] - self)
        return self + delta
        
