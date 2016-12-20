#!/usr/bin/env python

sign = lambda a: (a>0) - (a<0)

mu0bar = int("10"*20, 2)

def succ(alpha,inc=1): 
    # for successor: succ(alpha,1), predecessor: succ(alpha,-1)
    x = alpha
    y = x ^ mu0bar
    z = y ^ (y + inc)
    z = z | (x & (z << 1))
    w = x ^ z ^ ((z+1) >> 2)
    return w

class Tile:
    def __init__(self,alpha,y = 0):
        self.alpha = alpha
        self.y = y
    def __str__(self):
        return "("+format(self.alpha,'b')+","+str(self.y)+")"
    def n(self):
        pass


    def neighbours(self):
        north = self.alpha >> 2
        south = self.alpha << 2
        east = succ(south,+1)
        west = succ(south,-1)
        if ((self.alpha & 1) == 1):
            other = succ(north,1)
        else:
            other = succ(west,-1)

        delta_north = (self.alpha == 0)
        delta_south = -(self.alpha == 0)
        delta_east = 0
        delta_west = - (self.alpha == 1)
        if ((self.alpha & 1) == 1):
            delta_other = sign(other - north) * ((other & north) == 0)
        else:
            delta_other = sign(other - west) * ((other & west) == 0)


        return  (Tile(north, self.y + delta_north),
                Tile(west,  self.y + delta_west),
                Tile(east,  self.y + delta_east),
                Tile(south, self.y + delta_south),
                Tile(other, self.y + delta_other)
                )


#t = Tile(0b1001,1)
#for nt in t.neighbours():
#    print nt
