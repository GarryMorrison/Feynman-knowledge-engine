
----------------------------------------
|context> => |context: in the processor>

supported-ops |no> => |op: not>
not |no> => |yes>

supported-ops |yes> => |op: not>
not |yes> => |no>

supported-ops |don't know> => |op: not>
not |don't know> => |don't know>

supported-ops |node 1: 1> => |op: pattern>
pattern |node 1: 1> => |grass is wet> + |not rained last night>

supported-ops |node 1: *> => |op: then>
then |node 1: *> => 2.0|sprinkler was on> + -1.0|rained last night> + -1.0|not grass is wet>

supported-ops |node 2: 1> => |op: pattern>
pattern |node 2: 1> => |grass is wet> + |not sprinkler was on>

supported-ops |node 2: *> => |op: then>
then |node 2: *> => 2.0|rained last night> + -1.0|sprinkler was on> + -1.0|not grass is wet>

supported-ops |node 3: 1> => |op: pattern>
pattern |node 3: 1> => |sprinkler was on>

supported-ops |node 3: 2> => |op: pattern>
pattern |node 3: 2> => |rained last night>

supported-ops |node 3: *> => |op: then>
then |node 3: *> => |grass is wet>

supported-ops |node 5: 1> => |op: pattern>
pattern |node 5: 1> => |not rained last night> + |not sprinkler was on>

supported-ops |node 5: *> => |op: then>
then |node 5: *> => 2.0|not grass is wet> + -1.0|rained last night> + -1.0|sprinkler was on>

supported-ops |rained last night> => |op: active>
active |rained last night> => |no>

supported-ops |not rained last night> => |op: active>
active |not rained last night> #=> not active |rained last night>

supported-ops |sprinkler was on> => |op: active>
active |sprinkler was on> => |no>

supported-ops |not sprinkler was on> => |op: active>
active |not sprinkler was on> #=> not active |sprinkler was on>

supported-ops |grass is wet> => |op: active>
active |grass is wet> => |don't know>

supported-ops |not grass is wet> => |op: active>
active |not grass is wet> #=> not active |grass is wet>

supported-ops |list> => |op: the-unlearn>
the-unlearn |list> => |rained last night> + |sprinkler was on> + |grass is wet>

supported-ops |*> => |op: unlearn> + |op: unlearn-everything> + |op: make-active> + |op: read-sentence> + |op: conclude> + |op: t> + |op: report> + |op: report-active> + |op: currently-active>
unlearn |*> #=> learn(|op: active>, |_self>, |don't know>)
unlearn-everything |*> #=> unlearn the-unlearn |list>
make-active |*> #=> learn(|op: active>, remove-prefix["not "] |_self>, not has-prefix["not "] |_self>)
read-sentence |*> #=> make-active words-to-list |_self>
conclude |*> #=> drop then similar-input[pattern] such-that[active] rel-kets[active] |>
t |*> #=> table[state, unlearn-everything, read-sentence, currently-active, conclude] the-list-of |states>
report |*> #=> such-that[active] rel-kets[active] |>
report-active |*> #=> such-that[active] rel-kets[active] |>
currently-active |*> #=> such-that[active] rel-kets[active] |>

supported-ops |states> => |op: the-list-of>
the-list-of |states> => |grass is wet> + |sprinkler was on> + |rained last night> + |sprinkler was on and rained last night> + |grass is wet and not rained last night> + |grass is wet and not sprinkler was on> + |not rained last night> + |not sprinkler was on> + |not rained last night and not sprinkler was on>

supported-ops |node 4: 1> => |op: pattern>
pattern |node 4: 1> => |fish soup>

supported-ops |node 4: *> => |op: then>
then |node 4: *> => |sprinkler was on> + |rained last night>
----------------------------------------
