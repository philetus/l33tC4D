class Zone:
    """abstract superclass for node of entity tree to be inserted into ether
    """
    # intersection codes
    CONTAINED, CONTAINS, CROSSES, CLIPS = 0, 1, 2, 3

    SOLID = False # insertion will fail if it causes two solids to intersect 
    VISIBLE = False # visible zones are returned by a get intersection call

    def __init__( self, parent=None ):
        self.parent = parent

        # tracks whether something has crossed shadow
        self.dirty_shadow = False

    def intersect( self, position, radius ):
        """determine whether this zone intersects given box

           -> ( (<zone>, <intersection>, <normal>), ... )

           returns a list of tuples for each intersecting (sub-)zone:
               <zone> intersecting (sub-)zone
               <intersection> contained|contains|crosses|clips
               <normal> (u, v, w) coords given if zone clips box into two            
        """
        raise NotImplementedError()

    def resolve_intersection( self, position, scale, shadow_set ):
        """return true to further resolve detail of intersection
        """
        if scale > self.resolution:
            return True
        
        return False

    def ignore_intersection( self, zone ):
        """return true to ignore intersection with given zone
        """
        return False

    def get_bounds( self ):
        """return (min, max) coords containing this zone
        """
        raise NotImplementedError()

    def start_motion( self, path ):
        """put zone into motion so that it occupies area swept along path
        """
        raise NotImplementedError()

    def fail_motion( self ):
        """roll zone back to state before motion

           raises assertion error if not preceded by call to start motion
        """
        raise NotImplementedError()

    def finish_motion( self ):
        """update zone to new position

           raises assertion error if not preceded by call to start motion
        """
        raise NotImplementedError()
