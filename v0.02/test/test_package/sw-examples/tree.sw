|context> => |context: binary tree>

-- define the head:
left |x> => |0>
right |x> => |1>

-- define our operators:
child |*> #=> left |_self> + right |_self>
left-op |*> #=> |_self> _ |0>
right-op |*> #=> |_self> _ |1>

-- now build the tree:
|null> => map[left-op, left] child |x>
|null> => map[right-op, right] child |x>

|null> => map[left-op, left] child^2 |x>
|null> => map[right-op, right] child^2 |x>
        
|null> => map[left-op, left] child^3 |x>
|null> => map[right-op, right] child^3 |x>

-- |null> => map[left-op, left] child^4 |x>
-- |null> => map[right-op, right] child^4 |x>

