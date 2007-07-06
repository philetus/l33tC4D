
class Zone( object ):
    """superclass for phenomena that can be placed in octree of space nodes
    """

    def __init__( self, min_vertex, max_vertex ):
        """
        """
        # bounds is a list of min, max vertices
        self.bounds = [ min_vertex, max_vertex ]

        # selected flag indicates if zone is part of current selection set
        self.selected = False

        # hovered flag indicates if zone is under pointer
        self.hovered = False

    def interfere( self, space ):
        """determines if this zone intersects or contains given space

           returns true if zone contains space
           returns false if zone intersects given space
           otherwise returns none
        """
        # default - use bounds
        if self.bounds_contain_space( space ):
            return True

        if self.bounds_intersect_space( space ):
            return False

        return None

    def bounds_contain_space( self, space ):
        """returns true if this zone's bounding box contains given space
        """
        radius = space.size / 2.0

        # check that min bounds are not greater than min space coords
        for minb, mins in zip( self.bounds[0],
                               [c - radius for c in space.centroid] ):
            if minb > mins:
                return False

        # check that max bounds are not less than max space coords
        for maxb, maxs in zip( self.bounds[1],
                               [c + radius for c in space.centroid] ):
            if maxb < maxs:
                return False

        return True

    def bounds_intersect_space( self, space ):
        """returns true if this zone's bounding box intersects given space
        """
        radius = space.size / 2.0

        # if max space coord is less than min bound or min space coord is
        # greater than max bound return false
        for d, vertex in zip( [-1, 1], self.bounds ):
            for coord, bound in zip( space.centroid, vertex ):
                if (bound - (coord - (radius * d))) * d < 0:
                    return False

        return True
