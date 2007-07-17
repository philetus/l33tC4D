from Vertex import Vertex

class Space( object ):
    """node in an octree covering an area of 3d space

       provides quick interference calculations for things like selection
       and collision detection 
    """

    def __init__( self, parent=None, centroid=(0.0, 0.0, 0.0), size=2.0**10 ):
        self.centroid = Vertex( *centroid )
        self.size = size

        # parent space node
        self.parent = parent

        # set of zones contained by this space node
        self.zones = set()

        # list of child nodes addressed in binary - zyx
        self.children = None

    def __repr__( self ):
        return "<space x=%.2f y=%.2f z=%.2f size=%.2f/>" % (
            tuple(self.centroid) + (self.size,) )

    def print_tree( self, _indent=0 ):
        print "  " * _indent + "*" + str(self)
        for zone in self.zones:
            print "  " * _indent + " " + str(zone)
        if self.children is not None:
            for space in self.children:
                space.print_tree( _indent=_indent+1 )

    def insert( self, zone, limit=2.0**1 ):
        """insert a new zone into octree

           will descend tree until smallest containing space node is reached
           or size limit is reached

           throws a Collision_Exception if new zone would intersect with
           existing zone
        """
        # if this space node has no children spawn some
        if self.children is None:
            self.spawn()

        # if only one child intersects this zone, insert into that child,
        # otherwise add to this space's contained set
        child = None
        for space in self.children:
            if zone.interfere( space=space ) is not None:

                # if this is not first child space zone intersects, the
                # current space is the smallest containing space node
                if child is not None:
                    self._add_zone( zone )
                    return
                
                child = space

        # if the size limit has not been reached insert into containing
        if self.size > limit:
            child.insert( zone=zone, limit=limit )
            return

        # if size limit has been reached just add zone to this space
        self._add_zone( zone )

    def _add_zone( self, zone ):
        """private method to manage adding zone to space node
        """
        assert zone.space is None
        zone.space = self
        self.zones.add( zone )

    def remove( self, zone ):
        """remove given zone from space octree
        """
        if zone.space is None:
            raise KeyError( "zone not in space octree!" )

        # remove zone from space node's contained set
        zone.space.zones.remove( zone )

        # set zone's containing space to none
        zone.space = None
        
    def interfere( self, zone, limit=1.0, _baggage=set() ):
        """returns zones kissing and intersecting given zone down to size limit

           stops recursively interfering when space node of given size is
           reached

           returns: tuple( set(<kissing zones>), set(<intersecting zones>) )
        """
        kisses = set()
        intersects = set()
        
        # interfere this space with given zone
        zone_interference = zone.interfere( space=self )

        # if zone does not intersect or contain this space return empty sets
        if zone_interference is None:
            return kisses, intersects

        # if zone contains this space add all zones contained by this space and
        # its child spaces to the current intersection set
        if zone_interference:
            intersects |= self.zones | self.get_child_zones()

            # if any zones in baggage intersect or contain this space add
            # them to intersection set
            for z in _baggage:
                if z.interfere( space=self ) is not None:
                    intersects.add( z )
                    
            return kisses, intersects

        # otherwise zone intersects this space
        # calculate which baggage zones intersect or contain this space
        forward_baggage = set()
        for z in _baggage:
            z_interference = z.interfere( space = self )
            if z_interference is not None:

                # if baggage zone intersects this space add it to forward
                # baggage set to test against child spaces
                if not z_interference:
                    forward_baggage.add( z )

                # otherwise baggage zone contains this space, add it to
                # intersection set
                else:
                    intersects.add( z )                    
        
        # if size limit has not been reached interfere each child space with
        # this space's contained zones and forward baggage as baggage, and
        # union returned sets
        if self.size > limit:

            # if space node has no children spawn some
            if self.children is None:
                self.spawn()
                
            for space in self.children:
                k, i = space.interfere( zone=zone, limit=limit,
                                        _baggage=self.zones | forward_baggage )
                kisses |= k
                intersects |= i

            return kisses, intersects

        # otherwise size limit has been reached, add any forward baggage and
        # zones contained by this space and its children to kissing set
        # and return
        kisses |= self.zones | self.get_child_zones() | forward_baggage
        return kisses, intersects
        

    def get_child_zones( self ):
        """returns set of all zones contained by this space's children

           does *not* include zones contained by this space
        """
        zones = set()
        if self.children is not None:
            for space in self.children:
                zones |= space.zones | space.get_child_zones()
        return zones

    def spawn( self ):
        """generate a set of child space nodes for this node

           children are encoded in binary 0 for positive and 1 for negative,
           zyx
        """
        assert self.children is None
        self.children = []

        size = self.size / 2.0
        radius = size / 2.0

        for z in [-1, 1]:
            for y in [-1, 1]:
                for x in [-1, 1]:
                    delta = Vertex( *[a * radius for a in x, y, z] )
                    centroid = self.centroid + delta
                    space = Space( parent=self, centroid=centroid, size=size )
                    self.children.append( space )
                        
    def prune( self ):
        """prune empty nodes from space octree
        """
        if self.children is None:
            return
        
        # recursively prune from bottom up
        for space in self.children:
            space.prune()

        # if all child nodes are empty remove them all
        for space in self.children:
            if not space.is_empty():
                return

        self.children = None
        
    def is_empty( self ):
        """returns true if space contains no zones and has no children
        """
        if self.children is None and len(self.zones) < 1:
            return True
        
        return False            
        
