import gtk
import time
from threading import Thread, Lock

class Gui( object ):
    """root level gui class manages windows
    """

    def __init__( self ):
        # start gtk threads
        gtk.threads_init()

        # holds gtk main loop thread
        self._gtk_thread = None

        # set of running windows
        self._windows = set()

        # locks
        self.window_lock = Lock()
        self.gl_lock = Lock()

    def _start_gtk( self ):
        print "starting gtk main loop"
        
        gtk.threads_enter()
        try:
            gtk.main()
        finally:
            gtk.threads_leave()

        print "stopped gtk main loop"

    def add_window( self, window ):
        self.window_lock.acquire()
        self._windows.add( window )
        self.window_lock.release()

    def start( self ):
        """start gui rendering loop
        """
        self._gtk_thread = Thread( target=self._start_gtk )
        self._gtk_thread.start()

    def stop( self ):
        """stop gui rendering loop and close all windows
        """
        self.window_lock.acquire()
        
        # kill all windows
        for window in self._windows:
            window.destroy()
        
        # stop gtk main loop
        gtk.threads_enter()
        try:
            gtk.main_quit()
        finally:
            gtk.threads_leave()
            
        self.window_lock.release()
