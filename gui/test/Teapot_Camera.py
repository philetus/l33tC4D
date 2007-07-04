from OpenGL.GLUT import glutSolidTeapot, glutSolidSphere

from l33tC4D.gui.Gui import Gui
from l33tC4D.gui.GL_Camera import GL_Camera

class Teapot_Camera( GL_Camera ):
    """test app opens two gl camera windows and draws to them
    """

    def __init__( self, gui, gl_context=None, teapot=True ):
        self.teapot = teapot
        GL_Camera.__init__( self, gui, gl_context )

    def handle_draw( self ):
        """draw a teapot
        """
        #print "handle draw 0"
        if self.teapot:
            glutSolidTeapot( 1 )
        else:
            glutSolidSphere( 1, 12, 12 )

        #print "handle draw 1"

    def handle_press( self, x, y ):
        """
        """
        print "button pressed at %d, %d" % (x, y)

if __name__ == "__main__":
    gui = Gui()
    gui.start()

    camera_a = Teapot_Camera( gui )
    camera_a.show()

    camera_b = Teapot_Camera( gui, camera_a._gl_context, teapot=False )
    camera_b.show()
