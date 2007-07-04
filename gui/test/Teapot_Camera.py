from OpenGL.GLUT import glutSolidTeapot, glutSolidSphere
from OpenGL.GL import( glMaterialfv, GL_FRONT, GL_SPECULAR,
                       GL_SHININESS, GL_DIFFUSE )

from l33tC4D.gui.Gui import Gui
from l33tC4D.gui.GL_Camera import GL_Camera

class Teapot_Camera( GL_Camera ):
    """test app opens two gl camera windows and draws to them
    """

    def __init__( self, gui, gl_context=None, teapot=True ):
        self.teapot = teapot
        GL_Camera.__init__( self, gui, gl_context )

        self.specular = ( 1.0, 1.0, 1.0, 1.0 )
        self.shininess = 100.0
        self.diffuse = ( 0.7, 0.0, 0.1, 1.0 )

        self.eye = ( 0.0, 0.0, -100.0 )

    def handle_draw( self ):
        """draw a teapot
        """
        #print "handle draw 0"
        glMaterialfv( GL_FRONT, GL_SPECULAR, self.specular )
	glMaterialfv( GL_FRONT, GL_SHININESS, self.shininess )
        glMaterialfv( GL_FRONT, GL_DIFFUSE, self.diffuse )

        if self.teapot:
            glutSolidTeapot( 10.0 )
        else:
            glutSolidSphere( 10.0, 12, 12 )

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
