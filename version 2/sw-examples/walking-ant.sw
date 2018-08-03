-- learn and randomly walk a grid
-- keep a record of the pathway home
-- if find food return home, leaving a scent trail
-- once home, follow scent trail back to food (approximately)
-- if find food again, return home, adding to the scent trail
-- when food is gone, switch off scent trail, and start randomly walking again

-- need three walk types:
-- randomly
-- return home
-- follow scent trail

-- learn map:
|null> => learn-map[30,30] 

-- learn current location:
current |cell> => |grid: 10: 22>

-- learn home location:
home |cell> => current |cell>

-- start with no food:
stored-food home |cell> => |0>

-- learn path home:
learn-current-direction |*> #=> add-learn(|op: path>, |home>, |_self>)

-- find return path
return-path |home> #=> subtraction-invert[0] expand path |home>

-- place some food:
food |grid: 2: 2> => |3>
food |grid: 2: 3> => |3>
food |grid: 2: 4> => |3>
food |grid: 2: 5> => |3>
food |grid: 3: 5> => |3>
food |grid: 4: 5> => |3>
food |grid: 5: 6> => |3>
food |grid: 6: 6> => |3>
food |grid: 29: 29> => |20>
food |grid: 28: 3> => |20>

show-food |*> #=> display-map[30, 30, food] |>
tally-stored-food |*> #=> merge-value stored-food |_self>
show-stored-food |*> #=> display-map[30, 30, tally-stored-food] |>

carry-the |food> #=> learn(|op: carry>, |food>, plus[1] carry |food>) learn(|op: food>, current |cell>, minus[1] food current |cell> )
drop-the |food> #=> learn(|op: carry>, |food>, |0>) add-learn(|op: stored-food>, current |cell>, carry |food> )
-- drop |food> #=> add-learn(|op: stored-food>, current |cell>, carry |food> ) . learn(|op: carry>, |food>, |0>)

-- if-find-food |*> #=> process-if if(is-greater-than[0] food current |cell>, |found food>, |not found food> )
if-find-food |*> #=> process-if if( and(is-greater-than[0] food current |cell>, is-equal[0] carry |food>), |found food>, |not found food> )
process-if |found food> #=> carry-the |food> . switch-on-scent |> . switch-on-return |>
process-if |not found food> #=> |>

-- start by not carrying any food:
carry |food> => |0>

-- reach home operator:
if-reach-home |*> #=> process-if sdrop wif(equal( current |cell>, home |cell>), |reached home>, |not reached home>)
process-if |reached home> #=> drop-the |food> . switch-off-scent |> . switch-on-random |>
process-if |not reached home> #=> |>


-- start with scent trail off:
lay |scent> => |no>
switch-on-scent |*> #=> learn(|op: lay>, |scent>, |yes>)
switch-off-scent |*> #=> learn(|op: lay>, |scent>, |no>)
apply-scent |*> #=> learn(|op: value>, current |cell>, plus[1] value current |cell>)
scent |*> #=> process-if if(lay |scent>, |yes to scent>, |no to scent>)
process-if |yes to scent> #=> apply-scent |>
process-if |no to scent> #=> |>

-- start with random walk type:
type |walk> => |op: random-walk>
switch-on-random |*> #=> learn(|op: type>, |walk>, |op: random-walk>)
switch-on-return |*> #=> learn(|op: type>, |walk>, |op: return-home>)
-- switch-on-follow |*> #=> learn(|op: type>, |walk>, |op: follow-scent>)
take-step |*> #=> if-reach-home if-find-food learn(|op: current>, |cell>, apply( type |walk>, current |cell>))

random-walk |*> #=> if-find-scent process-if if(do-you-know try-random-walk |_self>, |valid step:> __ |_self>, |not valid step:> __ |_self>)
process-if |valid step: *> #=> apply(learn-current-direction next |direction>, remove-leading-category |_self>)
process-if |not valid step: *> #=> sselect[1,1] (remove-leading-category |_self> . turn-heading-right |>)

try-random-walk |*> #=> apply(random-next |direction>, |_self>)
-- random-next |direction> #=> learn-next-direction clean weighted-pick-elt ( 0.1 turn-left^2 + 0.25 turn-left + 1 + 0.25 turn-right + 0.1 turn-right^2 ) heading |ops>
random-next |direction> #=> learn-next-direction clean weighted-pick-elt ( 0.1 turn-left^2 + 0.25 turn-left + 1 + 0.25 turn-right + 0.1 turn-right^2 ) blur-heading heading |ops>
learn-next-direction |*> #=> learn(|op: next>, |direction>, |_self>)

-- define turn-heading-right operator:
turn-heading-right |*> #=> learn(|op: heading>, |ops>, pick-elt ( turn-right + turn-right^2 ) heading |ops>)

-- define blur-heading operator:
blur-heading |*> #=> learn(|op: heading>, |ops>, clean weighted-pick-elt ( 0.1 turn-left^2 + 0.25 turn-left + 10 + 0.25 turn-right + 0.1 turn-right^2 ) heading |ops>)


