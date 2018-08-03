
|context> => |context: active logic>

-- learn the meaning of not:
not |no> => |yes>
not |yes> => |no>
not |don't know> => |don't know>

-- define our if-then machines:
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


-- learn state of activation:
active |rained last night> => |don't know>
active |not rained last night> #=> not active |rained last night>
active |sprinkler was on> => |don't know>
active |not sprinkler was on> #=> not active |sprinkler was on>
active |grass is wet> => |don't know>
active |not grass is wet> #=> not active |grass is wet>


-- activation states we want to unlearn:
the-unlearn |list> => |rained last night> + |sprinkler was on> + |grass is wet>


-- unlearn operators:
unlearn |*> #=> learn(|op: active>, |_self>, |don't know>)
unlearn-everything |*> #=> unlearn the-unlearn |list>


-- our 'active' operators:
make-active |*> #=> learn(|op: active>, remove-prefix["not "] |_self>, not has-prefix["not "] |_self>)
currently-active |*> #=> such-that[active] rel-kets[active] |>
read-sentence |*> #=> make-active words-to-list |_self>


-- define our conclude operators:
conclude |*> #=> drop then similar-input[pattern] such-that[active] rel-kets[active] |>
inverse-conclude |*> #=> pattern similar-input[then] such-that[active] rel-kets[active] |>


-- define short-cuts for our tables:
t |*> #=> table[state, unlearn-everything, read-sentence, currently-active, conclude, inverse-conclude] the-list-of |states>
t2 |*> #=> table[state, unlearn-everything, read-sentence, currently-active, conclude] the-list-of |states>


-- learn the list of states we want in our tables:
the-list-of |states> => |grass is wet> 
the-list-of |states> +=> |sprinkler was on>
the-list-of |states> +=> |rained last night>
the-list-of |states> +=> |sprinkler was on and rained last night>
the-list-of |states> +=> |grass is wet and not rained last night>
the-list-of |states> +=> |grass is wet and not sprinkler was on>
the-list-of |states> +=> |not rained last night>
the-list-of |states> +=> |not sprinkler was on>
the-list-of |states> +=> |not rained last night and not sprinkler was on>
the-list-of |states> +=> |not grass is wet>
