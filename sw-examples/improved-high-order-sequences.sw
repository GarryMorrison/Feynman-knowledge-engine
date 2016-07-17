full |range> => range(|1>,|65536>)


-- count one two three four five six seven
sequence-number |node 0: *> => |sequence-0>

pattern |node 0: 1> => then |node 0: 0>

pattern |node 0: 2> => then |node 0: 1>

pattern |node 0: 3> => then |node 0: 2>

pattern |node 0: 4> => then |node 0: 3>

pattern |node 0: 5> => then |node 0: 4>

pattern |node 0: 6> => then |node 0: 5>



-- Fibonacci one one two three five eight thirteen
sequence-number |node 1: *> => |sequence-1>

pattern |node 1: 1> => then |node 1: 0>

pattern |node 1: 2> => then |node 1: 1>

pattern |node 1: 3> => then |node 1: 2>

pattern |node 1: 4> => then |node 1: 3>

pattern |node 1: 5> => then |node 1: 4>

pattern |node 1: 6> => then |node 1: 5>



-- factorial one two six twenty-four one-hundred-twenty
sequence-number |node 2: *> => |sequence-2>

pattern |node 2: 1> => then |node 2: 0>

pattern |node 2: 2> => then |node 2: 1>

pattern |node 2: 3> => then |node 2: 2>

pattern |node 2: 4> => then |node 2: 3>



step-1 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-2 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-3 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-4 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-5 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-6 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-7 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>

the-table |*> #=> table[ket,step-1,step-2,step-3,step-4,step-5,step-6,step-7] rel-kets[encode] |>


sequence-table |*> #=> table[ket,which-sequence] rel-kets[encode] |>
