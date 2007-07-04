import numpy
from scipy.special import sindg, cosdg

from VectorX import VectorX

class Vector2( VectorX ):
    """2 dimensional vector using numpy library to implement storage and methods
    """
    # instances only store coords array
    __slots__ = "_coords"
    
    def __init__( self, x, y ):
        """store x, y and z coordinates in numpy array
        """
        self._coords = numpy.array( [float(c) for c in (x, y)], 'd' )

    def __repr__( self ):
        return "<vector2 x=%.3f y=%.3f />" % tuple( self._coords )

    def cross( self ):
        """rotate vector by 90 degrees
        """
        return self.__class__( -self._coords[1], self._coords[0] )
        
    def rotate( self, degrees ):
        """rotate this vector by given degrees and return as new vector
        """
        # cosine vector is this vector multiplied by cosine of angle
        cosine = self.multiply( cosdg(degrees) )

        # sine vector is cross product of this vector and normalized given
        # vector, multiplied by sine of angle
        sine = self.cross().multiply( sindg(degrees) )

        return cosine.add( sine )

    ###
    ### getter and setter methods for properties
    ###
    
    def _get_x( self ):
        return self._coords[0]
    def _set_x( self, value ):
        self._coords[0] = float( value )
        
    def _get_y( self ):
        return self._coords[1]
    def _set_y( self, value ):
        self._coords[1] = float( value )

    ###
    ### properties
    ###

    x = property( fget=_get_x, fset=_set_x, doc="x coordinate of vector" )
    y = property( fget=_get_y, fset=_set_y, doc="y coordinate of vector" )

