from threading import Thread, Lock
from Queue import Queue
from Ether_Node import Ether_Node
from Shadow import Shadow

class Ether_Demon( Thread ):
    """thread-safe interface to manage zones in ether
    """
    REQUESTS = [ "insert", "remove", "move", "get_intersections" ]
    COLLISION_RESOLUTION = 1 # scale to resolve solid insertion to

    def init( self ):
        Thread.__init__( self )

        # root node of ether octree
        self.top = Ether_Node( demon=self )

        # queue to read requests from
        self.requests = Queue()

        # shadows indexed by zone
        self.shadows = {}

    def run( self ):

        # pull request dictionaries off of queue and pass them
        # to appropriate helper method
        while True:
            args = self.requests.get()
            request = args["request"]
            del args["request"]

            # call helper method for request type
            # self.__getattribute__( "f" )( x ) -> self.f( x )
            if not request in self.REQUESTS:
                raise ValueError( "unrecognized request type: '%s'" % request )
            self.__getattribute__( "_" + request )( **args )

    ###
    ### public methods hide use of queue to assure requests are handled one
    ### at a time
    ###

    def insert( self, zone ):
        """attempt to insert zone into ether

           returns True on success, False on failure
        """
        # build event dict
        responses = Queue() # queue to receive response
        request = { "request":"insert",
                    "zone":zone,
                    "responses":responses }

        # put request on queue and wait for response
        self.requests.put( request )
        response = responses.get()

        # if response is an error raise it, otherwise return it
        if isinstance( response, Exception ):
            raise response

        return response

    def remove( self, zone ):
        """remove zone from ether

           raises assertion error if zone not in ether
        """
        # build event dict
        responses = Queue() # queue to receive response
        request = { "request":"remove",
                    "zone":zone,
                    "responses":responses }

        # put request on queue and wait for response
        self.requests.put( request )
        response = responses.get()

        # if response is an error raise it
        if isinstance( response, Exception ):
            raise response
        
    def move( self, zone, path ):
        """move zone through ether by vector

           returns set of intersecting frozen shadows on failure
        """        
        # build event dict
        responses = Queue() # queue to receive response
        request = { "request":"move",
                    "zone":zone,
                    "path":path,
                    "responses":responses }

        # put request on queue and wait for response
        self.requests.put( request )
        response = responses.get()

        # if response is an error raise it, otherwise return response
        if isinstance( response, Exception ):
            raise response

        return response

    def get_intersections( self, zone ):
        """return dictionary of frozen shadows intersecting this zone
        """
        # build event dict
        responses = Queue() # queue to receive response
        request = { "request":"get_intersections",
                    "zone":zone,
                    "responses":responses }

        # put request on queue and wait for response
        self.requests.put( request )
        response = responses.get()

        # if response is an error raise it, otherwise return response
        if isinstance( response, Exception ):
            raise response

        return response

    ###
    ### private helper methods to handle requests
    ###

    def _insert( self, zone, responses ):
        response = None
        try:
            
            # check that zone does not already have a shadow in index
            if zone in self.shadows:
                raise AssertionError(
                    "insert failed: zone %s already in ether" % str(zone)) )

            # grow ether if necessary
            self._grow_to_bounds( *zone.get_bounds() )

            # create shadow for zone
            self.shadows[zone] = Shadow( zone )

            # attempt to insert zone's shadow into top ether node
            response = self.top.insert( shadow )

            # if insertion fails remove shadow
            if response is not True:
                self._wipe_shadow( shadow )
                del self.shadows[zone]

        except (Exception, e):
            response = e

        # place response on queue
        responses.put( response )

    def _remove( self, zone, responses ):
        response = True
        try:

            # call remove shadow to do the dirty in the ether
            self._wipe_shadow( zone )

            # remove shadow from index
            del self.shadows[zone]

        except (Exception, e ):
            response = e

        # put response on queue to signal completion
        responses.put( response )

    def _move( self, zone, path, responses ):
        response = None
        try:

            # remove old shadow
            shadow = self.shadows[zone]
            self._wipe_shadow( shadow )

            # generate moving geometry and test for collisions
            zone.start_motion( zone, path )
            response = self.top.insert( shadow )

            # remove shadow when finished
            self._wipe_shadow( shadow )
                
            # if response isn't true fail motion and replace shadow
            if response is not True:
                zone.fail_motion()
                if not self.top.insert( shadow ):
                    raise AssertionError(
                        "couldn't reinsert shadow after failed motion: zone %s"
                        % str(zone) )

            # otherwise complete motion and insert zone in new position
            else:
                
                # move zone to final position
                zone.finish_motion()

                # grow ether if necessary
                self._grow_to_bounds( *zone.get_bounds() )

                # reinsert shadow into top node
                if not self.top.insert( shadow ):
                    raise AssertionError(
                        "final position inconsistent with motion: zone %s"
                        % str(zone) )
                    
        except (Exception, e ):
            response = e

        responses.put( response )
                
    def _get_intersections( self, zone, responses ):
        response = None
        try:

            # make dictionary to hold intersecting frozen shadows
            # indexed by zone
            response = {}

            # start with containing ether node
            shadow = self.shadows[zone]
            node = shadow.get_top_ether()

            node._get_intersections( shadow, response )
            
        except (Exception, e):
            response = e
            
        responses.put( response )

    ###
    ### private helper methods to do stuff
    ###

    def _wipe_shadow( self, shadow ):
        raise NotImplementedError()

    def _grow_to_bounds( self, bmin, bmax ):
        node = self.top
        grew = False

        # if bounds not contained by top node grow top until it is
        while not node.contains_bounds( bmin, bmax ):

            # grow new parent node
            scale = node.scale + 1
            diameter = 2.0 * (node.SIZE ** scale)
            self.top = Ether_Node( demon=self, position=node.position,
                                   scale=scale )
            node.parent = self.top
            node = self.top

            # update shadow coords when done
            grew = True

        # update shadow coords if top grew
        if grew:
            self.top.update_shadow_coords()

