from numpy import eye, matrix
import math
from Vector3 import Vector3

class Matrix3:
    """4x4 matrix for transformations of 3d vectors
    """
    __slots__ = "_m" # instances only store numpy matrix
    EPSILON = 0.001 # +/- to be considered equal
    
    def __init__( self, seed=None ):
        """default to 4x4 identity matrix
        """
        if seed is None:
            self._matrix = matrix( eye(4, 4) )
        else:
            try:
                self._matrix = matrix( list(seed), 'd' ).reshape( 4, 4 )
            except ValueError:
                raise ValueError( "seed value doesn't give 4x4 matrix: '%s'"
                                  % str(seed) )

    def __repr__( self ):
        return """<matrix3 [[ %8.2f, %8.2f, %8.2f, %8.2f ],
          [ %8.2f, %8.2f, %8.2f, %8.2f ],
          [ %8.2f, %8.2f, %8.2f, %8.2f ],
          [ %8.2f, %8.2f, %8.2f, %8.2f ]] />""" % tuple( self )

    def rotate( self, degrees, axis ):
        """rotate matrix by given degrees around given axis vector

           from http://www.opengl.org/documentation/specs/man_pages/hardcopy/GL/html/gl/rotate.html
          ( xx(1-c)+c	xy(1-c)-zs  xz(1-c)+ys	 0  |
          | yx(1-c)+zs	yy(1-c)+c   yz(1-c)-xs	 0  |
          | xz(1-c)-ys	yz(1-c)+xs  zz(1-c)+c	 0  |
          |	 0	     0		 0	 1  )
          Where	c = cos(angle),	s = sine(angle), and ||( x,y,z )|| = 1
        """
        # generate rotation matrix
        magnitude = axis.magnitude
        if abs( magnitude ) < self.EPSILON:
            raise ZeroDivisionError(
                "can't rotate around zero magnitude vector: %s!" % str(axis) )
        x, y, z = (coord / magnitude for coord in axis)
        c = math.cos( math.radians(degrees) )
        s = math.sin( math.radians(degrees) )
        m = matrix( [[(x*x*(1-c))+c, (x*y*(1-c))-(z*s), (x*z*(1-c))+(y*s), 0],
                     [(y*x*(1-c))+(z*s), (y*y*(1-c))+c, (y*z*(1-c))-(x*s), 0],
                     [(x*z*(1-c))-(y*s), (y*z*(1-c))+(x*s), (z*z*(1-c))+c, 0],
                     [0, 0, 0, 1]],
                    'd' )

        # multiply rotation matrix with current matrix
        self._matrix *= m

        return self


    def translate( self, vector3 ):
        """translate matrix by given vector
        """
        # generate translation matrix
        x, y, z = vector3
        m = matrix( [[1, 0, 0, x],
                     [0, 1, 0, y],
                     [0, 0, 1, z],
                     [0, 0, 0, 1]],
                    'd' )

        # multiply transformation matrix with current matrix
        self._matrix *= m

        return self
       
    def scale( self, x, y, z ):
        """scale matrix by given coefficients
        """
        m = matrix( [[x, 0, 0, 0],
                     [0, y, 0, 0],
                     [0, 0, z, 0],
                     [0, 0, 0, 1]],
                    'd' )

        # multiply scale matrix with current matrix
        self._matrix *= m

        return self

    def transform( self, matrix3 ):
        """multiply this transformation matrix by another
        """
        self._matrix *= matrix3._matrix
        return self

    def __imul__( self, matrix3 ):
        return self.transform( matrix3 )

    def __iter__( self ):
        """iterate through individual float values of matrix
        """
        for i in range( 4 ):
            for j in range( 4 ):
                yield self._matrix[i, j]

    def _get_position( self ):
        return Vector3( self._matrix[:3,3].A1 )

    def _get_angle_axis( self ):
        # from http://en.wikipedia.org/wiki/Axis_angle
        # calculate trace of 3x3 rotation matrix and use to calculate angle
        t = self._matrix[:3,:3].trace().item()
        angle = math.acos((t - 1) / 2)

        # if angle is zero return zeros for axis, too
        if abs(angle) < self.EPSILON:
            return( 0.0, Vector3((0.0, 0.0, 0.0)) )

        # calculate raw axis
        axis = Vector3( (self._matrix[2,1] - self._matrix[1,2],
                         self._matrix[0,2] - self._matrix[2,0],
                         self._matrix[1,0] - self._matrix[0,1]) ).normalize()

        # convert angle to degrees
        angle = math.degrees( angle )
         
        return angle, axis
        
    position = property( fget=_get_position,
                         doc="current (x, y, z) position vector of matrix" )
    angle_axis = property( fget=_get_angle_axis,
                           doc="current (a, x, y, z) rotation of matrix" )
