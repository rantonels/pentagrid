import pentagrid as g

a = [ g.Tile("1000"), g.Tile("101001"), g.Tile("10"), g.Tile("1010") ]

v = g.Vertex(a)

print v

t = g.Tile(0b1000)

ns =  t.neighbours()

print ns[0].__hash__()
