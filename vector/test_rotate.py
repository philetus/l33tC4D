from numpy import matrix, identity
from scipy.special import cosdg, sindg

def rot_x_matrix( degrees ):
    r = identity( 3, 'd' )
    r[1][1] = cosdg( degrees )
    r[1][2] = -sindg( degrees )
    r[2][1] = sindg( degrees )
    r[2][2] = cosdg( degrees )

    return r

def rot_y_matrix( degrees ):
    r = identity( 3, 'd' )
    r[0][0] = cosdg( degrees )
    r[0][2] = sindg( degrees )
    r[2][0] = -sindg( degrees )
    r[2][2] = cosdg( degrees )

    return r

def rot_z_matrix( degrees ):
    r = identity( 3, 'd' )
    r[0][0] = cosdg( degrees )
    r[0][1] = -sindg( degrees )
    r[1][0] = sindg( degrees )
    r[1][1] = cosdg( degrees )

    return r

u = matrix( [1,0,0], 'd' ).transpose()
v = matrix( [0,1,0], 'd' ).transpose()
