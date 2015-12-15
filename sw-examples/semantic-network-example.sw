
----------------------------------------
|context> => |context: semantic network example>

supported-ops |Mammal> => |op: has> + |op: is-an>
has |Mammal> => |Vertebra>
is-an |Mammal> => |Animal>

supported-ops |Cat> => |op: is-a> + |op: has>
is-a |Cat> => |Mammal>
has |Cat> => |Fur>

supported-ops |Bear> => |op: is-a> + |op: has>
is-a |Bear> => |Mammal>
has |Bear> => |Fur>

supported-ops |Whale> => |op: is-a> + |op: lives-in>
is-a |Whale> => |Mammal>
lives-in |Whale> => |Water>

supported-ops |Fish> => |op: is-an> + |op: lives-in>
is-an |Fish> => |Animal>
lives-in |Fish> => |Water>
----------------------------------------
