
----------------------------------------
supported-ops |context> => |op: > + |op: previous>
 |context> => |context: prolog example>
previous |context> => |context: global context>

supported-ops |sally> => |op: mother> + |op: father>
mother |sally> => |trude>
father |sally> => |tom>

supported-ops |erica> => |op: mother> + |op: father>
mother |erica> => |trude>
father |erica> => |tom>

supported-ops |trude> => |op: mother> + |op: father> + |op: inverse-mother>
mother |trude> => |sara>
father |trude> => |sam>
inverse-mother |trude> => |sally> + |erica>

supported-ops |tom> => |op: mother> + |op: father> + |op: inverse-father>
mother |tom> => |ruth>
father |tom> => |mike>
inverse-father |tom> => |sally> + |erica>

supported-ops |ruth> => |op: mother> + |op: inverse-mother>
mother |ruth> => |gina>
inverse-mother |ruth> => |tom>

supported-ops |mike> => |op: mother> + |op: father> + |op: inverse-father>
mother |mike> => |mary>
father |mike> => |mark>
inverse-father |mike> => |tom>

supported-ops |sara> => |op: inverse-mother>
inverse-mother |sara> => |trude>

supported-ops |gina> => |op: inverse-mother>
inverse-mother |gina> => |ruth>

supported-ops |mary> => |op: inverse-mother>
inverse-mother |mary> => |mike>

supported-ops |sam> => |op: inverse-father>
inverse-father |sam> => |trude>

supported-ops |mark> => |op: inverse-father>
inverse-father |mark> => |mike>

supported-ops |*> => |op: child> + |op: parent> + |op: sibling> + |op: grand-parent> + |op: grand-mother> + |op: grand-father> + |op: grand-child> + |op: great-grand-child> + |op: great-grand-parent>

child |*> #=> inverse-mother |_self> + inverse-father |_self>

parent |*> #=> mother |_self> + father |_self>

sibling |*> #=> drop (clean child parent |_self> - |_self>)

grand-parent |*> #=> parent parent |_self>

grand-mother |*> #=> mother parent |_self>

grand-father |*> #=> father parent |_self>

grand-child |*> #=> child child |_self>

great-grand-child |*> #=> child child child |_self>

great-grand-parent |*> #=> parent parent parent |_self>

----------------------------------------
