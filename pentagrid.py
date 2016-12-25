#!/usr/bin/env python

from math import frexp
import numpy as np

# Math utilities

sign = lambda a: (a>0) - (a<0)

# memoized Fibonacci sequence

def memoize(f):
    cache = {}
    return lambda *args: cache[args] if args in cache else cache.update({args: f(*args)}) or cache[args]

@memoize
def fib(n):
    return n if n < 2 else fib(n-2) + fib(n-1)

# negaFibonacci

def negafib(n):
    # F_(-n) = (-1)^(n+1) F_n
    return ( 2*(n % 2 ) - 1 ) * fib(n)

# magic number 0b101010...10

mu0bar = int("10"*32, 2)

# negaFibonacci code

def negadecode(code):
    #decode negaFibonacci code
    length = frexp(code)[1]
    out = 0
    for i in range(length):
        if ((code >> i) & 1):
            out += negafib(i+1)
    return out

def negaencode(n):
    #encode n as sum of negaFibonacci
    if n==0:
        return 0

    nabs = abs(n)

    S = 0
    i = (1 if n>0 else 0)
    #bits = 0
    while (S < nabs):
        S += fib(i)
        i += 2
    #    bits += 1

    i-= 2

    k = negafib(i)
    
    m = n - k


    assert(abs(m) < abs(n))

    output = (1 << i-1) + negaencode(m)

    return output
    
           


# successor and predecessor as in Knuth

def succ(alpha,inc=1): 
    # for successor: succ(alpha,1), predecessor: succ(alpha,-1)
    x = alpha
    y = x ^ mu0bar
    z = y ^ (y + inc)
    z = z | (x & (z << 1))
    w = x ^ z ^ ((z+1) >> 2)
    return w

# cardinal directions

NORTH   = 0
EAST    = 1
SOUTH   = 2
WEST    = 3
OTHER   = 4

negate_direction = {
        SOUTH: NORTH,
        EAST: EAST,
        NORTH: SOUTH,
        OTHER: WEST,
        WEST: OTHER
        }

# some hyperboloid math

y = np.sqrt( 1 + 2*np.sqrt(5) - 2*np.sqrt(5 + np.sqrt(5))) # ask wolframalpha

step = np.array([(1+y*y)/(1-y*y) , 2*y/(1-y*y) , 0])

# Lorentz boost given the target 3-vector
def boost(a):
    return np.matrix([[a[0], a[1], 0],[a[1],a[0],0] ,[0,0,1]] )

flipper = np.matrix( [[1,0,0],[0,-1,0],[0,0,-1]] , dtype = np.float64)

stepper = boost(step) * flipper * (boost(step).I)


c_5,s_5 = np.cos(2*np.pi/5),np.sin(2*np.pi/5)
rotator = np.matrix( [ [1,0,0],[0,c_5,s_5],[0,-s_5,c_5] ] , dtype= np.float64)




# exceptions

class NotFibonacciException(Exception):
    pass

# the real deal

class Node:
    pass

class Tile(Node):
    def __init__(self,alpha,y = 0,validate = True):
        if isinstance(alpha,basestring):
            self.alpha = int(alpha,2)
        else:
            self.alpha = alpha

        if validate:
            for i in range(frexp(self.alpha)[1]):
                if ( 11 & (self.alpha >> i) == 11):
                    raise NotFibonacciException("The code %s (%d) is not a valid Fibonacci code. There must be no consecutive 1s"%(bin(self.alpha),self.alpha))

        self.y = y
    def inStr(self):
        return str(self.n())+","+str(self.y)
    def __str__(self):
        return "("+self.inStr()+")"
    def __repr__(self):
        return "Tile("+self.inStr()+")"
    def n(self):
        try:
            return self.N
        except AttributeError:
            self.N = negadecode(self.alpha)
            return self.N


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


        return  (Tile(north, self.y + delta_north, validate = False),
                Tile(east,  self.y + delta_east,   validate = False),
                Tile(south, self.y + delta_south,  validate = False),
                Tile(west,  self.y + delta_west,   validate = False),
                Tile(other, self.y + delta_other,  validate = False)
                )
    def moveTowardsOrigin(self):
        if self.alpha > 0:
            direction = 0
        elif self.y > 0:
            direction = 2
        elif self.y < 0:
            direction = 0
        else:
            direction = None
        if direction == None:
            return (None,NORTH)
        else:
            return (self.adjacent()[direction],direction)

    def orderedDirections(self):
        if (self.alpha & 1 ) == 1:
            return (0,4,1,2,3)
        else:
            return (0,1,2,3,4)

    def direction_towards_parent(self):
        return self.moveTowardsOrigin()[1]

    def transformation(self):
        try:
            return self.transf
        except AttributeError:

            if self == origin:
                self.transf = np.matrix(np.eye(3,dtype=np.float64))
            else:
                parent, direction_towards_parent = self.moveTowardsOrigin()
                direction_from_parent = parent.adjacent().index(self)
                ordirs = parent.orderedDirections()
                rotate_units = ordirs.index(direction_from_parent)  -  ordirs.index(parent.direction_towards_parent()) 
            #- ordirs.index(parent.moveTowardsOrigin()[1])
                

                addmatrix =  (rotator ** rotate_units) * stepper

                self.transf = parent.transformation() * addmatrix


            return self.transf

    def position(self):
        return np.squeeze(np.asarray(self.transformation().dot(np.array([1,0,0],dtype=np.float64))))

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

origin = Tile(0,0)

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
