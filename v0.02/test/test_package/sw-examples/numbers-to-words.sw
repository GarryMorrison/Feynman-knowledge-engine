n2w |0> #=> |>
n2w |1> => |one>
n2w |2> => |two>
n2w |3> => |three>
n2w |4> => |four>
n2w |5> => |five>
n2w |6> => |six>
n2w |7> => |seven>
n2w |8> => |eight>
n2w |9> => |nine>
n2w |10> => |ten>
n2w |11> => |eleven>
n2w |12> => |twelve>
n2w |13> => |thirteen>
n2w |14> => |fourteen>
n2w |15> => |fifteen>
n2w |16> => |sixteen>
n2w |17> => |seventeen>
n2w |18> => |eighteen>
n2w |19> => |nineteen>
n2w |20> => |twenty>
n2w |30> => |thirty>
n2w |40> => |forty>
n2w |50> => |fifty>
n2w |60> => |sixty>
n2w |70> => |seventy>
n2w |80> => |eighty>
n2w |90> => |ninety>

big-n2w |3> => |hundred>
big-n2w |4> => |thousand>
big-n2w |6> => |million>

learn-number |*> #=> learn(|op: current>, |number>, |_self>)
n2w |*> #=> general-n2w extract-value ket-length learn-number |_self>

general-n2w |1> #=> n2w current |number>
general-n2w |2> #=> n2w times-by[10] int-divide-by[10] current |number> __ n2w mod[10] current |number>
general-n2w |3> #=> smerge[" and "] sdrop (n2w int-divide-by[100] current |number> __ |hundred> . n2w mod[100] current |number> )
general-n2w |4> #=> n2w int-divide-by[1000] current |number> __ |thousand> __ n2w mod[1000] current |number>


hundred-rule |*> #=> smerge[" "] sdrop (n2w select-char[-3] |_self> . big-n2w ket-length current |_self>)
thousand-rule |*> #=> smerge[" "] sdrop (n2w select-char[-4] |_self> . big-n2w ket-length current |_self>)
million-rule |*> #=> smerge[" "] sdrop (n2w select-char[-6] |_self> . big-n2w ket-length current |_self>)

general-n2w |1> #=> n2w current |number>
general-n2w |2> #=> smerge[" "] sdrop n2w ( times-by[10] select-char[-2] current |number> . select-char[-1] current |number> )
general-n2w |3> #=> smerge[" and "] sdrop ( hundred-rule current |number> . n2w mod[100] current |number> )
general-n2w |4> #=> smerge[", "] sdrop ( thousand-rule current |number> . n2w mod[1000] current |number> )


