from numpy import matrix, dot, cross
import math

class Vector3:
    """3 dimensional vector using numpy library to implement storage and methods
    """
    __slots__ = [ "_coords" ] # instances only store numpy coords matrix
    EPSILON = 0.001 # +/- to be considered equal

    def __init__( self, seed=(1, 0, 0) ):
        """store x, y and z coordinates in numpy matrix
        """
        x, y, z = seed
        self._coords = matrix( [[x], [y], [z], [1.]], 'd' )

    def __getitem__( self, index ):
        return self._coords[index,0]

    def __setitem__( self, index, value ):
        self._coords[index,0] = value

    def __iter__( self ):
        for coord in self.array:
            yield coord

    def __repr__( self ):
        return "<vector3 x=%.3f y=%.3f z=%.3f />" % tuple( self )
    
    def add( self, vector3 ):
        """add given vector to this vector
        """
        self._coords[:3] += vector3._coords[:3]
        return self
    
    def __iadd__( self, vector3 ):
        """a += b <==> a.add( b )
        """
        return self.add( vector3 )

    def subtract( self, vector3 ):
        """subtract given vector from this vector and return as new vector
        """
        self._coords[:3] -= vector3._coords[:3]
        return self

    def __isub__( self, vector3 ):
        """a -= b <==> a.subtract( b )
        """
        return self.subtract( vector3 )

    def dot( self, vector3 ):
        """returns scalar dot product of this vector and given vector
        """
        return dot( self._coords[:3].transpose(), vector3._coords[:3] ).item()

    def cross( self, vector3 ):
        """cross this vector with given vector
        """
        product = cross( self.array, vector3.array )
        self._coords[:3] = matrix( product ).transpose()
        return self

    def multiply( self, scalar ):
        """multiply this vector by given scalar
        """
        self._coords[:3] *= scalar
        return self

    def __imul__( self, scalar ):
        return self.multiply( scalar )

    def divide( self, scalar ):
        """divide this vector by given scalar
        """
        # check we aren't dividing by 0
        if abs(scalar) < self.EPSILON:
            raise ZeroDivisionError( "can't divide vector by zero!" )

        self._coords[:3] /= scalar

        return self

    def __idiv__( self, scalar ):
        return self.divide( scalar )
    
    def normalize( self ):
        """set magnitude to 1.0; raises ZeroDivisionError if magnitude is 0
        """
        self.set_magnitude( 1.0 )
        return self

    def project( self, vector3 ):
        """project this vector onto given vector
        """
        self._coords[:3] = vector3._coords[:3] * ( self.dot(vector3)
                                                   / vector3.magnitude**2 )
        
        return self
    
    def angle_to( self, vector3 ):
        """return angle from this vector to given vector in degrees
        """
        # make sure neither vector is zero-length
        sm = self.magnitude
        vm = vector3.magnitude
        if abs(sm) < self.EPSILON or abs(vm) < self.EPSILON:
            raise ZeroDivisionError(
                "can't calculate angle between zero-length vectors!" )
        
        # calculation will fail if vectors have same heading
        # catch error and return zero
        try:
            return math.degrees( math.acos(self.dot(vector3) / (sm * vm)) )
        except ValueError:
            # test whether direction is same or opposite
            if Vector3( self ).add( vector3 ).magnitude < sm:
                return 180.0
            return 0.0
        
    def rotate( self, degrees, axis ):
        """rotate this vector around given axis vector and return as new vector
        """
        # copy and normalize axis
        axis = Vector3( axis ).normalize()

        # get stub of self projected onto axis
        stub = Vector3( self ).project( axis )

        # subtract stub from self
        self -= stub

        # get new vector crossed with axis
        crossed = Vector3( axis ).cross( self )

        # trigify self and crossed to account for rotation
        crossed *= math.sin( math.radians(degrees) )
        self *= math.cos( math.radians(degrees) )

        # add crossed and stub components to self
        self += crossed
        self += stub
        
        return self

    def transform( self, matrix3 ):
        """transform vector with 4x4 matrix
        """
        self._coords =  matrix3._matrix * self._coords
        return self

    def set_magnitude( self, scalar ):
        # assure magnitude is not zero
        m = self._get_magnitude()
        if m < self.EPSILON:
            raise ZeroDivisionError(
                "can't adjust magnitude of zero-length vector!" )
        self._coords[:3] *= scalar / m

    ###
    ### getter and setter methods for properties
    ###

    def _get_x( self ):
        return self._coords[0,0]
    def _set_x( self, value ):
        self._coords[0,0] = value
        
    def _get_y( self ):
        return self._coords[1,0]
    def _set_y( self, value ):
        self._coords[1,0] = value
        
    def _get_z( self ):
        return self._coords[2,0]
    def _set_z( self, value ):
        print "setting z"
        self._coords[2,0] = value
        
    def _get_magnitude( self ):
        return math.sqrt( sum(self.array**2) )

    def _get_array( self ):
        return self._coords[:3].A1

    ###
    ### properties
    ###
    
    x = property( _get_x, doc="x coordinate of vector" )
    y = property( _get_y, doc="y coordinate of vector" )
    z = property( _get_z, doc="z coordinate of vector" )
    magnitude = property( _get_magnitude, doc="length of vector" )
    array = property( _get_array, doc="coords as flat array" )

