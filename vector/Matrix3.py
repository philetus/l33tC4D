from numpy import eye, matrix
from math import cos, sin, radians

class Matrix3:
    """4x4 matrix for transformations of 3d vectors
    """
    __slots__ = "_m" # instances only store numpy matrix
    
    def __init__( self, seed=None ):
        """default to 4x4 identity matrix
        """
        if seed is None:
            self._m = matrix( eye(4, 4) )
        else:
            self._m = matrix( seed )
            if self._m.shape != (4, 4):
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
        x, y, z = (coord / magnitude for coord in axis)
        c = cos( radians(degrees) )
        s = sin( radians(degrees) )
        m = matrix( [[(x*x*(1-c))+c, (x*y*(1-c))-(z*s), (x*z*(1-c))+(y*s), 0],
                     [(y*x*(1-c))+(z*s), (y*y*(1-c))+c, (y*z*(1-c))-(x*s), 0],
                     [(x*z*(1-c))-(y*s), (y*z*(1-c))+(x*s), (z*z*(1-c))+c, 0],
                     [0, 0, 0, 1]],
                    'd' )

        # multiply rotation matrix with current matrix
        self._m *= m

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
        self._m *= m

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
        self._m *= m

        return self

    def __imul__( self, matrix3 ):
        """multiply this transformation matrix by another
        """
        self._m *= matrix3._m
        return self

    def __iter__( self ):
        """iterate through individual float values of matrix
        """
        for i in range( 4 ):
            for j in range( 4 ):
                yield self._m[i, j]

    def _get_position( self ):
        return tuple(self._m[:3,3].A1)

    position = property( fget=_get_position,
                         doc="current (x, y, z) position of matrix" )
