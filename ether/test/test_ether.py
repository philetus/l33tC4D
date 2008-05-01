from l33tC4D.ether.Ether_Demon import Ether_Demon
from l33tC4D.ether.Box import Box

# start ether demon
ether_demon = Ether_Demon()
ether_demon.start()

# make a box
box = Box( position=(10, 6, 0), size=5 )

# insert it into ether
print "inserted box into ether: %s" % str( ether_demon.insert(box) )

# make another box
box_x = Box( position=(10, 3, 0), size=5 )

# insert it too
print "inserted box x into ether: %s" % str( ether_demon.insert(box_x) )

# move box x and try again
box_x.position._coords[1,0] = -5
print "inserted box x into ether: %s" % str( ether_demon.insert(box_x) )

# remove box
print "removed box from ether: %s" % str( ether_demon.remove(box) )
