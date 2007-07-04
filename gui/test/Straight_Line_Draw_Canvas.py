from l33tC4D.gui.Gui import Gui
from l33tC4D.gui.Canvas import Canvas

class Straight_Line_Draw_Canvas( Canvas ):
    """A simple line drawing application to test l33tgui canvas library
    """

    def __init__( self, gui ):
        Canvas.__init__( self, gui )

        # flag tracks whether mouse button is down
        self.pressed_flag = False
        
        # Variables to track rubber band for line being drawn
        self.first_point = None
        self.last_point = None

        # list of lines that have been drawn
        self.lines = [] # [((x0, y0), (x1, y1)), ...]

        # variables to control appearance of lines
        self.line_thickness = 5
        self.line_color = (1.0, 0.0, 0.0, 0.8) # slightly translucent red
        self.rubber_line_thickness = 2
        self.rubber_line_color = (0.0, 0.0, 0.0, 0.4) # translucent gray

        # background color to draw
        self.background_color = (1.0, 1.0, 1.0, 1.0) # opaque white

        # set window title
        self.title = "l33tgui: straight line draw test app"
        
    def handle_press( self, x, y ):
        """When mouse button is pressed, set the flag to True and set the coords
           for the first point
        """
        self.pressed_flag = True
        self.first_point = (x, y)

    def handle_release(self, x, y):
        """when mouse butoon is released, finalize line and clear the mouse
           pressed flag
        """
        # append new line to list of lines
        self.lines.append( (self.first_point, (x, y)) )

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
        
        # draw all lines in lines list
        brush.color = self.line_color
        brush.size = self.line_thickness
        for (x0, y0), (x1, y1) in self.lines:
            brush.move_to( x0, y0 ) # move to beginning of line
            brush.path_to( x1, y1 ) # make path to end of line
            brush.stroke_path() # stroke line with current color and thickness
            brush.clear_path() # clear line path we just drew

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


if __name__ == "__main__":
    gui = Gui()
    gui.start()
    
    canvas = Straight_Line_Draw_Canvas( gui )
    canvas.show()

    
