import unittest

from l33tC4D.space.Space import Space
from l33tC4D.space.Vertex import Vertex
from l33tC4D.space.Edge import Edge

class Test_Space( unittest.TestCase ):
    """tests space octree
    """

    def setUp( self ):
        self.space = Space( size=2.0**8 )

    def test_vertex( self ):
        """test inserting a vertex into space octree and then interfering with
           another vertex
        """
        self.a = Vertex( 3, 4, 5 )

        self.space.insert( self.a, limit=2.0**6 )

        self.b = Vertex( 3, 4, 3 )

        # check that kissing set contains a until limit is below 8
        kissed, contained = self.space.interfere( zone=self.b, limit=2.0**8 )
        self.assert_( len(contained) == 0 )
        self.assert_( self.a in kissed )

        kissed, contained = self.space.interfere( zone=self.b, limit=2.0**6 )
        self.assert_( len(contained) == 0 )
        self.assert_( self.a in kissed )

        kissed, contained = self.space.interfere( zone=self.b, limit=2.0**3 )
        self.assert_( len(contained) == 0 )
        self.assert_( self.a in kissed )

        kissed, contained = self.space.interfere( zone=self.b, limit=2**2 )
        self.assert_( len(contained) == 0 )
        self.assert_( self.a not in kissed )


    def test_prune( self ):
        """test pruning a tree
        """
        pass

    def test_edge( self ):
        """test interfering an edge with a space with some vertices
        """
        self.a = Vertex( 0, 0, 0 )
        self.b = Vertex( 0, 1, 10 )
        self.ab = Edge( self.a, self.b )
        
        self.c = Vertex( 0, 1, 1 )
        self.space.insert( self.c, limit=2.0**2 )
        
        self.d = Vertex( 0, 6, 10 )
        self.space.insert( self.d )

        kissed, contained = self.space.interfere( zone=self.ab, limit=2.0**3 )
        self.assert_( len(contained) == 0 )
        print "kissed at 2**3", kissed
        self.assert_( self.c in kissed )
        self.assert_( self.d in kissed )

        kissed, contained = self.space.interfere( zone=self.ab, limit=2.0**2 )
        self.assert_( len(contained) == 0 )
        print "kissed at 2**2", kissed
        self.assert_( self.c in kissed )
        self.assert_( self.d not in kissed )

        kissed, contained = self.space.interfere( zone=self.ab, limit=2.0**-1 )
        self.assert_( len(contained) == 0 )
        print "kissed at 2**-1", kissed
        self.assert_( len(kissed) == 0 )

        self.space.prune()
        self.space.print_tree()


if __name__ == '__main__':
    unittest.main()

