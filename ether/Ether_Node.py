from l33tC4D.vector.Vector3 import Vector3
from Shadow_Node import Shadow_Node

class Ether_Node:
    """a node in a sparse tree filling occupied space
    """
    CONTAINED, CONTAINS, CROSSES, CLIPS = 0, 1, 2, 3
    SIZE = 3 # radius of scale 1 node

    def __init__( self, demon, parent=None, name=(0, 0, 0),
                  position=(0, 0, 0), scale=0 ):
        self.demon = demon # ether demon managing this ether node
        self.parent = parent # ether node containing this node
        self.name = name # relative position of this node to parent
        self.position = Vector3( position )
        self.scale = scale

        # coord relative to top node, generated on demand
        self._coord = None

        # child nodes indexed by name (x,y,z)
        self.children = {}

        # shadow nodes in this ether node indexed by zone
        self.shadows = {}

    def __repr__( self ):
        return "<ether node (%.2f %.2f %.2f) %d>" % ( tuple(self.position)
                                                 + (self.scale,) )

    def __getitem__( self, name ):
        """return child with given name, spawn it if it doesn't exist
        """
        # if child with given name does not exist build it
        if name not in self.children:
            scale = self.scale - 1
            diameter = 2.0 * (self.SIZE ** scale)
            position = tuple( p + (n * diameter) for p, n
                              in zip(self.position, name) )
            child = Ether_Node( demon=self.demon, parent=self, name=name,
                                position=position, scale=scale )
            self.children[name] = child

        return self.children[name]

    def __contains__( self, name ):
        return name in self.children

    def __iter__( self ):
        return self.children.itervalues()

    ###
    ### public ether node interface should only be accessed by its demon
    ###

    def get_coord( self ):
        """return coord of this ether node relative to top node
        """
        # if coord is not set build it from parent coord
        if self._coord is None:
            if self.parent is None:
                self._coord = ()
            else:
                self._coord = self._next_coord( self.parent.get_coord(),
                                                self.name )

        return self._coord
        
    def insert( self, shadow ):
        """insert given zone shadow into ether tree
        """
        # if this shadow is not solid just insert it here
        if not shadow.zone.SOLID:
            shadow_node = Shadow_Node( shadow=shadow,
                                       ether=self,
                                       zone=shadow.zone,
                                       intersection=self.CONTAINED )
            shadow.nodes[tuple] = shadow_node
            self.shadows[shadow.zone] = shadow_node

            return True

        # otherwise attempt to insert solid
        return self._insert_solid( shadow=shadow,
                                   zone=shadow.zone,
                                   intersection=self.CONTAINED )

    def _insert_solid( self, shadow, zone, intersection, normal=None ):
        print "\ninserting %s into ether at %s" % (str(zone), str(self.get_coord()) )

        # check for intersecting shadows:
        intersecting_shadows = self.find_shadows(
            solid=True, test=shadow.zone.ignore_intersection )

        # if any of the intersecting shadows contain this node this
        # shadow collides with it, fail
        for intersecting_shadow in intersecting_shadows:
            if intersecting_shadow.intersection == self.CONTAINS:
                return False

        # if this shadow contains this ether node and there is another
        # intersecting shadows this shadow collides with it, fail
        if intersection == self.CONTAINS and intersecting_shadows:
            return False

        # if there are no intersecting shadows or we have reached resolution
        # limit without discovering a collision just make shadow node here
        if( (not intersecting_shadows)
            or self.scale == self.demon.COLLISION_RESOLUTION ):

            shadow_node = Shadow_Node( shadow=shadow,
                                       ether=self,
                                       zone=zone,
                                       intersection=intersection,
                                       normal=normal )
            shadow.nodes.add( shadow_node )
            self.shadows[zone] = shadow_node

            print "halting descent"

            return True

        print "descending"

        # otherwise push other solid shadows in this ether node
        push_shadows = [
            node for node in self.shadows.itervalues()
            if node.zone.SOLID and not zone.ignore_intersection(node.zone) ]
        
        while push_shadows:
            self._push_shadow( push_shadows.pop() )

        # then find children that intersect bounds and test them against zone,
        # return false if any child insertions fail
        for name, position, radius in self.iter_bounded_children(
            *zone.get_bounds() ):

            # insert each sub zone returned by zone intersection test
            # into child, and return false if insert fails
            for z, i, n in zone.intersect( position, radius ):
                child = self[name]
                if not child._insert_solid( shadow=shadow,
                                            zone=z,
                                            intersection=i,
                                            normal=n ):
                    return False

        return True

    def _push_shadow( self, shadow_node ):
        """resolve shadow down into children of this node
        """        
        shadow = shadow_node.shadow
        
        print "pushing shadow:", str(shadow)
        
        # find children touching shadow node's zone's bounds and test
        # each child's bounding box for intersection with zone
        for name, position, radius in self.iter_bounded_children(
            *shadow_node.zone.get_bounds() ):

            # make shadow node in child for each sub-zone returned 
            for zone, intersection, normal in shadow_node.zone.intersect(
                position, radius ):

                child_node = Shadow_Node( shadow=shadow,
                                          ether=self[name],
                                          zone=zone,
                                          intersection=intersection,
                                          normal=normal )
                shadow.nodes.add( child_node )
                self[name].shadows[zone] = child_node

        # remove shadow node from this ether node and parent shadow
        self.purge_shadow_node( shadow_node )

    def purge_shadow_node( self, shadow_node ):
        """remove a child node from ether and from self
        """
        # check that node belongs to this shadow and its purported ether
        shadow = shadow_node.shadow
        zone = shadow_node.zone
        
        #print "ether:", str(shadow_node.ether), str(self)
        #print "zone:", str(zone), str(self.shadows.keys())
        #print "node:", str(shadow_node), str(self.shadows[zone])
        
        if not( shadow_node.ether is self
                and zone in self.shadows
                and self.shadows[zone] is shadow_node ):
            raise AssertionError( "can't purge shadow node, doesn't match!" )
        
        # remove from shadow
        shadow.nodes.discard( shadow_node )

        # remove from ether
        del self.shadows[zone]

    def find_shadows( self, solid=False, test=None ):
        """find all of the shadow nodes intersecting this ether node
        """
        # get list of children's shadow nodes
        shadow_list = []
        self._get_shadows( shadow_list, solid )

        # if there is no test given just return shadow nodes
        if test is None:
            return set( shadow_list )

        # if test is given filter shadow nodes
        shadow_set = set()
        for node in shadow_list:
            if not test( node.zone ):
                shadow_set.add( node )
                    
        return shadow_set

    def _get_shadows( self, shadow_list, solid=False ):
        
        # add shadow nodes to list
        shadow_list.extend(
            node for node in self.shadows.itervalues()
            if node.zone.VISIBLE and ((not solid) or node.zone.SOLID) )

        # collect children's nodes too
        for child in self:
            child._get_shadows( shadow_list, solid )
        

    def iter_bounded_children( self, bmin, bmax ):
        """iterate over the name, position and radius of bounded children
        """
        radius = self.SIZE ** (self.scale - 1)
        for name in self.get_bounded_children( bmin, bmax ):
            position = tuple( p + (2 * n * radius) for p, n
                              in zip(self.position, name) )
            yield (name, position, radius)
        
    def update_shadow_coords( self, coord=None ):
        """update coords of shadow nodes when top ether node changes
        """
        raise NotImplementedError()

    def get_bounded_children( self, bmin, bmax ):
        """calculate which children intersect given bounds

           -> <name_set> with names of intersecting children
        """
        child_radius = float(self.SIZE ** (self.scale - 1))
        
        # convert coordinate bounds to name bounds
        nmin, nmax = [], []
        for coord_bound, named_bound, d in ((bmin, nmin, -1), (bmax, nmax, 1)):
            for b, p in zip( coord_bound, self.position ):

                # calculate distance from center of node in child radii
                radii = (b - p) / child_radius

                # if radii does not overlap ether node return empty set
                if radii * d <-3:
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

    def _next_coord( self, coord, name ):
        """add name onto coord
        """
        # squish coord into a single number <0-26>
        c = 0
        for i, n in zip( (3, 2, 1), name ):
            c += i * (n + 1)

        return coord + (c,)

    def wipe_coords( self ):
        """clear cached coords
        """
        self._coord = None
        for child in self.children:
            child.wipe_coords()
        
    def remove( self, zone ):
        """remove given zone from ether tree
        """
        raise NotImplementedError()
