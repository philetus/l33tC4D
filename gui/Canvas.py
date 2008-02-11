import gtk

from Window import Window
from Brush import Brush

class Canvas( Window ):
    """superclass for cross-platform 2d graphics application windows

       the window is filled with a 2d drawing surface that can be drawn to
       using the brush interface

       a draw handler taking a brush as an argument must be provided by
       subclasses to allow the canvas to redraw the window in a separate thread
       
       redraw events can be manually triggered by calling the redraw() method

       a pointer motion handler, a pointer button pressed handler and a pointer
       button released handler are provided to allow mouse events to be
       captured by providing the appropriate handler in a subclass

       the canvas is displayed to the screen by calling show()

       window quit events can be captured by providing a handle_quit() method
       in a subclass, and can be suppressed by returning False from the
       quit handler
    """

    def __init__( self, gui ):
        super( Canvas, self ).__init__( gui=gui )
        
        # set up drawing area widget
        self._drawing_area = None
        gtk_thread = self.GTK_Thread( self )
        try:
            self._init_drawing_area()
        finally:
            gtk_thread.leave()
            
        # set default window title and size
        self.title = "l33tgui: canvas"
        self.size = (400, 400)

    def redraw( self ):
        """manually trigger a canvas redraw event
        """
        gtk_thread = self.GTK_Thread( self )
        try:
            self._drawing_area.queue_draw()
        finally:
            gtk_thread.leave()

    def handle_draw( self, brush ):
        """called to draw canvas contents with brush
        """
        raise NotImplementedError(
            "classes that subclass Canvas must implement a handle_draw method" )

    def handle_motion( self, x, y ):
        """do something when pointer is moved over canvas
        """
        pass

    def handle_press( self, x, y ):
        """do something when pointer button is triggered
        """
        pass

    def handle_release( self, x, y ):
        """do something when pointer button is released
        """
        pass

    def handle_resize( self ):
        """do something when window is resized
        """
        pass

    ###
    ### private functions to map gtk events to canvas handlers
    ###

    def _on_expose( self, drawing, event ):
        gtk_thread = self.GTK_Thread( self, mark=True )
        try:
            # get a new cairo context from the drawing area
            context = self._drawing_area.window.cairo_create()

            # set a clip region for the expose event
            context.rectangle( event.area.x, event.area.y,
                               event.area.width, event.area.height)
            context.clip()

            # call draw handler to draw contents of canvas to cairo context
            self.handle_draw( Brush(context, self.size) )

        finally:
            gtk_thread.leave()

        return False

    def _on_configure( self, drawing, event ):
        gtk_thread = self.GTK_Thread( self, mark=True )
        try:
            self.handle_resize()
        finally:
            gtk_thread.leave()

    def _on_motion( self, drawing_area, event ):
        gtk_thread = self.GTK_Thread( self, mark=True )
        try:
            self.handle_motion( event.x, event.y )
        finally:
            gtk_thread.leave()

    def _on_press( self, drawing_area, event ):
        gtk_thread = self.GTK_Thread( self, mark=True )
        try:
            self.handle_press( event.x, event.y )
        finally:
            gtk_thread.leave()

    def _on_release( self, drawing_area, event ):
        gtk_thread = self.GTK_Thread( self, mark=True )
        try:
            self.handle_release( event.x, event.y )
        finally:
            gtk_thread.leave()

    ###
    ### private getter and setter methods for canvas properties
    ###

    def _get_size( self ):
        gtk_thread = self.GTK_Thread( self )
        try:
            rect = self._drawing_area.get_allocation()
        finally:
            gtk_thread.leave()

        return rect.width, rect.height

    ###
    ### private helper functions
    ###

    def _init_drawing_area( self ):
        """set up drawing area widget
        """
        # get a new drawing area object
        self._drawing_area = gtk.DrawingArea()

        # set up callbacks
        self._drawing_area.set_events( gtk.gdk.POINTER_MOTION_MASK |
                                       gtk.gdk.BUTTON_RELEASE_MASK |
                                       gtk.gdk.BUTTON_PRESS_MASK )
        self._drawing_area.connect( "expose_event", self._on_expose )
        self._drawing_area.connect( "configure_event", self._on_configure )
        self._drawing_area.connect( "motion_notify_event", self._on_motion )
        self._drawing_area.connect( "button_press_event", self._on_press )
        self._drawing_area.connect( "button_release_event", self._on_release )

        # add drawing area to window
        self._window.add( self._drawing_area )
