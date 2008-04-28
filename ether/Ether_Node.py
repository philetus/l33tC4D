from l33tC4D.vector.Vector3 import Vector3
from Shadow_Node import Shadow_Node

class Ether_Node:
    """a node in a sparse tree filling occupied space
    """
    CONTAINED, CONTAINS, CROSSES, CLIPS = 0, 1, 2, 3
    SIZE = 3 # radius of scale 1 node

    def __init__( self, demon, parent=None, position=(0, 0, 0), scale=0 ):
        self.demon = demon # ether demon managing this ether node
        self.parent = parent # ether node containing this node
        self.position = Vector3( position )
        self.scale = scale

        # child nodes indexed by name (x,y,z)
        self.children = {}

        # shadow nodes in this ether node indexed by zone
        self.shadows = {}

    def __getitem__( self, name ):
        """return child with given name, spawn it if it doesn't exist
        """
        # if child with given name does not exist build it
        if name not in self.children:
            scale = self.scale - 1
            diameter = 2.0 * (self.SIZE ** scale)
            position = tuple( p + (n * diameter) for p, n
                              in zip(self.position, name) )
            child = Ether_Node( demon=self.demon, parent=self,
                                position=position, scale=scale )
            self.children[name] = child

        return self.children[name]

    ###
    ### public ether node interface should only be accessed by its demon
    ###

    def insert( self, shadow ):
        """insert given zone shadow into ether tree
        """
        # if this shadow is not solid just insert it here
        if not shadow.zone.solid:
            shadow_node = Shadow_Node( shadow=shadow,
                                       ether=self,
                                       zone=shadow.zone,
                                       coord=(),
                                       intersection=self.CONTAINED )
            shadow.nodes[tuple] = shadow_node
            self.shadows[shadow.zone] = shadow_node

            return True

        # otherwise attempt to insert solid
        return self._insert_solid( shadow=shadow,
                                   coord=(),
                                   zone=shadow.zone,
                                   intersection=self.CONTAINED )

    def _insert_solid( self, shadow, coord, zone, intersection, normal=None ):
        # check for intersecting shadows:
        intersection = False
        for intersecting in self._get_shadows( solid=True ):
            if not shadow.zone.ignore_intersection( intersecting.zone ):
                intersection = True
        
        # if there is no intersection make shadow node here and return true
        if not intersection:
            shadow_node = Shadow_Node( shadow=shadow,
                                       ether=self,
                                       zone=shadow.zone,
                                       coord=coord,
                                       intersection=intersection,
                                       normal=normal )
            shadow.nodes[coord] = shadow_node
            self.shadows[zone] = shadow_node

            return True

        # if there is intersection and we have reached resolution
        # limit return false
        if self.scale == self.demon.COLLISION_RESOLUTION:
            return False

        # otherwise push other solid shadows in this ether node
        for shadow_node in self.shadows:
            if shadow_node.zone.solid:
                self._push_shadow( shadow_node.shadow )

        # then find children that intersect bounds and test them against zone,
        # return false if any child insertions fail
        radius = self.SIZE ** (self.scale - 1)
        for child_name in self.get_bounded_children( *zone.get_bounds() ):
            position = tuple( p + (2 * n * radius)
                              for p, n in zip(self.position, child_name) )
            for z, i, n in zone.intersect( position, radius ):
                if not self.children[child_name]._insert_solid(
                    shadow=shadow, coord=self._next_coord(coord, child_name),
                    zone=z, intersection=i, normal=n ):
                    return False

        return True
        

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

    def _next_coord( self, coord, name ):
        """add name onto coord
        """
        # squish coord into a single number <0-26>
        c = 0
        for i, n in zip( (3, 2, 1), name ):
            c += i * (n + 1)

        return coord + (c,)

    def _push_shadow( self, shadow ):
        """resolve shadow down into child nodes
        """
        
    def remove( self, zone ):
        """remove given zone from ether tree
        """
