from Zone import Zone
from Vertex import Vertex

class Edge( Zone ):
    """a line in space connecting two vertices
    """

    def __init__( self, vertex_a, vertex_b ):
        self.vertices = [ vertex_a, vertex_b ]
        
        Zone.__init__( self, *self.generate_bounds() )

    def generate_bounds( self ):
        """return min, max bounds as vertices
        """
        min_bound = [ min(a, b) for a, b in zip(*self.vertices) ]
        max_bound = [ max(a, b) for a, b in zip(*self.vertices) ]
        return Vertex( *min_bound ), Vertex( *max_bound )

    def __getitem__( self, index ):
        return self.vertices[index]

    def interfere( self, space ):
        """determines if this zone intersects or contains given space

           returns true if zone contains space (never happens)
           returns false if zone intersects given space
           otherwise returns none

           *lazy* - actually tests against sphere with diameter of space
           size rather than cube
        """
        # test if ends of edge are within radius of space centroid
        radius = space.size * 0.8660254037844386 # sqrt(3) / 2
        for end in self.vertices:
            if end.distance( space.centroid ) <= radius:
                return False
        
        # then project centroid onto edge and test if distance is less than
        # radius
        closest = space.centroid.project( edge=self )
        if closest.distance( space.centroid ) > radius:
            return None            

        # if it is test that distance between edges is greater than distance
        # from projected point to either edge
        between = self[0].distance( self[1] )
        for end in self.vertices:
            if end.distance( closest ) >= between:
                return None

        return False
