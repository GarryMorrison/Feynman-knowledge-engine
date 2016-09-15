full |range> => range(|1>,|2048>)
encode |A> => pick[10] full |range>
encode |B> => pick[10] full |range>
encode |C> => pick[10] full |range>
encode |D> => pick[10] full |range>
encode |E> => pick[10] full |range>
encode |F> => pick[10] full |range>
encode |G> => pick[10] full |range>
encode |H> => pick[10] full |range>
encode |end of sequence> => pick[10] full |range>
encode |alpha 0> => pick[10] full |range>
encode |alpha 1> => pick[10] full |range>
encode |alpha 2> => pick[10] full |range>


-- alphabet
-- alpha 0, alpha 1, alpha 2
start-node |alphabet> => random-column[10] encode |alpha 0>
pattern |node 0: 0> => start-node |alphabet>
then |node 0: 0> => random-column[10] encode |alpha 1>

pattern |node 0: 1> => then |node 0: 0>
then |node 0: 1> => random-column[10] encode |alpha 2>

pattern |node 0: 2> => then |node 0: 1>
then |node 0: 2> => append-column[10] encode |end of sequence>


-- alpha 0
-- A, B, C
start-node |alpha 0> => random-column[10] encode |A>
pattern |node 1: 0> => start-node |alpha 0>
then |node 1: 0> => random-column[10] encode |B>

pattern |node 1: 1> => then |node 1: 0>
then |node 1: 1> => random-column[10] encode |C>

pattern |node 1: 2> => then |node 1: 1>
then |node 1: 2> => append-column[10] encode |end of sequence>


-- alpha 1
-- D, E, F
start-node |alpha 1> => random-column[10] encode |D>
pattern |node 2: 0> => start-node |alpha 1>
then |node 2: 0> => random-column[10] encode |E>

pattern |node 2: 1> => then |node 2: 0>
then |node 2: 1> => random-column[10] encode |F>

pattern |node 2: 2> => then |node 2: 1>
then |node 2: 2> => append-column[10] encode |end of sequence>


-- alpha 2
-- G, H
start-node |alpha 2> => random-column[10] encode |G>
pattern |node 3: 0> => start-node |alpha 2>
then |node 3: 0> => random-column[10] encode |H>

pattern |node 3: 1> => then |node 3: 0>
then |node 3: 1> => append-column[10] encode |end of sequence>
