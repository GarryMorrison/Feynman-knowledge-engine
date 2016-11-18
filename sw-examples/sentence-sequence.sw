full |range> => range(|1>,|2048>)
encode |end of sequence> => pick[10] full |range>

-- encode words:
encode |old> => pick[10] full |range>
encode |other> => pick[10] full |range>
encode |on> => pick[10] full |range>
encode |the> => pick[10] full |range>
encode |hill> => pick[10] full |range>
encode |also> => pick[10] full |range>
encode |the> => pick[10] full |range>
encode |man> => pick[10] full |range>
encode |used> => pick[10] full |range>
encode |a> => pick[10] full |range>
encode |telescope> => pick[10] full |range>
encode |woman> => pick[10] full |range>
encode |lady> => pick[10] full |range>


-- encode classes:
encode |A> => pick[10] full |range>
encode |B> => pick[10] full |range>
encode |C> => pick[10] full |range>
encode |X> => pick[10] full |range>
encode |Y> => pick[10] full |range>


-- empty sequence
pattern |node 1: 1> => append-column[10] encode |end of sequence>

-- old
pattern |node 2: 1> => random-column[10] encode |old>
then |node 2: 1> => append-column[10] encode |end of sequence>

-- other
pattern |node 3: 1> => random-column[10] encode |other>
then |node 3: 1> => append-column[10] encode |end of sequence>

-- on, the, hill
pattern |node 4: 1> => random-column[10] encode |on>
then |node 4: 1> => random-column[10] encode |the>

pattern |node 4: 2> => then |node 4: 1>
then |node 4: 2> => random-column[10] encode |hill>

pattern |node 4: 3> => then |node 4: 2>
then |node 4: 3> => append-column[10] encode |end of sequence>

-- also
pattern |node 5: 1> => random-column[10] encode |also>
then |node 5: 1> => append-column[10] encode |end of sequence>


-- the
pattern |node 6: 1> => random-column[10] encode |the>
then |node 6: 1> => append-column[10] encode |end of sequence>

-- man
pattern |node 7: 1> => random-column[10] encode |man>
then |node 7: 1> => append-column[10] encode |end of sequence>

-- used, a, telescope
pattern |node 8: 1> => random-column[10] encode |used>
then |node 8: 1> => random-column[10] encode |a>

pattern |node 8: 2> => then |node 8: 1>
then |node 8: 2> => random-column[10] encode |telescope>

pattern |node 8: 3> => then |node 8: 2>
then |node 8: 3> => append-column[10] encode |end of sequence>

-- woman
pattern |node 9: 1> => random-column[10] encode |woman>
then |node 9: 1> => append-column[10] encode |end of sequence>

-- lady
pattern |node 10: 1> => random-column[10] encode |lady>
then |node 10: 1> => append-column[10] encode |end of sequence>



-- X: {{}, old, other}
start-node |X: 1> => pattern |node 1: 1>
start-node |X: 2> => pattern |node 2: 1>
start-node |X: 3> => pattern |node 3: 1>

-- Y: {{}, on the hill, also}
start-node |Y: 1> => pattern |node 1: 1>
start-node |Y: 2> => pattern |node 4: 1>
start-node |Y: 3> => pattern |node 5: 1>

-- A: {the}
start-node |A: 1> => pattern |node 6: 1>

-- B: {man,woman,lady}
start-node |B: 1> => pattern |node 7: 1>
start-node |B: 2> => pattern |node 9: 1>
start-node |B: 3> => pattern |node 10: 1>

-- C: {used a telescope}
start-node |C: 1> => pattern |node 8: 1>


-- A, X, B, Y, C
pattern |node 20: 1> => random-column[10] encode |A>
then |node 20: 1> => random-column[10] encode |X>

pattern |node 20: 2> => then |node 20: 1>
then |node 20: 2> => random-column[10] encode |B>

pattern |node 20: 3> => then |node 20: 2>
then |node 20: 3> => random-column[10] encode |Y>

pattern |node 20: 4> => then |node 20: 3>
then |node 20: 4> => random-column[10] encode |C>

pattern |node 20: 5> => then |node 20: 4>
then |node 20: 5> => append-column[10] encode |end of sequence>


-- operators:
append-colon |*> #=> merge-labels(|_self> + |: >)
random-class-sequence |*> #=> follow-sequence start-node pick-elt starts-with append-colon |_self>
random-sequence |*> #=> follow-sequence start-node pick-elt rel-kets[start-node] |>
recall-sentence |*> #=> follow-sequence[random-class-sequence] pattern |_self>

-- usage:
-- sa: recall-sentence |node 20: 1>

