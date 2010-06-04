import gtk
gtk.set_interactive(False)
import time
from threading import Thread, Lock

class Gui( object ):
    """root level gui class manages windows
    """

    def __init__( self ):
        # start gtk threads
        gtk.gdk.threads_init()

        # holds gtk main loop thread
        self._gtk_thread = None

        # set of running windows
        self._windows = set()

        # locks
        self.gl_lock = Lock()

    def _start_gtk( self ):
        print "starting gtk main loop"
        
        gtk.gdk.threads_enter()
        try:
            gtk.main()
        finally:
            gtk.gdk.threads_leave()

        print "stopped gtk main loop"

    def add_window( self, window ):
        self._windows.add( window )

    def start( self ):
        """start gui rendering loop
        """
        self._gtk_thread = Thread( target=self._start_gtk )
        self._gtk_thread.start()

    def stop( self ):
        """stop gui rendering loop and close all windows
        """
        
        # kill all windows
        while self._windows:
            window = self._windows.pop()
            window.destroy()
        
        # stop gtk main loop
        gtk.gdk.threads_enter()
        try:
            gtk.main_quit()
        finally:
            gtk.gdk.threads_leave()
            

