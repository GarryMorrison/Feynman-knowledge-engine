full |range> => range(|1>,|65536>)
encode |count> => pick[10] full |range>
encode |one> => pick[10] full |range>
encode |two> => pick[10] full |range>
encode |three> => pick[10] full |range>
encode |four> => pick[10] full |range>
encode |five> => pick[10] full |range>
encode |six> => pick[10] full |range>
encode |seven> => pick[10] full |range>
encode |Fibonacci> => pick[10] full |range>
encode |eight> => pick[10] full |range>
encode |thirteen> => pick[10] full |range>
encode |factorial> => pick[10] full |range>
encode |twenty-four> => pick[10] full |range>
encode |one-hundred-twenty> => pick[10] full |range>


-- count one two three four five six seven
sequence-number |node 0: *> => |sequence-0>
pattern |node 0: 0> => random-column[10] encode |count>
then |node 0: 0> => random-column[10] encode |one>

pattern |node 0: 1> => then |node 0: 0>
then |node 0: 1> => random-column[10] encode |two>

pattern |node 0: 2> => then |node 0: 1>
then |node 0: 2> => random-column[10] encode |three>

pattern |node 0: 3> => then |node 0: 2>
then |node 0: 3> => random-column[10] encode |four>

pattern |node 0: 4> => then |node 0: 3>
then |node 0: 4> => random-column[10] encode |five>

pattern |node 0: 5> => then |node 0: 4>
then |node 0: 5> => random-column[10] encode |six>

pattern |node 0: 6> => then |node 0: 5>
then |node 0: 6> => random-column[10] encode |seven>



-- Fibonacci one one two three five eight thirteen
sequence-number |node 1: *> => |sequence-1>
pattern |node 1: 0> => random-column[10] encode |Fibonacci>
then |node 1: 0> => random-column[10] encode |one>

pattern |node 1: 1> => then |node 1: 0>
then |node 1: 1> => random-column[10] encode |one>

pattern |node 1: 2> => then |node 1: 1>
then |node 1: 2> => random-column[10] encode |two>

pattern |node 1: 3> => then |node 1: 2>
then |node 1: 3> => random-column[10] encode |three>

pattern |node 1: 4> => then |node 1: 3>
then |node 1: 4> => random-column[10] encode |five>

pattern |node 1: 5> => then |node 1: 4>
then |node 1: 5> => random-column[10] encode |eight>

pattern |node 1: 6> => then |node 1: 5>
then |node 1: 6> => random-column[10] encode |thirteen>



-- factorial one two six twenty-four one-hundred-twenty
sequence-number |node 2: *> => |sequence-2>
pattern |node 2: 0> => random-column[10] encode |factorial>
then |node 2: 0> => random-column[10] encode |one>

pattern |node 2: 1> => then |node 2: 0>
then |node 2: 1> => random-column[10] encode |two>

pattern |node 2: 2> => then |node 2: 1>
then |node 2: 2> => random-column[10] encode |six>

pattern |node 2: 3> => then |node 2: 2>
then |node 2: 3> => random-column[10] encode |twenty-four>

pattern |node 2: 4> => then |node 2: 3>
then |node 2: 4> => random-column[10] encode |one-hundred-twenty>


input-encode |*> #=> append-column[10] encode |_self>

step-1 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-2 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-3 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-4 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-5 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-6 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-7 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>

the-table |*> #=> table[ket,step-1,step-2,step-3,step-4,step-5,step-6,step-7] rel-kets[encode] |>

which-sequence |*> #=> sequence-number drop-below[0.5] 10 similar-input[pattern] input-encode |_self>

sequence-table |*> #=> table[ket,which-sequence] rel-kets[encode] |>
