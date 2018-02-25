current |person> => |old man>
learn-person |*> #=> learn(|op: current>, |person>, |_self>)

adjectives |old man> => 10|crotchety> + 8|grumpy> + 5|friendly> + |kindly> + 0.2|sleepy>
adjectives |old woman> => 2|kindly> + |sleepy> + |pleasant> + |strange>
adjectives |teenager> => |enthusiastic> + |energetic>

pick-adjective (*) #=> clean weighted-pick-elt adjectives |_self>
how-many-adjectives |*> #=> clean weighted-pick-elt (8|0> + 2|1> + 0.5|2>)

insert-adjective |*> #=> |>
insert-adjective |1> #=> pick-adjective current |person> _ | >
insert-adjective |2> #=> smerge[", "] (pick-adjective current |person> . pick-adjective current |person>) _ | >
insert-adjective |3> #=> smerge[", "] (pick-adjective current |person> . pick-adjective current |person> . pick-adjective current |person>) _ | >

adjective-list |*> #=> insert-adjective how-many-adjectives learn-person |_self>

the-sentence |*> #=> |The > _ adjective-list |_self> _ |_self> _ |.>

sentence |*> #=> the-sentence pick-elt (|old man> + |old woman> + |teenager>)

