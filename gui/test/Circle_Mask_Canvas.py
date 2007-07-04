from l33tC4D.gui.Gui import Gui
from l33tC4D.gui.Canvas import Canvas

from math import sqrt

class Circle_Mask_Canvas( Canvas ):
    """A draws circles with masks to test l33tgui canvas
    """

    class Circle( object ):

        # length of control segment for approximating a unit circle
        # from http://www.whizkidtech.redprince.net/bezier/circle/
        KAPPA = 0.5522847498
        
        def __init__( self, center, radius ):
            self.center = center
            self.radius = radius
            self.color = ( 1.0, 0.0, 1.0, 0.6 )
            
        def draw( self, brush ):
            brush.color = self.color

            # move to 0 degree position on circle
            brush.move_to( self.center[0] + self.radius, self.center[1] )
            brush.path_by( dx=-self.radius,
                           dy=self.radius,
                           c0_dx=0,
                           c0_dy=self.radius * self.KAPPA,
                           c1_dx=(self.radius * self.KAPPA) - self.radius,
                           c1_dy=self.radius )
            brush.path_by( dx=-self.radius,
                           dy=-self.radius,
                           c0_dx=-self.radius * self.KAPPA,
                           c0_dy=0,
                           c1_dx=-self.radius,
                           c1_dy=(self.radius * self.KAPPA) - self.radius )
            brush.path_by( dx=self.radius,
                           dy=-self.radius,
                           c0_dx=0,
                           c0_dy=-self.radius * self.KAPPA,
                           c1_dx=self.radius - (self.radius * self.KAPPA),
                           c1_dy=-self.radius )
            brush.path_by( dx=self.radius,
                           dy=self.radius,
                           c0_dx=self.radius * self.KAPPA,
                           c0_dy=0,
                           c1_dx=self.radius,
                           c1_dy=self.radius - (self.radius * self.KAPPA) )
            brush.close_path()
            brush.fill_path()
            brush.clear_path()
            

    def __init__( self, gui ):
        super( Circle_Mask_Canvas, self ).__init__( gui=gui )

        # flag tracks whether mouse button is down
        self.pressed_flag = False
        
        # Variables to track rubber band for line being drawn
        self.first_point = None
        self.last_point = None

        # list of circles that have been drawn
        self.circles = [] 

        # variables to control appearance of lines
        self.line_thickness = 5
        self.line_color = (1.0, 0.0, 0.0, 0.8) # slightly translucent red
        self.rubber_line_thickness = 2
        self.rubber_line_color = (0.0, 0.0, 0.0, 0.4) # translucent gray

        # background color to draw
        self.background_color = (1.0, 1.0, 1.0, 1.0) # opaque white

        # set window title
        self.title = "l33tgui: circle mask test app"
        
    def handle_press( self, x, y ):
        """When mouse button is pressed, set the flag to True and set the coords
           for the first point
        """
        self.pressed_flag = True
        self.first_point = (x, y)

    def handle_release(self, x, y):
        """when mouse button is released, finalize line and clear the mouse
           pressed flag
        """
        # append new line to list of lines
        self.circles.append( self.Circle(
            self.first_point, self.distance(self.first_point,(x,y))) )

        # clear mouse pressed flag and rubber band line coords
        self.pressed_flag = False
        self.first_point = None
        self.last_point = None

        # trigger canvas to redraw itself
        self.redraw()

    def handle_motion(self, x, y):
        """when mouse is moved, follow mouse with rubber band line
        """
        if self.pressed_flag:
            self.last_point = (x, y)

            # trigger canvas to redraw itself
            self.redraw()
        
    def handle_draw( self, brush ):
        """when a canvas redraw is triggered draw all lines in the lines list
           and if we are in the middle of drawing a line draw rubber band
        """
        # draw background
        brush.color = self.background_color
        width, height = self.size
        brush.move_to( 0, 0 )
        brush.path_to( width, 0 )
        brush.path_to( width, height )
        brush.path_to( 0, height )
        brush.close_path()
        brush.fill_path()
        brush.clear_path()
        
        # draw all circles in lines list
        pop_counter = 0
        for circle in self.circles:
            pop_counter += 1
            mask_width, mask_height = brush.mask_size
            brush.push_mask( 5, 5, mask_width - 5, mask_height - 5 )
            circle.draw( brush )

        # fill in smallest masked area with current color
        brush.move_to( 0, 0 )
        brush.path_to( width, 0 )
        brush.path_to( width, height )
        brush.path_to( 0, height )
        brush.close_path()
        brush.fill_path()
        brush.clear_path()

        for i in range( pop_counter ):
            brush.pop_mask()        

        # if we are currently drawing a line draw rubber band
        if (self.first_point is not None) and (self.last_point is not None):
            brush.color = self.rubber_line_color
            brush.size = self.rubber_line_thickness
            brush.move_to( *self.first_point )
            brush.path_to( *self.last_point )
            brush.stroke_path()
            brush.clear_path()

    def handle_quit( self ):
        """say goodbye when we leave
        """
        print "bye!"

        # really close the window
        return True

    @staticmethod
    def distance( a, b ):
        return sqrt( ((b[0] - a[0])**2) + ((b[1] - a[1])**2) )


if __name__ == "__main__":
    gui = Gui()
    gui.start()
    
    canvas = Circle_Mask_Canvas( gui )
    canvas.show()

    
