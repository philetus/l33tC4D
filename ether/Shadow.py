class Shadow:
    """extension of a zone in ether
    """

    def __init__( self, zone ):

        # top zone shadow is extension of
        self.zone = zone

        # set of shadow nodes
        self.nodes = set()

    def __repr__( self ):
        return "<shadow %s>" % str(self.zone)

