from OpenGL.GL import ( glPushMatrix, glPopMatrix, glTranslatef, glMaterialfv,
                        GL_FRONT, GL_SPECULAR, GL_SHININESS, GL_DIFFUSE )
from OpenGL.GLUT import glutSolidCube

from Zone import Zone
from Vertex import Vertex

class Box( Zone ):
    """a simple cube zone rendered with glut solid cube
    """

    def __init__( self, centroid=(0, 0, 0), size=10.0 ):
        self.centroid = Vertex( *centroid )
        self.size = float( size )

        # generate min and max bounds for zone init
        radius = self.size / 2.0
        min_bound = Vertex( *[c - radius for c in self.centroid] )
        max_bound = Vertex( *[c + radius for c in self.centroid] )
        Zone.__init__( self, min_bound, max_bound )

        self.selected_color = ( 0.7, 0.0, 0.1, 1.0 )
        self.last_color = None

        self.specular = ( 1.0, 1.0, 1.0, 1.0 )
        self.shininess = 100.0
        self.diffuse = ( 0.1, 0.0, 0.7, 1.0 )

    def __repr__( self ):
        return "<box x='%.2f' y='%.2f' z='%.2f' size='%.2f' />" % (
            tuple(self.centroid) + (self.size,) )

    def draw( self ):
        """draw a cube using glut solid cube
        """
        # save current matrix
        glPushMatrix()

        # set material
        glMaterialfv( GL_FRONT, GL_SPECULAR, self.specular )
	glMaterialfv( GL_FRONT, GL_SHININESS, self.shininess )
        glMaterialfv( GL_FRONT, GL_DIFFUSE, self.diffuse )

        # move to centroid
        glTranslatef( *self.centroid )

        # draw cube
        glutSolidCube( self.size )

        # restore matrix
        glPopMatrix()

    def handle_select( self ):
        """change color on selection
        """
        self.last_color = self.diffuse
        self.diffuse = self.selected_color
        
    def handle_deselect( self ):
        """restore color on deselect
        """
        self.diffuse = self.last_color
        
