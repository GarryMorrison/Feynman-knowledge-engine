
----------------------------------------
|context> => |context: active logic>

not |no> => |yes>
not |yes> => |no>
not |don't know> => |don't know>

pattern |node 1: 1> => |grass is wet> + |not rained last night>
then |node 1: 1> => 2.0|sprinkler was on> + -1.0|rained last night> + -1.0|not grass is wet>

pattern |node 2: 1> => |grass is wet> + |not sprinkler was on>
then |node 2: 1> => 2.0|rained last night> + -1.0|sprinkler was on> + -1.0|not grass is wet>

pattern |node 3: 1> => |sprinkler was on>
then |node 3: 1> => |grass is wet> + -1.0|not sprinkler was on>

pattern |node 3: 2> => |rained last night>
then |node 3: 2> => |grass is wet> + -1.0|not rained last night>

pattern |node 4: 1> => |not rained last night> + |not sprinkler was on>
then |node 4: 1> => 2.0|not grass is wet> + -1.0|rained last night> + -1.0|sprinkler was on>


active |rained last night> => |don't know>
active |not rained last night> #=> not active |rained last night>
active |sprinkler was on> => |don't know>
active |not sprinkler was on> #=> not active |sprinkler was on>
active |grass is wet> => |no>
active |not grass is wet> #=> not active |grass is wet>

the-unlearn |list> => |rained last night> + |sprinkler was on> + |grass is wet>

unlearn |*> #=> learn(|op: active>, |_self>, |don't know>)
unlearn-everything |*> #=> unlearn the-unlearn |list>
make-active |*> #=> learn(|op: active>, remove-prefix["not "] |_self>, not has-prefix["not "] |_self>)
read-sentence |*> #=> make-active words-to-list |_self>
conclude |*> #=> drop then similar-input[pattern] such-that[active] rel-kets[active] |>
currently-active |*> #=> such-that[active] rel-kets[active] |>
t |*> #=> table[state, unlearn-everything, read-sentence, currently-active, conclude, inverse-conclude] the-list-of |states>
inverse-conclude |*> #=> pattern similar-input[then] such-that[active] rel-kets[active] |>

the-list-of |states> => |grass is wet> + |sprinkler was on> + |rained last night> + |sprinkler was on and rained last night> + |grass is wet and not rained last night> + |grass is wet and not sprinkler was on> + |not rained last night> + |not sprinkler was on> + |not rained last night and not sprinkler was on> + |not grass is wet>
----------------------------------------
