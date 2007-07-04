import gtk

class Window( object ):
    """superclass for various l33tgui windows

       creates gtk window to hold a widget and registers it with the
       window boss
    """

    def __init__( self, gui ):
        
        # register window with gui
        self.gui = gui
        self.gui.add_window( self )

        # create new gtk window to hold stuff
        gtk.threads_enter()
        try:
            self._window_init()
        finally:
            gtk.threads_leave()
        
    def _window_init( self ):
        """create gtk window and connect its destroy signal to on quit method
        """
        self._window = gtk.Window()
        self._window.set_resize_mode( gtk.RESIZE_IMMEDIATE )
        self._window.set_reallocate_redraws( True )
        self._window.connect( "destroy", self._on_quit )

    def show( self ):
        """display window on screen
        """        
        gtk.threads_enter()
        try:
            self._window.show_all()
        finally:
            gtk.threads_leave()

    def destroy( self ):
        """manually trigger a window destroy event
        """
        gtk.threads_enter()
        try:
            self._window.destroy()
        finally:
            gtk.threads_leave()

    def handle_quit( self ):
        """do something when window is closed, return False to suppress
        """
        return True

    ###
    ### private functions to map gtk events to canvas handlers
    ###

    def _on_quit( self, window ):
        return self.handle_quit()
            

    ###
    ### private getter and setter methods for window properties
    ###

    def _get_title( self ):
        return self._window.get_title()

    def _set_title( self, string ):
        self._window.set_title( string )

    def _get_size( self ):
        # window get_size is not guaranteed to return current window size
        # this method should be overloaded by subclass to return the size
        # of drawing area filling window instead
        return self._window.get_size()
    
    def _set_size( self, size ):
        self._window.resize( *size )

    def _get_position( self ):
        return self._window.get_position()
    
    def _set_position( self, position ):
        self._window.move( *position )

    ###
    ### properties for accessing window attributes
    ###

    title = property( _get_title, _set_title, doc="window title" )
    size = property( _get_size, _set_size,
                     doc="current window size (width, height)" )
    position = property( _get_position, _set_position,
                     doc="current window position (x, y)" )
