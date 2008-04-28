from Zone import Zone

class Box( Zone ):
    """a solid box that can be inserted into ether
    """

    def __init__( self, position=(0,0,0), size=2, color=(0,0,1,1) ):
        Zone.__init__( self )
