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

        # tracks whether we are inside gtk thread
        self.in_gtk_thread = False
        
        # create new gtk window to hold stuff
        gtk_thread = self.GTK_Thread( self )
        try:
            self._window_init()
        finally:
            gtk_thread.leave()
        
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
        gtk_thread = self.GTK_Thread( self )
        try:
            self._window.show_all()
        finally:
            gtk_thread.leave()

    def destroy( self ):
        """manually trigger a window destroy event
        """
        gtk_thread = self.GTK_Thread( self )
        try:
            self._window.destroy()
        finally:
            gtk_thread.leave()

    def handle_quit( self ):
        """do something when window is closed, return False to suppress
        """
        return True


    ###
    ### private functions to map gtk events to canvas handlers
    ###

    def _on_quit( self, window ):
        gtk_thread = self.GTK_Thread( self, mark=True )
        value = None
        try:
            value = self.handle_quit()

        finally:
            gtk_thread.leave()

        return value
            

    ###
    ### private getter and setter methods for window properties
    ###

    def _get_title( self ):
        return self._window.get_title()

    def _set_title( self, string ):
        self._window.set_title( string )

    def _get_size( self ):
        """window get_size is not guaranteed to return current window size
           this method should be overloaded by subclass to return the size
           of drawing area filling window instead
        """
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

    ###
    ### helper class to manage entering and leaving gtk threads
    ###
    
    class GTK_Thread( object ):
        """manages entering and leaving gtk threads

           if already inside gtk thread when created, does not really enter
           thread and doesn't really leave when leave is called

           setting mark flag to true causes in gtk thread to be set and
           unset without actually calling gtk threads enter/leave for
           use inside callbacks
        """
        def __init__( self, window, mark=False ):
            self.window = window
            self.mark = mark
            self.really_leave = False

            if not self.window.in_gtk_thread:
                if not self.mark:
                    gtk.threads_enter()
                self.window.in_gtk_thread = True
                self.really_leave = True

                #print "entering gtk thread"

            else:
                pass
                #print "not really entering gtk thread"

        def leave( self ):
            if self.really_leave:

                if not self.window.in_gtk_thread:
                    raise RuntimeError( "not in gtk thread!" )
                                        
                self.window.in_gtk_thread = False
                if not self.mark:
                    gtk.threads_leave()

                #print "leaving gtk thread"
                
            else:
                pass
                #print "not really leaving gtk thread"

            # remove cycle to help garbage collector?
            del self.window


