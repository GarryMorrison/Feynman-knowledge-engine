
----------------------------------------
|context> => |context: binary tree>

supported-ops |x> => |op: text> + |op: left> + |op: right>
text |x> => |start node>
left |x> => |0>
right |x> => |1>

supported-ops |0> => |op: text> + |op: left> + |op: right>
text |0> => |first child node>
left |0> => |00>
right |0> => |10>

supported-ops |1> => |op: text> + |op: left> + |op: right>
text |1> => |second child node>
left |1> => |01>
right |1> => |11>

supported-ops |00> => |op: text> + |op: left> + |op: right>
text |00> => |third child node>
left |00> => |000>
right |00> => |100>

supported-ops |10> => |op: text> + |op: left> + |op: right>
text |10> => |fourth child node>
left |10> => |010>
right |10> => |110>

supported-ops |01> => |op: text> + |op: left> + |op: right>
text |01> => |fifth child node>
left |01> => |001>
right |01> => |101>

supported-ops |11> => |op: text> + |op: left> + |op: right>
text |11> => |sixth child node>
left |11> => |011>
right |11> => |111>

supported-ops |*> => |op: child>
child |*> #=> left |_self> + right |_self>
----------------------------------------
