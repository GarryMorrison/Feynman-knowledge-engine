full |range> => range(|1>,|2048>)
encode |end of sequence> => pick[10] full |range>

-- encode words:
encode |the> => pick[10] full |range>
encode |eldest> => pick[10] full |range>
encode |youngest> => pick[10] full |range>
encode |child> => pick[10] full |range>
encode |sibling> => pick[10] full |range>
encode |old> => pick[10] full |range>
encode |other> => pick[10] full |range>
encode |man> => pick[10] full |range>
encode |woman> => pick[10] full |range>
encode |lady> => pick[10] full |range>
encode |young> => pick[10] full |range>
encode |on> => pick[10] full |range>
encode |hill> => pick[10] full |range>
encode |also> => pick[10] full |range>
encode |used> => pick[10] full |range>
encode |a> => pick[10] full |range>
encode |telescope> => pick[10] full |range>


-- encode classes:
encode |A> => pick[10] full |range>
encode |B> => pick[10] full |range>
encode |C> => pick[10] full |range>
encode |D> => pick[10] full |range>
encode |E> => pick[10] full |range>
encode |F> => pick[10] full |range>
encode |G> => pick[10] full |range>
encode |H> => pick[10] full |range>
encode |I> => pick[10] full |range>
encode |J> => pick[10] full |range>
encode |K> => pick[10] full |range>
encode |L> => pick[10] full |range>
encode |M> => pick[10] full |range>
encode |N> => pick[10] full |range>


-- empty sequence
pattern |node 1: 1> => append-column[10] encode |end of sequence>

-- the
pattern |node 2: 1> => random-column[10] encode |the>
then |node 2: 1> => append-column[10] encode |end of sequence>

-- youngest
pattern |node 3: 1> => random-column[10] encode |youngest>
then |node 3: 1> => append-column[10] encode |end of sequence>

-- eldest
pattern |node 4: 1> => random-column[10] encode |eldest>
then |node 4: 1> => append-column[10] encode |end of sequence>

-- child
pattern |node 5: 1> => random-column[10] encode |child>
then |node 5: 1> => append-column[10] encode |end of sequence>

-- sibling
pattern |node 6: 1> => random-column[10] encode |sibling>
then |node 6: 1> => append-column[10] encode |end of sequence>

-- old
pattern |node 7: 1> => random-column[10] encode |old>
then |node 7: 1> => append-column[10] encode |end of sequence>

-- other
pattern |node 8: 1> => random-column[10] encode |other>
then |node 8: 1> => append-column[10] encode |end of sequence>

-- man
pattern |node 9: 1> => random-column[10] encode |man>
then |node 9: 1> => append-column[10] encode |end of sequence>

-- woman
pattern |node 10: 1> => random-column[10] encode |woman>
then |node 10: 1> => append-column[10] encode |end of sequence>

-- lady
pattern |node 11: 1> => random-column[10] encode |lady>
then |node 11: 1> => append-column[10] encode |end of sequence>

-- young
pattern |node 12: 1> => random-column[10] encode |young>
then |node 12: 1> => append-column[10] encode |end of sequence>

-- on, the, hill
pattern |node 13: 1> => random-column[10] encode |on>
then |node 13: 1> => random-column[10] encode |the>

pattern |node 13: 2> => then |node 13: 1>
then |node 13: 2> => random-column[10] encode |hill>

pattern |node 13: 3> => then |node 13: 2>
then |node 13: 3> => append-column[10] encode |end of sequence>

-- also
pattern |node 14: 1> => random-column[10] encode |also>
then |node 14: 1> => append-column[10] encode |end of sequence>

-- used, a, telescope
pattern |node 15: 1> => random-column[10] encode |used>
then |node 15: 1> => random-column[10] encode |a>

pattern |node 15: 2> => then |node 15: 1>
then |node 15: 2> => random-column[10] encode |telescope>

pattern |node 15: 3> => then |node 15: 2>
then |node 15: 3> => append-column[10] encode |end of sequence>



-- A: {the}
start-node |A: 1> => pattern |node 2: 1>

-- B: {{}, old, other}
start-node |B: 1> => pattern |node 1: 1>
start-node |B: 2> => pattern |node 7: 1>
start-node |B: 3> => pattern |node 8: 1>

-- C: {man, woman, lady}
start-node |C: 1> => pattern |node 9: 1>
start-node |C: 2> => pattern |node 10: 1>
start-node |C: 3> => pattern |node 11: 1>

-- D: {{}, young}
start-node |D: 1> => pattern |node 1: 1> 
start-node |D: 2> => pattern |node 12: 1> 

-- E: {child}
start-node |E: 1> => pattern |node 5: 1> 
 
-- F: {youngest, eldest}
start-node |F: 1> => pattern |node 3: 1> 
start-node |F: 2> => pattern |node 4: 1> 

-- G: {child, sibling}
start-node |G: 1> => pattern |node 5: 1> 
start-node |G: 2> => pattern |node 6: 1> 

-- H: {{}, on the hill, also}
start-node |H: 1> => pattern |node 1: 1>
start-node |H: 2> => pattern |node 13: 1>
start-node |H: 3> => pattern |node 14: 1>

-- I: {used a telescope}
start-node |I: 1> => pattern |node 15: 1>



-- J: B, C
pattern |node 100: 1> => random-column[10] encode |B>
then |node 100: 1> => random-column[10] encode |C>

pattern |node 100: 2> => then |node 100: 1>
then |node 100: 2> => append-column[10] encode |end of sequence>

-- K: D, E
pattern |node 101: 1> => random-column[10] encode |D>
then |node 101: 1> => random-column[10] encode |E>

pattern |node 101: 2> => then |node 101: 1>
then |node 101: 2> => append-column[10] encode |end of sequence>

-- L: F, G
pattern |node 102: 1> => random-column[10] encode |F>
then |node 102: 1> => random-column[10] encode |G>

pattern |node 102: 2> => then |node 102: 1>
then |node 102: 2> => append-column[10] encode |end of sequence>


-- M: {J, K, L}
start-node |M: 1> => pattern |node 100: 1>
start-node |M: 2> => pattern |node 101: 1>
start-node |M: 3> => pattern |node 102: 1>


-- N: A, M, H, I
pattern |node 200: 1> => random-column[10] encode |A>
then |node 200: 1> => random-column[10] encode |M>

pattern |node 200: 2> => then |node 200: 1>
then |node 200: 2> => random-column[10] encode |H>

pattern |node 200: 3> => then |node 200: 2>
then |node 200: 3> => random-column[10] encode |I>

pattern |node 200: 4> => then |node 200: 3>
then |node 200: 4> => append-column[10] encode |end of sequence>


-- operators:
append-colon |*> #=> merge-labels(|_self> + |: >)
random-class-sequence |*> #=> follow-sequence start-node pick-elt starts-with append-colon |_self>
random-sequence |*> #=> follow-sequence start-node pick-elt rel-kets[start-node] |>
-- recall-sentence |*> #=> follow-sequence[random-class-sequence] pattern |_self>
print-sentence |*> #=> recall-sentence pattern |_self>

-- old usage:
-- sa: recall-sentence |node 20: 1>

-- usage:
-- sa: print-sentence |node 200: 1>

