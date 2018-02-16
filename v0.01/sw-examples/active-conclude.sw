
----------------------------------------
|context> => |context: active conclude 2>

supported-ops |no> => |op: not>
not |no> => |yes>

supported-ops |yes> => |op: not>
not |yes> => |no>

supported-ops |don't know> => |op: not>
not |don't know> => |don't know>

supported-ops |node 1: 1> => |op: pattern>
pattern |node 1: 1> => |grass is wet> + |not rained last night>

supported-ops |node 1: *> => |op: then>
then |node 1: *> => |sprinkler was on>

supported-ops |node 2: 1> => |op: pattern>
pattern |node 2: 1> => |grass is wet> + |not sprinkler was on>

supported-ops |node 2: *> => |op: then>
then |node 2: *> => |rained last night>

supported-ops |node 3: 1> => |op: pattern>
pattern |node 3: 1> => |sprinkler was on>

supported-ops |node 3: 2> => |op: pattern>
pattern |node 3: 2> => |rained last night>

supported-ops |node 3: *> => |op: then>
then |node 3: *> => |grass is wet>

supported-ops |rained last night> => |op: active>
active |rained last night> => |don't know>

supported-ops |not rained last night> => |op: active>
active |not rained last night> => |don't know>

supported-ops |sprinkler was on> => |op: active>
active |sprinkler was on> => |don't know>

supported-ops |not sprinkler was on> => |op: active>
active |not sprinkler was on> => |don't know>

supported-ops |grass is wet> => |op: active>
active |grass is wet> => |don't know>

supported-ops |*> => |op: conclude> + |op: unlearn-grass-is-wet> + |op: unlearn-rained-last-night> + |op: unlearn-sprinkler-was-on> + |op: unlearn-not-rained-last-night> + |op: unlearn-not-sprinkler-was-on> + |op: make-active> + |op: unlearn-everything> + |op: read-sentence> + |op: unlearn>
conclude |*> #=> then drop-below[0.8] rescale similar-input[pattern] such-that[active] rel-kets[active] |>
unlearn-grass-is-wet |*> #=> learn(|op: active>, |grass is wet>, |don't know>)
unlearn-rained-last-night |*> #=> learn(|op: active>, |rained last night>, |don't know>)
unlearn-sprinkler-was-on |*> #=> learn(|op: active>, |sprinkler was on>, |don't know>)
unlearn-not-rained-last-night |*> #=> learn(|op: active>, |not rained last night>, |don't know>)
unlearn-not-sprinkler-was-on |*> #=> learn(|op: active>, |not sprinkler was on>, |don't know>)
make-active |*> #=> learn(|op: active>, |_self>, |yes>)
unlearn-everything |*> #=> unlearn rel-kets[active]|>
read-sentence |*> #=> make-active words-to-list |_self>
unlearn |*> #=> learn(|op: active>, |_self>, |don't know>)

supported-ops |Fred> => |op: age>
age |Fred> => |33>
----------------------------------------
