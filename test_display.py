import matplotlib.pyplot as plt
from scipy.misc import imread
import numpy as np

fig = plt.figure()

ax = fig.add_subplot(111)

import pentagrid as grid

tiles = [grid.origin]

i = 0
while len(tiles) < 50:
    for n in tiles[i].adjacent():
#        if not n.y in [0,1,-1]:
#            continue
        if not n in tiles:
            while not n.moveTowardsOrigin()[0] in tiles:
                n = n.moveTowardsOrigin()[0]
            tiles.append(n)
    i += 1

for t in tiles:
    pos_hyper = t.position()
    pos_disk = pos_hyper[1:]/(1+pos_hyper[0])
    size = int(90./pos_hyper[0])
    ax.text(pos_disk[0],pos_disk[1],str(t) , va = "center", ha = "center",size=size)
    print t, t.transformation()


print grid.origin.adjacent()

two = grid.Tile(0b1001,1)
print two

print two.moveTowardsOrigin()[0]

print grid.Tile(0b1,0).adjacent()
print grid.Tile(0,1).adjacent()

img = imread(open("tiling.png",'r'))

plt.imshow(img, extent=[-1,1,-1,1])

ax.axis([-1,1,-1,1])
plt.show()

