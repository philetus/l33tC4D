from l33tC4D.gui.Gui import Gui
from l33tC4D.space.Space import Space
from l33tC4D.space.Box import Box
from l33tC4D.space.Zone_Camera import Zone_Camera

class Box_Camera( Zone_Camera ):
    """draws some boxes using zone camera
    """

    def __init__( self, gui, space ):
        Zone_Camera.__init__( self, gui, space )


if __name__ == "__main__":
    gui = Gui()
    gui.start()

    space = Space()
    a = Box()
    b = Box( centroid=(7, 7, 7) )

    space.insert( a )
    space.insert( b )

    camera = Box_Camera( gui, space )
    camera.show()