if-find-scent |*> #=> process-if if(is-greater-than[0] value current |cell>, |found scent:> __ |_self> , |not found scent:> __ |_self>)
process-if |found scent: *> #=> sselect[1,1] ( remove-leading-category |_self> . learn(|op: heading>, |ops>, random-if-zero reverse-if-neg push-float reverse-dir return-path |home> ) )
process-if |not found scent: *> #=> remove-leading-category |_self>

random-if-zero (*) #=> if(do-you-know sdrop |_self>, |_self>, pick-elt list-of |directions>)

-- define return home operator:
-- return-path |home>
--   17|op: N> + 21|op: E>
return-home |*> #=> apply(learn-current-direction return-next |direction>, |_self>)
return-next |direction> #=> learn-next-direction drop clean weighted-pick-elt reverse-if-neg push-float return-path |home>
-- return-next |direction> #=> learn-next-direction drop clean weighted-pick-elt reverse-if-neg push-float ( 0.25 turn-left + 1 + 0.25 turn-right ) return-path |home>
-- return-next |direction> #=> learn-next-direction drop clean weighted-pick-elt reverse-if-neg push-float ( 0.1 turn-left + 1 + 0.1 turn-right ) return-path |home>
-- return-next |direction> #=> learn-next-direction drop clean weighted-pick-elt reverse-if-neg push-float ( 0.02 turn-left + 1 + 0.02 turn-right ) return-path |home>
reverse-if-neg |*> #=> if(is-greater-equal-than[0] |_self>, pop-float |_self>, - reverse-dir pop-float |_self>)

-- define follow scent operator:
follow-scent |*> #=> apply(learn-current-direction follow-next |direction>, |_self>)
-- weight-directions |*> #=> algebra(value apply( |_self>, current |cell>), |*>, |_self>)
nghbr |*> #=> (N + NE + E + SE + S + SW + W + NW) |_self>
weight-directions |*> #=> algebra(push-float pop-float value apply( |_self>, clean ( 1 + nghbr + nghbr^2 ) current |cell>), |*>, |_self>)


-- follow-next |direction> #=> learn-next-direction clean weighted-pick-elt ( 0.25 turn-left + 1 + 0.25 turn-right ) weight-directions list-of |directions>
-- follow-next |direction> #=> learn-next-direction clean pick-elt drop ( 0.25 turn-left + 1 + 0.25 turn-right ) weight-directions list-of |directions>
-- follow-next |direction> #=> learn-next-direction clean pick-elt drop weight-directions list-of |directions>
follow-next |direction> #=> learn-next-direction clean weighted-pick-elt ( 0.1 turn-left^2 + 0.25 turn-left + 1 + 0.25 turn-right + 0.1 turn-right^2 )  heading |ops>

-- choose a heading when leaving the nest:
list-of |directions> => |op: N> + |op: NE> + |op: E> + |op: SE> + |op: S> + |op: SW> + |op: W> + |op: NW>
choose-heading |*> #=> learn(|op: heading>, |ops>, pick-elt list-of |directions>)
|null> => choose-heading |>

-- define turn-right operators:
turn-right |op: S> => |op: SW>
turn-right |op: SW> => |op: W>
turn-right |op: W> => |op: NW>
turn-right |op: NW> => |op: N>
turn-right |op: N> => |op: NE>
turn-right |op: NE> => |op: E>
turn-right |op: E> => |op: SE>
turn-right |op: SE> => |op: S>

-- define turn-left operators:
turn-left |op: S> => |op: SE>
turn-left |op: SW> => |op: S>
turn-left |op: W> => |op: SW>
turn-left |op: NW> => |op: W>
turn-left |op: N> => |op: NW>
turn-left |op: NE> => |op: N>
turn-left |op: E> => |op: NE>
turn-left |op: SE> => |op: E>

-- define reverse operators:
reverse-dir |op: S> => |op: N>
reverse-dir |op: SW> => |op: NE>
reverse-dir |op: W> => |op: E>
reverse-dir |op: NW> => |op: SE>
reverse-dir |op: N> => |op: S>
reverse-dir |op: NE> => |op: SW>
reverse-dir |op: E> => |op: W>
reverse-dir |op: SE> => |op: NW>

-- define expand operators:
expand |op: S> => - |op: N>
expand |op: SW> => - |op: N> - |op: E>
expand |op: W> => - |op: E>
expand |op: NW> => |op: N> - |op: E>
expand |op: N> => |op: N>
expand |op: NE> => |op: N> + |op: E>
expand |op: E> => |op: E>
expand |op: SE> => - |op: N> + |op: E>



d |*> #=> display-map[30,30]

-- single map update:
line |*> #=> scent |> . take-step |> . d |>

-- set max steps:
max |steps> => |20>

-- walk max steps:
walk |*> #=> sdrop set-to[0] line sp2seq range(|1>, max |steps>)

