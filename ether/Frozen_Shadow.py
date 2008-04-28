class Frozen_Shadow:
    """snapshot of extension of zone in ether intersecting querying zone
    """

    def __init__( self, zone ):
        self.zone = zone

        # set of shadow nodes indexed by coord
        self.nodes = {}

    def get_top_coord( self ):
        """calculate coord of top ether node
        """
        if not self.nodes:
            raise AssertionError( "empty shadow has no top coord!" )
            
        # find largest common coord prefix
        coords = list( self.nodes )
        top_coord = list( coords.pop() )
        while coords and top_coord:
            coord = coords.pop()

            # cut top coord to size of coord if it is longer
            top_coord = top_coord[:len(coord)]
            
            # loop and compare coords, chop top coord at first mismatch
            same = True
            i = 0
            while same and i < len(top_coord):
                if top_coord[i] != coord[i]:
                    same = False
                    top_coord = top_coord[:i]
                i += 1

        # return top coord as tuple
        return tuple(top_coord)
