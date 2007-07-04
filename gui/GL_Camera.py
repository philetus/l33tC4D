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

        # for rotating view
        self.rotation = [ 0, 0, 0 ]

        # flag to track pointer up or down
        self.pointer_down = False

        # eye position and focus
        self.eye = ( 0.0, 0.0, -6.0 )
        self.focus = ( 0.0, 0.0, 3.0,
                       0.0, 0.0, 0.0,
                       0.0, 1.0, 0.0 )

        # near, far clipping planes
        self.clip = ( 50, 5000 )

        # gl context and gl drawable
        self._gl_context = gl_context
        self._gl_drawable = None

        # create new gl drawing area and add it to window
        gtk_thread = self.GTK_Thread( self )
        try:
            self._init_gl_area()
        finally:
            gtk_thread.leave()

        #print "init 0.2"
        
        # set default size and title
        self.size = 400, 400
        self.title = "l33tgui: gl camera"

        #print "init 1"



    def redraw( self ):
        """manually trigger a canvas redraw event
        """
        gtk_thread = self.GTK_Thread( self )
        try:
            self._gl_area.queue_draw()
        finally:
           gtk_thread.leave()

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

           by default rotates view in x-y, override to change
        """
        if self.pointer_down:
            self.rotation[0] = x
            self.rotation[1] = y
            self.redraw()
            #self._gl_area.queue_draw()

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
        gtk_thread = self.GTK_Thread( self, mark=True )
        try:
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

        finally:
            gtk_thread.leave()

        
    def _on_expose( self, gl_area, event ):
        gtk_thread = self.GTK_Thread( self, mark=True )
        try:
            #print "on expose 0"
            
            # call gl begin or die trying
            self._gl_begin()            
            try:
                
                # ???
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                # Set up the model view matrix
                glMatrixMode( GL_MODELVIEW )
                glLoadIdentity()
                gluLookAt( *self.focus )
                glTranslatef( *self.eye )
                glRotatef( self.rotation[0], 0.0, 1.0, 0.0 )
                glRotatef( self.rotation[1], 1.0, 0.0, 0.0 )
                glRotatef( self.rotation[2], 0.0, 0.0, 1.0 )

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
                gtk_thread.leave()

        finally:
            self.in_gtk_thread = False

        return True

    def _on_configure( self, gl_area, event ):
        gtk_thread = self.GTK_Thread( self, mark=True )
        try:
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

        finally:
            gtk_thread.leave()
            
        return True

    def _on_motion( self, drawing_area, event ):
        gtk_thread = self.GTK_Thread( self, mark=True )
        try:
            self.handle_motion( event.x, event.y )
        finally:
            gtk_thread.leave()

    def _on_press( self, drawing_area, event ):
        gtk_thread = self.GTK_Thread( self, mark=True )
        try:
            self.pointer_down = True
            self.handle_press( event.x, event.y )
        finally:
            gtk_thread.leave()

    def _on_release( self, drawing_area, event ):
        gtk_thread = self.GTK_Thread( self, mark=True )
        try:
            self.pointer_down = False
            self.handle_release( event.x, event.y )
        finally:
            gtk_thread.leave()

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

        # calculate left/right and top/bottom clipping planes based the
        # smallest square viewport
        a = 9.0 / min( width, height )
        clipping_planes = ( a*width, a*height )
        
        # setup the projection
        glFrustum(-clipping_planes[0], clipping_planes[0],
                  -clipping_planes[1], clipping_planes[1],
                  self.clip[0], self.clip[1] )

    
