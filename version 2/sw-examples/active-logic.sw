not |no> => |yes>
not |yes> => |no>
not |don't know> => |don't know>


pattern |node 1: 1> => |grass is wet> + |not rained last night>
then |node 1: *> => |sprinkler was on>

pattern |node 2: 1> => |grass is wet> + |not sprinkler was on>
then |node 2: *> => |rained last night>

pattern |node 3: 1> => |sprinkler was on>
pattern |node 3: 2> => |rained last night>
then |node 3: *> => |grass is wet>


active |rained last night> => |don't know>
active |not rained last night> #=> not active |rained last night>

active |sprinkler was on> => |don't know>
active |not sprinkler was on> #=> not active |sprinkler was on>

active |grass is wet> => |don't know>
active |not grass is wet> #=> not active |grass is wet>


the-unlearn |list> => |rained last night> + |sprinkler was on> + |grass is wet>
unlearn |*> #=> learn(|op: active>, |_self>, |don't know>)
unlearn-everything |*> #=> unlearn the-unlearn |list>

make-active |*> #=> learn(|op: active>, remove-prefix["not "] |_self>, not has-prefix["not "] |_self>)
read-sentence |*> #=> make-active words-to-list |_self>

conclude |*> #=> then drop-below[0.8] rescale similar-input[pattern] such-that[active] rel-kets[active] |>


