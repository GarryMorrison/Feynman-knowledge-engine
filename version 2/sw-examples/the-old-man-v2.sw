
current |person> => |old man>
learn-person |*> #=> learn(|op: current>, |person>, |_self>)

adjectives |old man> => 10|crotchety> + 8|grumpy> + 5|friendly> + |kindly> + 0.2|sleepy>
comma |old man> => |,>

adjectives |old woman> => 2|kindly> + |sleepy> + |pleasant> + |strange>
comma |old woman> => |,>

adjectives |teenager> => |enthusiastic> + |energetic>
comma |teenager> #=> |>

pick-adjective |*> #=> clean weighted-pick-elt adjectives |_self>

adjective-0 |*> #=> |>
adjective-1 |*> #=> ( pick-adjective _ comma ) |_self>
adjective-2 |*> #=> ( pick-adjective . pick-adjective _ comma ) |_self>
adjective-3 |*> #=> ( pick-adjective . pick-adjective . pick-adjective _ comma ) |_self>
choose-number-of |adjectives> #=> clean weighted-pick-elt (8|op: adjective-0> + 2|op: adjective-1> + 0.5|op: adjective-2> + 0.2|op: adjective-3> )

adjective-list |*> #=> smerge[", "] apply( choose-number-of |adjectives>, |_self> )

the-sentence |*> #=> smerge[" "] sdrop (|The> . adjective-list |_self> . |_self> _ |.>)

sentence |*> #=> the-sentence pick-elt (|old man> + |old woman> + |teenager>)


