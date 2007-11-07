import numpy
from math import acos, degrees

class VectorX( object ):
    """abstract class implementing vector methods with numpy lib

       subclasses must store coords as a numpy array named '_coords'
    """
    # instances only store coords array
    __slots__ = "_coords"

    def __iter__( self ):
        for coord in self._coords:
            yield coord.item()

    def __getitem__( self, index ):
        return self._coords[index,0]

    def __setitem__( self, index, value ):
        self._coords[index,0] = value

    def add( self, vector ):
        """add given vector to this vector and return as new vector
        """
        return self.__class__( *(c.item() for c in
                                 numpy.add(self._coords, vector._coords)[:3]) )

    def __add__( self, vector ):
        """a + b <==> a.add( b )
        """
        return self.add( vector )

    def subtract( self, vector ):
        """subtract given vector from this vector and return as new vector
        """
        return self.__class__( *(c.item() for c in
                                 numpy.subtract(self._coords,
                                                vector._coords)[:3]) )

    def __sub__( self, vector ):
        """a - b <==> a.subtract( b )
        """
        return self.subtract( vector )

    def dot( self, vector ):
        """returns scalar dot product of this vector and given vector
        """
        return numpy.dot( self._coords[:3].transpose(),
                          vector._coords[:3] ).item()

    def cross( self, vector ):
        """cross this vector with given vector and return as new vector
        """
        return self.__class__( *numpy.cross(self._coords.A1[:3],
                                            vector._coords.A1[:3]) )

    def multiply( self, scalar ):
        """multiply this vector by given scalar and return as new vector
        """
        return self.__class__( *(c.item() for c in
                                 numpy.multiply(self._coords,
                                                float(scalar))[:3]) )

    def divide( self, scalar ):
        """divide this vector by given scalar and return as new vector
        """
        # check we aren't dividing by 0
        if scalar == 0.0:
            raise ZeroDivisionError( "attempted to divide vector by 0!" )
        return self.__class__( *(c.item() for c in
                                 numpy.divide(self._coords,
                                              float(scalar))[:3]) )
    
    def normalize( self ):
        """return new vector with same heading and magnitude of 1.0
        """
        # assure magnitude > 0
        magnitude = self._get_magnitude()
        if magnitude == 0.0:
            raise ZeroDivisionError( "can't normalize vector of magnitude 0!" )
        return self.divide( magnitude )

    def project( self, vector ):
        """project this vector onto given vector and return as new vector
        """
        return vector.multiply( self.dot(vector) /
                                (vector._get_magnitude()**2) )

    def angle_to( self, vector ):
        """return angle from this vector to given vector in degrees
        """
        try:
            return degrees( acos(self.normalize().dot(vector.normalize())) )
        except ValueError:
            if self._get_magnitude() > 0 and vector._get_magnitude() > 0:
                return 0.0
            raise ValueError( "couldn't calculate angle from %s to %s!"
                              % (self, vector) )

    ###
    ### getter and setter methods for properties
    ###
    
    def _get_magnitude( self ):
        return numpy.sqrt( sum(c**2 for c in self) )

    ###
    ### properties
    ###

    magnitude = property( fget=_get_magnitude, doc="length of vector" )
