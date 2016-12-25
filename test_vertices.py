import pentagrid as g

a = [ g.Tile("1000"), g.Tile("101001"), g.Tile("10"), g.Tile("1010") ]

v = g.Vertex(a)

print v

t = g.Tile(0b1000)

ns =  t.neighbours()

print ns[0].__hash__()

print

t = g.Tile(0)
print map( lambda x: str(x), t.adjacent())



for i in range(-15,15):
    
    print i, format(g.negaencode(i),"b")

o = g.origin
print o.transformation()
print o.position()

t = g.Tile(0b10010100,-8)
print t
print t.adjacent()
p = t.moveTowardsOrigin()[0]
print p
print p.adjacent()
a = p.adjacent()[3]

print a,t
print g.negadecode(49),g.negadecode(54)
print a.alpha,t.alpha,a.y,t.y

print t.transformation()
print t.position()

