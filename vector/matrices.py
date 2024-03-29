from numpy import matrix
from math import sqrt, radians, cos, sin

def angle_axis( angle, u, v, w ):
    """builds a 4d numpy matrix to rotate angle degrees around given axis

       angle - angle to rotate in degrees
    """
    ###
    ### from http://www.mines.edu/~gmurray/ArbitraryAxisRotation/ArbitraryAxisRotation.html
    ###
    c = cos( radians(angle) )
    s = sin( radians(angle) )
    t = 1 - c
    u2, v2, w2 = u**2, v**2, w**2
    d = u2 + v2 + w2
    root = sqrt( d )
    
    # generate rotation matrix
    return matrix(
        [[(u2+((v2+w2)*c))/d, (u*v*t-w*root*s)/d, (u*w*t+v*root*s)/d, 0],
         [(u*v*t+w*root*s)/d, (v2+((u2+w2)*c))/d, (v*w*t-u*root*s)/d, 0],
         [(u*w*t-v*root*s)/d, (v*w*t+u*root*s)/d, (w2+((u2+v2)*c))/d, 0],
         [0, 0, 0, 1]],
        'd' )

def translate_matrix( x, y, z ):
    """builds 4d numpy matrix for translation given distance in x, y and z
    """
    return matrix(
        [[1, 0, 0, x],
         [0, 1, 0, y],
         [0, 0, 1, z],
         [0, 0, 0, 1]],
        'd' )

def scale_matrix( x, y, z ):
    """builds 4d numpy matrix for non-uniform scaling in x, y and z
    """
    return matrix(
        [[x, 0, 0, 0],
         [0, y, 0, 0],
         [0, 0, z, 0],
         [0, 0, 0, 1]],
        'd' )

def roll( angle ):
    """builds 4d numpy matrix for rotation about x axis
    """
    angle = radians( float(angle) )
    c = cos( angle )
    s = sin( angle )
    return matrix(
        [[1, 0, 0, 0],
         [0, c, -s, 0],
         [0, s, c, 0],
         [0, 0, 0, 1]],
        'd' )

def pitch( angle ):
    """builds 4d numpy matrix for rotation about y axis
    """
    angle = radians( float(angle) )
    c = cos( angle )
    s = sin( angle )
    return matrix(
        [[c, 0, s, 0],
         [0, 1, 0, 0],
         [-s, 0, c, 0],
         [0, 0, 0, 1]],
        'd' )

def yaw( angle ):
    """builds 4d numpy matrix for rotation about z axis
    """
    angle = radians( float(angle) )
    c = cos( angle )
    s = sin( angle )
    return matrix(
        [[c, -s, 0, 0],
         [s, c, 0, 0],
         [0, 0, 1, 0],
         [0, 0, 0, 1]],
        'd' )

def roll_pitch_yaw( r, p, y ):
    """builds 4d numpy matrix for roll > pitch > yaw rotation
    """
    return yaw( y ) * pitch( p ) * roll( r )

def yaw_pitch_roll( r, p, y ):
    """builds 4d numpy matrix for yaw > pitch > roll rotation
    """
    return roll( r ) * pitch( p ) * yaw( y )

def pitch_yaw_roll( r, p, y ):
    """builds 4d numpy matrix for pitch > yaw > roll rotation
    """
    return roll( r ) * yaw( y ) * pitch( p )

