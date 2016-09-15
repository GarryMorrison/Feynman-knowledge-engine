full |range> => range(|1>,|2048>)
encode |A> => pick[10] full |range>
encode |B> => pick[10] full |range>
encode |C> => pick[10] full |range>
encode |D> => pick[10] full |range>
encode |E> => pick[10] full |range>
encode |F> => pick[10] full |range>
encode |end of sequence> => pick[10] full |range>


-- alphabet
-- A B C D E F
start-node |alphabet> => append-column[10] encode |A>
pattern |node 0: 0> => random-column[10] encode |A>
then |node 0: 0> => random-column[10] encode |B>

pattern |node 0: 1> => then |node 0: 0>
then |node 0: 1> => random-column[10] encode |C>

pattern |node 0: 2> => then |node 0: 1>
then |node 0: 2> => random-column[10] encode |D>

pattern |node 0: 3> => then |node 0: 2>
then |node 0: 3> => random-column[10] encode |E>

pattern |node 0: 4> => then |node 0: 3>
then |node 0: 4> => random-column[10] encode |F>

pattern |node 0: 5> => then |node 0: 4>
then |node 0: 5> => append-column[10] encode |end of sequence>

