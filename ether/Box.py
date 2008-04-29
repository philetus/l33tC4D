from l33tC4D.vector.Vector3 import Vector3
from Zone import Zone

class Box( Zone ):
    """a solid box that can be inserted into ether
    """
    SOLID = True
    VISIBLE = True
    
    def __init__( self, position=(0,0,0), size=2, color=(0,0,1,1) ):
        Zone.__init__( self )

        self.position = Vector3( position )
        self.size = float( size )

    def __repr__( self ):
        return "<box (%.1f %.1f %.1f) %.2f>" % ( tuple(self.position)
                                              + (self.size,) )

    def get_bounds( self ):
        """return (min, max) coords containing this zone
        """
        r = self.size / 2.0
        return tuple( tuple(p + (d * r) for p in self.position)
                      for d in (-1, 1) )

    def intersect( self, position, radius ):
        """determine whether this zone intersects given box

           -> ( (<zone>, <intersection>, <normal>), ... )

           returns a list of tuples for each intersecting (sub-)zone:
               <zone> intersecting (sub-)zone
               <intersection> contained|contains|crosses|clips
               <normal> (u, v, w) coords given if zone clips box into two
        """
        bmin, bmax = self.get_bounds()
       
        # check whether each coord is inside or outside
        outside = False
        insides = []
        for i, bound, d in ( (0, bmin, -1), (1, bmax, 1) ):

            for j, p, b in zip( range(3), position, bound ):
                dist = (p - b) * d

                # if min is bigger than radius or max is smaller than radius
                # this box doesn't intersect given bound, return empty tuple
                if dist > radius:
                    return ()

                if dist < -radius:
                    outside = True
                else:
                    insides.append( (i,j) )

        # if no bounds are outside this box is contained by given box
        if not outside:
            return ((self, self.CONTAINED, None),)

        # if no bounds are inside this box contains given box
        if not insides:
            return ((self, self.CONTAINS, None),)

        # if there is only one bound inside given box this box clips it,
        # calculate normal
        if len(insides) == 1:
            i, j = insides[0]
            normal = [0.0, 0.0, 0.0]
            normal[j] = 1.0 if i else -1.0
            return ((self, self.CLIPS, tuple(normal)),)

        # otherwise this box crosses given box
        return ((self, self.CROSSES, None),)
                

