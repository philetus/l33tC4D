from Vector3 import Vector3
from math import degrees, radians, cos, sin, asin, atan2

class Polar_Vector3( Vector3 ):
    """polar interface to vector3
    """

    def __init__( self, seed=(0, 0, 1) ):
        lat, lon, radius = seed
        x = radius * cos( radians(lat) ) * cos( radians(lon) )
        y = radius * cos( radians(lat) ) * sin( radians(lon) )
        z = radius * sin( radians(lat) )
        Vector3.__init__( self, (x, y, z) )

    def __repr__( self ):
        return "<polar_vector3 lat=%.3f lon=%.3f radius=%.3f />" % tuple( self )

    def __iter__( self ):
        for v in self.lat, self.lon, self.radius:
            yield v

    ###
    ### getter and setter methods for properties
    ###

    def _get_lat( self ):
        return degrees( asin(self.z / self.magnitude) )

    def _get_lon( self ):
        return degrees( atan2(self.y, self.x) )

    ###
    ### properties
    ###

    lat = property( fget=_get_lat, doc="latitude of vector" )
    lon = property( fget=_get_lon, doc="longitude of vector" )
    radius = Vector3.magnitude
