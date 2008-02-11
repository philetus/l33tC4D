from Vector3 import Vector3
from math import degrees, radians, cos, sin, asin, atan2

class Polar_Vector3( Vector3 ):
    """polar interface to vector3
    """
    __slots__ = "_coords" # instances only store numpy coords matrix
    
    def __repr__( self ):
        return "<polar_vector3 lat=%.3f lon=%.3f radius=%.3f />" % (
            self.lat, self.lon, self.radius )

    def set_heading( self, lat, lon, radius=1.0 ):
        """set heading of vector to given lat, lon
        """
        self[0] = radius * cos( radians(90 - lat) ) * cos( radians(lon) )
        self[1] = radius * cos( radians(90 - lat) ) * sin( radians(lon) )
        self[2] = radius * sin( radians(90 - lat) )
        return self

    ###
    ### getter and setter methods for properties
    ###

    def _get_lat( self ):
        return 90.0 - degrees( asin(self.z / self.magnitude) )

    def _get_lon( self ):
        return degrees( atan2(self.y, self.x) )

    ###
    ### properties
    ###

    lat = property( fget=_get_lat, doc="latitude of vector" )
    lon = property( fget=_get_lon, doc="longitude of vector" )
    radius = Vector3.magnitude
