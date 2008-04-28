from l33tC4D.vector.Vector3 import Vector3

class Ether:
    """a node in a sparse tree filling occupied space
    """
    CONTAINED, CONTAINS, CROSSES, CLIPS = 0, 1, 2, 3
    SIZE = 3 # radius of scale 1 node

    def __init__( self, demon, parent=None, position=(0, 0, 0), scale=0 ):
        self.demon = demon # ether demon managing this ether node
        self.parent = parent # ether node containing this node
        self.position = position
        self.scale = scale
        self.children = {} # child nodes indexed by name (x,y,z)
        self.shadows = {} # nets in this ether indexed by zone
        self.contained = set() # set of zones containing this ether

    def bounded_children( self, bmin, bmax ):
        """calculate which children intersect given bounds

           -> <name_set> with names of intersecting children
        """
        child_radius = float(self.SIZE ** (self.scale - 1))
        
        # convert coordinate bounds to name bounds
        nmin, nmax = [], []
        for coord_bound, named_bound, d in ((bmin, nmin, -1), (bmax, nmax, 1)):
            for b, p in zip( coord_bound, self.position ):

                # calculate distance from center of node in child radii
                radii = (v - p) % child_radius

                # if radii does not overlap ether node return empty set
                if radii * d < -3:
                    return set()

                # determine whether coord is in center or perimiter
                if abs(radii) <= 1:
                    named_bound.append( 0 )
                elif radii < 0:
                    named_bound.append( -1 )
                else:
                    named_bound.append( 1 )

        # build set of nodes intersecting bounding box
        name_set = set()
        for u in range( nmin[0], nmax[0] + 1 ):
            for v in range( nmin[1], nmax[1] + 1 ):
                for w in range( nmin[2], nmax[2] + 1 ):
                    name_set.add( (u, v, w) )

        return name_set

    def contains_bounds( self, bmin, bmax ):
        """returns true if this node contains given bounds
        """
        radius = self.SIZE ** self.scale
        for bound in bmin, bmax:
            for b, p in zip( bound, self.position ):
                if abs( b - p ) > radius:
                    return False

        return True                

    def get_nets( self ):
        """return dictionary of sets of contained nets indexed by zone 
        """
        nets = {}
        for zone, net in self.nets.iteritems():
            nets[zone] = set([net])

        for child in self.children.itervalues():
            for zone, net_set in child.get_nets.iteritems():
                if not zone in nets:
                    nets[zone] = set()
                nets[zone] |= net_set

        return nets

    def get_zones( self ):
        """returns set of all zones touching this ether node
        """
        zones = set( self.nets.iterkeys() ) | self.contained
        for child in self.children.itervalues():
            zones |= child.get_zones()

        return zones

    def insert( self, zone ):
        """insert given zone into ether tree

           when intersections are encountered, query both zones to
           determine whether to continue resolution
        """
        # get bounds
        mn, mx = zone.get_bounds()

        # while top ether does not contain zone bounds grow tree
        top = self._get_top()
        while not top._contains( mn, mx ):
            self._spawn_top()
            top = self.get_top()

        # intersect zone with top node
        top._intersect( zone )
            self.parent.insert( zone )
            return

    def _intersect( self, zone ):
        ### intersect zone with tree

        # if node has 
        
    def remove( self, zone ):
        """remove given zone from ether tree
        """
