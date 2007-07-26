import numpy
from math import degrees, radians, cos, sin, asin, atan2

from VectorX import VectorX
from matrices import angle_axis

class Vector3( VectorX ):
    """3 dimensional vector using numpy library to implement storage and methods
    """
    # instances only store coords array
    __slots__ = "_coords"

    def __init__( self, x=0.0, y=0.0, z=0.0, lat=None, lon=None, r=1.0 ):
        """store x, y and z coordinates in numpy array
        
           if latitude and longitude are given convert to cartesian coords
        """
        if lat is not None and lon is not None:
            lat = radians( lat )
            lon = radians( lon )
            x = r * cos( lat ) * cos( lon )
            y = r * cos( lat ) * sin( lon )
            z = r * sin( lat )
        self._coords = numpy.array( [float(c) for c in (x, y, z)], 'd' )

    def __repr__( self ):
        return "<vector3 x=%.3f y=%.3f z=%.3f />" % tuple( self._coords )
    
    def rotate( self, angle, axis ):
        """rotate this vector around given axis and return as new vector

           axis is another vector3
           angle is in degrees
        """
        # get angle axis rotation matrix
        rotation = angle_axis( float(angle), *axis._coords.flat )

        # return new vector with rotated coords
        return self.transform( rotation )

    def transform( self, matrix ):
        """transform vector with 4x4 matrix and return as new vector
        """
        coords = self._coords.copy()
        coords.resize( 4 )

        # multiply vector with matrix
        #print "coords:", coords, "matrix:", matrix
        #WTF??? coords =  matrix * coords
        coords = coords * matrix

        # return new vector with rotated coords
        return self.__class__( *tuple(coords.flat)[:3] )

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
        
    def _get_z( self ):
        return self._coords[2]
    def _set_z( self, value ):
        self._coords[2] = float( value )

    def _get_lat( self ):
        return degrees( asin(self._coords[2] / self._get_magnitude()) )

    def _get_lon( self ):
        return degrees( atan2(self._coords[1], self._coords[0]) )

    ###
    ### properties
    ###
    
    x = property( fget=_get_x, fset=_set_x, doc="x coordinate of vector" )
    y = property( fget=_get_y, fset=_set_y, doc="y coordinate of vector" )
    z = property( fget=_get_z, fset=_set_z, doc="z coordinate of vector" )

    lat = property( fget=_get_lat, doc="latitude of vector" )
    lon = property( fget=_get_lon, doc="longitude of vector" )
