import unittest

from Vector3 import Vector3
from matrices import angle_axis, yaw, pitch, roll

class Test_matrices(unittest.TestCase):
    
    def setUp(self):
        self.x = Vector3( 1, 0, 0 )
        self.y = Vector3( 0, 1, 0 )
        self.z = Vector3( 0, 0, 1 )
        self.a = Vector3( 2, 1, 0 )
        self.b = Vector3( 5, 3, 1.5 )

    def test_angle_axis( self ):
        """rotate test vectors around each axis and test that they come
           back to where they started
        """
        for vector in self.a, self.b:
            for axis in (self.x, self.y, self.z):
                t = vector
                rotation = angle_axis( 30, *axis )
                for i in range( 12 ):
                    t = t.transform( rotation )

                # check that t ~= vector
                for ct, cv in zip( t, vector ):
                    self.assert_( abs(ct-cv) < 0.001 )

    def test_yaw_pitch_roll( self ):
        """
        """
        for r in range( 0, 360, 30 ):
            for p in range( 0, 360, 30 ):
                for y in range( 0, 360, 30 ):
                    t = self.b
                    there = yaw( 30 ) * pitch( 30 ) * roll( 30 )
                    back = roll( -30 ) * pitch( -30 ) * yaw( -30 )

                    t = t.transform( there )
                    t = t.transform( back )
                    
                    # check that t ~= self.b
                    for ct, cv in zip( t, self.b ):
                        self.assert_( abs(ct-cv) < 0.001 )

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_matrices)
    unittest.TextTestRunner(verbosity=2).run(suite)

