-- learn and randomly walk a grid:

-- learn map:
|null> => learn-map[30,30] 

-- learn current location:
current |cell> => |grid: 1: 22>

-- define walk direction:
direction |ops> => |op: SW> + |op: S> + |op: SE>
direction |ops> => |op: W> + |op: SW> + |op: S> + |op: SE> + |op: E>
next |*> #=> apply(pick-elt direction |ops>, |_self>)

-- update-map operators:
i |*> #=> learn(|op: value>, current |cell>, plus[1] value current |cell>)
n |*> #=> learn(|op: current>, |cell>, next current |cell>)
d |*> #=> display-map[30,30]


-- single map update:
line |*> #=> i |_self> . n |_self> . d |_self>

-- set max steps:
max |steps> => |30>

-- walk max steps:
walk |*> #=> sdrop set-to[0] line sp2seq range(|1>, max |steps>)

