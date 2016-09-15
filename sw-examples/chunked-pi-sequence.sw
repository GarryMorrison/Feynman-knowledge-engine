full |range> => range(|1>,|2048>)
encode |3> => pick[10] full |range>
encode |.> => pick[10] full |range>
encode |1> => pick[10] full |range>
encode |4> => pick[10] full |range>
encode |5> => pick[10] full |range>
encode |9> => pick[10] full |range>
encode |2> => pick[10] full |range>
encode |6> => pick[10] full |range>
encode |8> => pick[10] full |range>
encode |7> => pick[10] full |range>
encode |end of sequence> => pick[10] full |range>
encode |alpha 0> => pick[10] full |range>
encode |alpha 1> => pick[10] full |range>
encode |alpha 2> => pick[10] full |range>
encode |alpha 3> => pick[10] full |range>
encode |alpha 4> => pick[10] full |range>
encode |alpha 5> => pick[10] full |range>


-- pi
-- alpha 0, alpha 1, alpha 2, alpha 3, alpha 4, alpha 5
start-node |pi> => random-column[10] encode |alpha 0>
pattern |node 0: 0> => start-node |pi>
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
then |node 0: 5> => append-column[10] encode |end of sequence>


-- alpha 0
-- 3, ., 1
start-node |alpha 0> => random-column[10] encode |3>
pattern |node 1: 0> => start-node |alpha 0>
then |node 1: 0> => random-column[10] encode |.>

pattern |node 1: 1> => then |node 1: 0>
then |node 1: 1> => random-column[10] encode |1>

pattern |node 1: 2> => then |node 1: 1>
then |node 1: 2> => append-column[10] encode |end of sequence>


-- alpha 1
-- 4, 1, 5
start-node |alpha 1> => random-column[10] encode |4>
pattern |node 2: 0> => start-node |alpha 1>
then |node 2: 0> => random-column[10] encode |1>

pattern |node 2: 1> => then |node 2: 0>
then |node 2: 1> => random-column[10] encode |5>

pattern |node 2: 2> => then |node 2: 1>
then |node 2: 2> => append-column[10] encode |end of sequence>


-- alpha 2
-- 9, 2, 6
start-node |alpha 2> => random-column[10] encode |9>
pattern |node 3: 0> => start-node |alpha 2>
then |node 3: 0> => random-column[10] encode |2>

pattern |node 3: 1> => then |node 3: 0>
then |node 3: 1> => random-column[10] encode |6>

pattern |node 3: 2> => then |node 3: 1>
then |node 3: 2> => append-column[10] encode |end of sequence>


-- alpha 3
-- 5, 3, 5
start-node |alpha 3> => random-column[10] encode |5>
pattern |node 4: 0> => start-node |alpha 3>
then |node 4: 0> => random-column[10] encode |3>

pattern |node 4: 1> => then |node 4: 0>
then |node 4: 1> => random-column[10] encode |5>

pattern |node 4: 2> => then |node 4: 1>
then |node 4: 2> => append-column[10] encode |end of sequence>


-- alpha 4
-- 8, 9, 7
start-node |alpha 4> => random-column[10] encode |8>
pattern |node 5: 0> => start-node |alpha 4>
then |node 5: 0> => random-column[10] encode |9>

pattern |node 5: 1> => then |node 5: 0>
then |node 5: 1> => random-column[10] encode |7>

pattern |node 5: 2> => then |node 5: 1>
then |node 5: 2> => append-column[10] encode |end of sequence>


-- alpha 5
-- 9
start-node |alpha 5> => random-column[10] encode |9>
pattern |node 6: 0> => start-node |alpha 5>
then |node 6: 0> => append-column[10] encode |end of sequence>
