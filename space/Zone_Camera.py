from OpenGL.GLU import gluUnProject
from OpenGL.GL import *

from l33tC4D.gui.Gui import Gui
from l33tC4D.gui.GL_Camera import GL_Camera

from Space import Space
from Vertex import Vertex
from Edge import Edge

class Zone_Camera( GL_Camera ):
    """renders zones in space octree using opengl
    """

    def __init__( self, gui, space ):
        GL_Camera.__init__( self, gui )

        self.space = space

        self.eye = ( 0.0, 0.0, -100.0 )

        self.selected = set()

        self.last_click = None

    def handle_draw( self ):
        """
        """
        if self.last_click is not None:
            glPushMatrix()
            glColor3f(0,1,0)
            glBegin( GL_LINES )
            for v in self.last_click:
                glVertex3f( *v )
            glEnd()
            glPopMatrix()
        
        for zone in self.space.zones | self.space.get_child_zones():
            zone.draw()

    def handle_press( self, x, y ):
        """
        """
        # opengl calculates coords from lower left
        width, height = self.size
        y = height - y
        print "button pressed at %d, %d" % (x, y)

        near = Vertex( *gluUnProject( x, y, 0.0 ) )
        far = Vertex( *gluUnProject( x, y, 1.0 ) )
        selection = Edge( near, far )

        print "selection edge from %s to %s" % ( str(near), str(far) )

        #self.last_click = near, far

        # find selected
        print "processing selection...",
        self.select( zone=selection )
        print "done!"

        self.redraw()

    def select( self, zone, kissing=True ):
        """select zones in camera's space octree by interfering with given zone
        """
        print "a",
        kissed, contained = self.space.interfere( zone, limit=2**1 )

        print "b",
        selection_set = contained
        if kissing:
            selection_set |= kissed

        # remove zones no longer in selection set
        for z in self.selected - selection_set:
            self.selected.remove( z )
            z.deselect()

        # add novel zones to selection set
        for z in selection_set - self.selected:
            z.select()
            self.selected.add( z )

    

