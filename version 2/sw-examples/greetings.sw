
----------------------------------------
|context> => |context: greetings>

supported-ops |*> => |op: hello> + |op: hey> + |op: wat-up> + |op: greetings> + |op: howdy> + |op: good-morning> + |op: gday> + |op: greet> + |op: the-friends-of>
hello |*> #=> |Hello,> __ |_self> _ |!>
hey |*> #=> |Hey Ho!> __ |_self> _ |.>
wat-up |*> #=> |Wat up my homie!> __ |_self> __ |right?>
greetings |*> #=> |Greetings fine Sir. I belive they call you> __ |_self> _ |.>
howdy |*> #=> |Howdy partner!>
good-morning |*> #=> |Good morning> __ |_self> _ |.>
gday |*> #=> |G'day> __ |_self> _ |.>
greet |*> #=> apply(pick-elt list-of |greetings>, |_self>)
the-friends-of |*> #=> list-to-words friends |_self>

supported-ops |greetings> => |op: list-of>
list-of |greetings> => |op: hello> + |op: hey> + |op: wat-up> + |op: greetings> + |op: howdy> + |op: good-morning> + |op: gday>

supported-ops |Sam> => |op: friends>
friends |Sam> => |Charlie> + |George> + |Emma> + |Jack> + |Robert> + |Frank> + |Julie>

supported-ops |Emma> => |op: friends>
friends |Emma> => |Liz> + |Bob>
----------------------------------------
