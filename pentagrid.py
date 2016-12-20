#!/usr/bin/env python

sign = lambda a: (a>0) - (a<0)

mu0bar = int("10"*32, 2)

def succ(alpha,inc=1): 
    # for successor: succ(alpha,1), predecessor: succ(alpha,-1)
    x = alpha
    y = x ^ mu0bar
    z = y ^ (y + inc)
    z = z | (x & (z << 1))
    w = x ^ z ^ ((z+1) >> 2)
    return w

class Node:
    pass

class Tile(Node):
    def __init__(self,alpha,y = 0):
        if isinstance(alpha,basestring):
            self.alpha = int(alpha,2)
        else:
            self.alpha = alpha
        self.y = y
    def inStr(self):
        return format(self.alpha,'b')+","+str(self.y)
    def __str__(self):
        return "("+self.inStr()+")"
    def __repr__(self):
        return "Tile(0b"+self.inStr()+")"
    def n(self):
        pass


    def adjacent(self):
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
                Tile(east,  self.y + delta_east),
                Tile(south, self.y + delta_south),
                Tile(west,  self.y + delta_west),
                Tile(other, self.y + delta_other)
                )

    def neighbours(self):
        adj = self.adjacent()
        if (self.alpha & 1) == 1:
            adj = [ adj[0], adj[4], adj[1], adj[2], adj[3] ]
        out = []
        for i in range(5):
            a = adj[i]
            b = adj[(i+1)%5]

            c_candidates = [ e for e in a.adjacent() if (e in b.adjacent()) and not (e == self) ]
            assert len(c_candidates) == 1 
            c = c_candidates[0]
            
            out.append(Vertex([a,b,c,self]))
        return out
    
    def __eq__(self,other):
        if isinstance(other,Tile):
            return (self.alpha == other.alpha) and (self.y == other.y)
        else:
            return False
    def __neq__(self,other):
        return not self.__eq__(other)
    def __hash__(self):
        return hash((self.alpha,self.y))
    def __cmp__(self,other):
        if self.alpha == other.alpha:
            return sign(self.y - other.y)
        else:
            return sign(self.alpha - other.alpha)

class Vertex(Node):
    def __init__(self,faces):
        self.faces = sorted(faces)
    def neighbours(self):
        return self.faces
    def __eq__(self,other):
        if isinstance(other,Vertex):
            return self.faces == other.faces
        else:
            return False
    def __neq__(self,other):
        return not self.__eq__(other)
    def __hash__(self):
        return hash((45,tuple(self.faces)))
    def __str__(self):
        return "["+"|".join(map(str, self.faces) ) + "]"
    def __repr__(self):
        return "Vertex(["+",".join(map(str,self.faces))+"])"
