full |range> => range(|1>,|2048>)
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
encode |O> => pick[10] full |range>
encode |P> => pick[10] full |range>
encode |Q> => pick[10] full |range>
encode |R> => pick[10] full |range>
encode |S> => pick[10] full |range>
encode |T> => pick[10] full |range>
encode |U> => pick[10] full |range>
encode |V> => pick[10] full |range>
encode |W> => pick[10] full |range>
encode |X> => pick[10] full |range>
encode |Y> => pick[10] full |range>
encode |Z> => pick[10] full |range>
encode |end of sequence> => pick[10] full |range>
encode |alpha 0> => pick[10] full |range>
encode |alpha 1> => pick[10] full |range>
encode |alpha 2> => pick[10] full |range>
encode |alpha 3> => pick[10] full |range>
encode |alpha 4> => pick[10] full |range>
encode |alpha 5> => pick[10] full |range>
encode |alpha 6> => pick[10] full |range>
encode |alpha 7> => pick[10] full |range>
encode |alpha 8> => pick[10] full |range>


-- alphabet
-- alpha 0, alpha 1, alpha 2, alpha 3, alpha 4, alpha 5, alpha 6, alpha 7, alpha 8
start-node |alphabet> => random-column[10] encode |alpha 0>
pattern |node 0: 0> => start-node |alphabet>
then |node 0: 0> => random-column[10] encode |alpha 1>

pattern |node 0: 1> => then |node 0: 0>
then |node 0: 1> => random-column[10] encode |alpha 2>

pattern |node 0: 2> => then |node 0: 1>
then |node 0: 2> => random-column[10] encode |alpha 3>

pattern |node 0: 3> => then |node 0: 2>
then |node 0: 3> => random-column[10] encode |alpha 4>

pattern |node 0: 4> => then |node 0: 3>
then |node 0: 4> => random-column[10] encode |alpha 5>

pattern |node 0: 5> => then |node 0: 4>
then |node 0: 5> => random-column[10] encode |alpha 6>

pattern |node 0: 6> => then |node 0: 5>
then |node 0: 6> => random-column[10] encode |alpha 7>

pattern |node 0: 7> => then |node 0: 6>
then |node 0: 7> => random-column[10] encode |alpha 8>

pattern |node 0: 8> => then |node 0: 7>
then |node 0: 8> => append-column[10] encode |end of sequence>


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
-- G, H, I
start-node |alpha 2> => random-column[10] encode |G>
pattern |node 3: 0> => start-node |alpha 2>
then |node 3: 0> => random-column[10] encode |H>

pattern |node 3: 1> => then |node 3: 0>
then |node 3: 1> => random-column[10] encode |I>

pattern |node 3: 2> => then |node 3: 1>
then |node 3: 2> => append-column[10] encode |end of sequence>


-- alpha 3
-- J, K, L
start-node |alpha 3> => random-column[10] encode |J>
pattern |node 4: 0> => start-node |alpha 3>
then |node 4: 0> => random-column[10] encode |K>

pattern |node 4: 1> => then |node 4: 0>
then |node 4: 1> => random-column[10] encode |L>

pattern |node 4: 2> => then |node 4: 1>
then |node 4: 2> => append-column[10] encode |end of sequence>


-- alpha 4
-- M, N, O
start-node |alpha 4> => random-column[10] encode |M>
pattern |node 5: 0> => start-node |alpha 4>
then |node 5: 0> => random-column[10] encode |N>

pattern |node 5: 1> => then |node 5: 0>
then |node 5: 1> => random-column[10] encode |O>

pattern |node 5: 2> => then |node 5: 1>
then |node 5: 2> => append-column[10] encode |end of sequence>


-- alpha 5
-- P, Q, R
start-node |alpha 5> => random-column[10] encode |P>
pattern |node 6: 0> => start-node |alpha 5>
then |node 6: 0> => random-column[10] encode |Q>

pattern |node 6: 1> => then |node 6: 0>
then |node 6: 1> => random-column[10] encode |R>

pattern |node 6: 2> => then |node 6: 1>
then |node 6: 2> => append-column[10] encode |end of sequence>


-- alpha 6
-- S, T, U
start-node |alpha 6> => random-column[10] encode |S>
pattern |node 7: 0> => start-node |alpha 6>
then |node 7: 0> => random-column[10] encode |T>

pattern |node 7: 1> => then |node 7: 0>
then |node 7: 1> => random-column[10] encode |U>

pattern |node 7: 2> => then |node 7: 1>
then |node 7: 2> => append-column[10] encode |end of sequence>


-- alpha 7
-- V, W, X
start-node |alpha 7> => random-column[10] encode |V>
pattern |node 8: 0> => start-node |alpha 7>
then |node 8: 0> => random-column[10] encode |W>

pattern |node 8: 1> => then |node 8: 0>
then |node 8: 1> => random-column[10] encode |X>

pattern |node 8: 2> => then |node 8: 1>
then |node 8: 2> => append-column[10] encode |end of sequence>


-- alpha 8
-- Y, Z
start-node |alpha 8> => random-column[10] encode |Y>
pattern |node 9: 0> => start-node |alpha 8>
then |node 9: 0> => random-column[10] encode |Z>

pattern |node 9: 1> => then |node 9: 0>
then |node 9: 1> => append-column[10] encode |end of sequence>
