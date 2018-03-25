
----------------------------------------
 |context> => |context: The Matrix>
previous |context> => |context: global context>
source |context> => |url: https://www.youtube.com/watch?v=UodTzseLh04>
description |context> => |Introduction to Graph Databases>

name |node: 1> => |Thomas Anderson>
age |node: 1> => |29>
knows |node: 1> => |node: 7> + |node: 2>

name |node: 2> => |Trinity>
loves |node: 2> => |node: 1>

name |node: 7> => |Morpheus>
rank |node: 7> => |Captain>
occupation |node: 7> => |Total badass>
knows |node: 7> => |node: 2> + |node: 3>

name |node: 3> => |Cypher>
last-name |node: 3> => |Reagan>
knows |node: 3> => |node: 13>

name |node: 13> => |Agent Smith>
version |node: 13> => |1.0b>
language |node: 13> => |C++>
coded-by |node: 13> => |node: 42>

name |node: 42> => |The Architect>


inverse-name |Thomas Anderson> => |node: 1>
inverse-name |Trinity> => |node: 2>
inverse-name |Morpheus> => |node: 7>
inverse-name |Cypher> => |node: 3>
inverse-name |Agent Smith> => |node: 13>
inverse-name |The Architect> => |node: 42>

full-knows |*> #=> name clean drop (exp-max[knows] |_self> - |_self>)
----------------------------------------
