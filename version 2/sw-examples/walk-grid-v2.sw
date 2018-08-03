-- learn and randomly walk a grid

-- learn map:
|null> => learn-map[30,30] 

-- learn current location:
current |cell> => |grid: 1: 22>

-- define turn-right operator:
turn-right |op: S> => |op: W>
turn-right |op: SW> => |op: NW>
turn-right |op: W> => |op: N>
turn-right |op: NW> => |op: NE>
turn-right |op: N> => |op: E>
turn-right |op: NE> => |op: SE>
turn-right |op: E> => |op: S>
turn-right |op: SE> => |op: SW>

-- define walk direction:
heading |ops> => 0.25|op: SW> + |op: S> + 0.25|op: SE>
-- heading |ops> => |op: S>
next |*> #=> set-to[1] apply(weighted-pick-elt heading |ops>, |_self>)

-- define turn-heading-right operator:
turn-heading-right |*> #=> learn(|op: heading>, |ops>, turn-right heading |ops>)

-- define step operator:
step |*> #=> process-if if(do-you-know next |_self>, |valid step:> __ |_self>, |not valid step:> __ |_self>)
process-if |valid step: *> #=> next remove-leading-category |_self>
process-if |not valid step: *> #=> sselect[1,1] (remove-leading-category |_self> . turn-heading-right |>)
-- process-if |not valid step: *> #=> sdrop (remove-leading-category |_self> . set-to[0] turn-heading-right |>)

-- update-map operators (increment current spot, take a step, and display map):
inc |*> #=> learn(|op: value>, current |cell>, plus[1] value current |cell>)
n |*> #=> learn(|op: current>, |cell>, step current |cell>)
d |*> #=> display-map[30,30]


-- single map update:
line |*> #=> inc |_self> . n |_self> . d |_self>

-- set max steps:
max |steps> => |30>

-- walk max steps:
walk |*> #=> sdrop set-to[0] line sp2seq range(|1>, max |steps>)

