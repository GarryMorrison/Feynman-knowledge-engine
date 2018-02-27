ones |0> #=> |>
ones |1> => |one>
ones |2> => |two>
ones |3> => |three>
ones |4> => |four>
ones |5> => |five>
ones |6> => |six>
ones |7> => |seven>
ones |8> => |eight>
ones |9> => |nine>

tens |10> => |ten>
tens |11> => |eleven>
tens |12> => |twelve>
tens |13> => |thirteen>
tens |14> => |fourteen>
tens |15> => |fifteen>
tens |16> => |sixteen>
tens |17> => |seventeen>
tens |18> => |eighteen>
tens |19> => |nineteen>

ten |20> => |twenty>
ten |30> => |thirty>
ten |40> => |forty>
ten |50> => |fifty>
ten |60> => |sixty>
ten |70> => |seventy>
ten |80> => |eighty>
ten |90> => |ninety>

tens |*> #=> smerge[" "] sdrop ( ten times-by[10] int-divide-by[10] |_self> . ones mod[10] |_self> )
hundreds-rule |*> #=> smerge[" and "] (hundreds int-divide-by[100] mod[1000] |_self> . tens mod[100] |_self>)

hundreds |0> #=> |>
hundreds |*> #=> ones |_self> __ |hundred>

thousands |0> #=> |>
thousands |*> #=> hundreds-rule |_self> __ |thousand>

millions |0> #=> |>
millions |*> #=> hundreds-rule |_self> __ |million>

n2w |0> => |zero>
n2w |*> #=> smerge[", "] sdrop (millions int-divide-by[1000000] mod[1000000000] |_self> . thousands int-divide-by[1000] mod[1000000] |_self> . hundreds-rule |_self>)


