import gtk
import gtk.gdkgl
import gtk.gtkgl
from OpenGL.GL import *
from OpenGL.GLU import *

from Window import Window

class GL_Camera( Window ):
    """a window showing a view of an opengl world
    """
        
    def __init__( self, gui, gl_context=None ):
        super( GL_Camera, self ).__init__( gui=gui )
        
        #print "init 0"
        

        #print "init 0.1"

        # eye position and focus
        self.eye = ( 0.0, 0.0, -6.0 )
        self.focus = ( 0.0, 0.0, 3.0,
                       0.0, 0.0, 0.0,
                       0.0, 1.0, 0.0 )

        # gl context and gl drawable
        self._gl_context = gl_context
        self._gl_drawable = None
        
        # create new gl drawing area and add it to window
        gtk.threads_enter()
        try:
            self._init_gl_area()
        finally:
            gtk.threads_leave()

        #print "init 0.2"
        
        # set default size and title
        self.size = 400, 400
        self.title = "l33tgui: gl camera"

        #print "init 1"



    def redraw( self ):
        """manually trigger a canvas redraw event
        """
        gtk.threads_enter()
        try:
            self._gl_area.queue_draw()
        finally:
            gtk.threads_leave()

    def handle_init_gl( self ):
        """
        """
        #print "handle init gl 0"
        
        light_diffuse = (1.0, 1.0, 1.0, 0.0)
        light_position = (1.0, 1.0, 1.0, 0.0)

        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)

        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClearDepth(1.0)

        self._set_view()

        #print "handle init gl 1"


    def show( self ):
        """display window on screen
        """
        super( GL_Camera, self ).show()
                    
        self._gl_area.realize()

    def handle_draw( self ):
        """draw something
        """
        raise NotImplementedError( "Don't you want to draw something?" )
 
    def handle_resize( self ):
        """do something when window is resized
        """
        pass

    def handle_motion( self, x, y ):
        """do something when mouse pointer is moved
        """
        pass

    def handle_press( self, x, y ):
        """do something when pointer button is pressed
        """
        pass

    def handle_release( self, x, y ):
        """do something when pointer button is released
        """
        pass

    ###
    ### private functions to map gtk events to canvas handlers
    ###

    def _on_realize( self, gl_area ):
        #print "on realize 0"

        # call gl begin or die trying
        self._gl_begin()
        try:

            # call gl init handler
            self.handle_init_gl()

        # call gl end
        finally:
            self._gl_drawable.gl_end()

            #print "on realize 1"

        
    def _on_expose( self, gl_area, event ):
        #print "on expose 0"
        
        # call gl begin or die trying
        self._gl_begin()            
        try:
            
            # ???
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # call draw handler to draw world
            self.handle_draw()

            # set view
            self._set_view()

            # swap or flush buffer
            if self._gl_drawable.is_double_buffered():
                self._gl_drawable.swap_buffers()
            else:
                glFlush()
                
        # call gl end
        finally:
            self._gl_drawable.gl_end()

            #print "on expose 1"

        return True

    def _on_configure( self, gl_area, event ):
        #print "on configure 0"
        

        #print "on configure 0.1"
        
        # call gl begin or die trying
        self._gl_begin()
        try:

            # resize gl viewport to fill camera window
            width, height = self.size
            glViewport(0, 0, width, height)

            self._set_view()

            # call resize handler
            self.handle_resize()
            
        # OpenGL end
        finally:
            self._gl_drawable.gl_end()


        #print "on configure 1"

        return True

    def _on_motion( self, drawing_area, event ):
        self.handle_motion( event.x, event.y )

    def _on_press( self, drawing_area, event ):
        self.handle_press( event.x, event.y )

    def _on_release( self, drawing_area, event ):
        self.handle_release( event.x, event.y )

    ###
    ### private getter and setter methods for properties
    ###

    def _get_size( self ):
        rect = self._gl_area.get_allocation()
        
        return rect.width, rect.height

    ###
    ### private helper functions
    ###
    
    def _gl_begin( self ):
        # call gl begin or die trying
        if self._gl_context is None:
            self._gl_context = self._gl_area.get_gl_context()
        if self._gl_drawable is None:
            self._gl_drawable = self._gl_area.get_gl_drawable()

        #print "context: %s" % self._gl_context
        #print "drawable: %s" % self._gl_drawable

        assert self._gl_drawable.gl_begin( self._gl_context ), \
               "couldn't gl begin in on realize"

    def _init_gl_area( self ):
        # if creating a double buffered framebuffer fails try to create a
        # single buffered framebuffer
        display_mode = gtk.gdkgl.MODE_RGB | \
                       gtk.gdkgl.MODE_DEPTH | \
                       gtk.gdkgl.MODE_DOUBLE
        try:
            self._gl_config = gtk.gdkgl.Config( mode=display_mode )
        except gdkgl.NoMatches:
            display_mode &= ~gtk.gdkgl.MODE_DOUBLE
            self._gl_config = gtk.gdkgl.Config( mode=mode )

        # get opengl drawing area and add it to window
        self._gl_area = gtk.gtkgl.DrawingArea( glconfig=self._gl_config,
                                               share_list=None,
                                               render_type=gtk.gdkgl.RGBA_TYPE )        
        self._window.add( self._gl_area )

        # set up signal handlers
	self._gl_area.set_events( gtk.gdk.POINTER_MOTION_MASK |
                                  gtk.gdk.BUTTON_RELEASE_MASK |
                                  gtk.gdk.BUTTON_PRESS_MASK )
        self._gl_area.connect_after( "realize", self._on_realize )
        self._gl_area.connect( "expose_event", self._on_expose )
	self._gl_area.connect( "configure_event", self._on_configure )
	self._gl_area.connect( "motion_notify_event", self._on_motion )
	self._gl_area.connect( "button_press_event", self._on_press )
	self._gl_area.connect( "button_release_event", self._on_release )
	
    def _set_view( self ):
        width, height = self.size

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if width > height:
            w = float(width) / float(height)
            glFrustum(-w, w, -1.0, 1.0, 5.0, 60.0)
        else:
            h = float(height) / float(width)
            glFrustum(-1.0, 1.0, -h, h, 5.0, 60.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt( *self.focus )
        glTranslatef( *self.eye )
    
