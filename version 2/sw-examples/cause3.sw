pattern |node: 1: 1> => |fred>
pattern |node: 1: 2> => |freddie>
pattern |node: 1: 3> => |smith>
pattern |node: 1: 4> => |smithie>
pattern |node: 1: 5> => |fred> . |smith>
then |node: 1: *> => |person: Fred Smith>

pattern |node: 2: 1> => |mazza>
then |node: 2: *> => |person: Mary>

pattern |node: 3: 1> => |hey>
then |node: 3: *> => |greeting: Hey!>

pattern |node: 4: 1> => |what's>
pattern |node: 4: 2> => |what> . |is>
then |node: 4: *> => |question: what is>

pattern |node: 5: 1> => |up>
then |node: 5: *> => |direction: up>

pattern |node: 6: 1> => |having> . |a> . |baby>
then |node: 6: *> => |phrase: having a baby>

pattern |node: 7: 1> => |in> . |the> . |family> . |way>
then |node: 7: *> => |phrase: in the family way>

pattern |node: 8: 1> => |up> . |the> . |duff>
then |node: 8: *> => |phrase: up the duff>

pattern |node: 9: 1> => |with> . |child>
then |node: 9: *> => |phrase: with child>

pattern |node: 10: 1> => |phrase: having a baby>
pattern |node: 10: 2> => |phrase: in the family way>
pattern |node: 10: 3> => |phrase: up the duff>
pattern |node: 10: 4> => |phrase: with child>
then |node: 10: *> => |concept: pregnancy>

read |*> #=> ssplit[" "] replace[",?", ""] to-lower |_self>
