pattern |node: 1: 1> => |word: fred>
pattern |node: 1: 2> => |word: freddie>
pattern |node: 1: 3> => |word: smith>
pattern |node: 1: 4> => |word: smithie>
then |node: 1: *> => |person: Fred Smith>

pattern |node: 2: 1> => |word: mazza>
then |node: 2: *> => |person: Mary>

pattern |node: 3: 1> => |word: hey>
then |node: 3: *> => |greeting: Hey!>

pattern |node: 4: 1> => |word: what's>
then |node: 4: *> => |question: what is>

pattern |node: 5: 1> => |word: up>
then |node: 5: *> => |direction: up>

pattern |node: 6: 1> => read |text: having a baby>
then |node: 6: *> => |phrase: having a baby>

pattern |node: 7: 1> => read |text: in the family way>
then |node: 7: *> => |phrase: in the family way>

pattern |node: 8: 1> => read |text: up the duff>
then |node: 8: *> => |phrase: up the duff>

pattern |node: 9: 1> => read |text: with child>
then |node: 9: *> => |phrase: with child>

pattern |node: 10: 1> => |phrase: having a baby>
pattern |node: 10: 2> => |phrase: in the family way>
pattern |node: 10: 3> => |phrase: up the duff>
pattern |node: 10: 4> => |phrase: with child>
then |node: 10: *> => |concept: pregnancy>
