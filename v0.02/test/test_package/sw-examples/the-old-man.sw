
current |person> => |old man>
learn-person |*> #=> learn(|op: current>, |person>, |_self>)

adjectives |old man> => 10|crotchety> + 8|grumpy> + 5|friendly> + |kindly> + 0.2|sleepy>
adjectives |old woman> => 2|kindly> + |sleepy> + |pleasant> + |strange>
adjectives |teenager> => |enthusiastic> + |energetic>

pick-adjective (*) #=> clean weighted-pick-elt adjectives |_self>
how-many-adjectives |*> #=> clean weighted-pick-elt (8|0> + 2|1> + 0.5|2> + 0.2|3>)

insert-adjective |*> #=> |>
insert-adjective |1> #=> pick-adjective current |person>
insert-adjective |2> #=> pick-adjective current |person> . pick-adjective current |person>
insert-adjective |3> #=> pick-adjective current |person> . pick-adjective current |person> . pick-adjective current |person>
  
adjective-list |*> #=> smerge[", "] insert-adjective how-many-adjectives learn-person |_self>

the-sentence |*> #=> smerge[" "] sdrop (|The> . adjective-list |_self> . |_self> _ |.>)

sentence |*> #=> the-sentence pick-elt (|old man> + |old woman> + |teenager>)

