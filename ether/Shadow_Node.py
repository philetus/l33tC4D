class Shadow_Node:
    """marks the leaf node of the extension of a zone in ether
    """
    CONTAINED, CONTAINS, CROSSES, CLIPS = 0, 1, 2, 3

    def __init__( self, shadow, ether, zone, intersection, normal=None ):

        # shadow this node belongs to
        self.shadow = shadow

        # ether node this shadow node intersects
        self.ether = ether

        # sub-zone this shadow node is extension of
        self.zone = zone

        # type of intersection with ether node
        self.intersection = intersection

        # zone surface normal at intersection
        self.normal = normal
    
