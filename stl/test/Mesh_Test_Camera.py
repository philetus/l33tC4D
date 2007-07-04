from OpenGL.GL import *

from l33tC4D.gui.Gui import Gui
from l33tC4D.gui.GL_Camera import GL_Camera

from l33tC4D.stl.STL_Mesh import STL_Mesh

class Mesh_Test_Camera( GL_Camera ):
    """test app opens gl camera window and draws stl mesh
    """

    def __init__( self, gui, gl_context=None ):
        GL_Camera.__init__( self, gui, gl_context )
        
        self.one_hub_mesh = STL_Mesh( "solid_one_hub.stl" )
        self.one_hub_mesh.diffuse = STL_Mesh.YELLOW

        self.eye = ( 0.0, 0.0, -200.0 )

    def handle_draw( self ):
        """draw stl mesh
        """
        # rotate hub 45 degrees
        glRotatef( 45.0, 0.0, 1.0, 0.0 )

        self.one_hub_mesh.draw()

    def handle_press( self, x, y ):
        """
        """
        print "button pressed at %d, %d" % (x, y)


if __name__ == "__main__":
    gui = Gui()
    gui.start()

    camera = Mesh_Test_Camera( gui )
    camera.show()
