|context> => |context: visualizing edit distance>

  op1 |kitten> => substitute[s,k,0] |_self>
  op2 substitute[s,k,0] |kitten> => substitute[i,e,4] |_self>
  op3 substitute[i,e,4] substitute[s,k,0] |kitten> => insert[g,6] |_self>

  op4 |kitten> => delete[k,0] |_self>
  op5 op4 |kitten> => insert[s,0] |_self>
  op6 op5 op4 |kitten> => delete[e,4] |_self>
  op7 op6 op5 op4 |kitten> => insert[i,4] |_self>
  op8 op7 op6 op5 op4 |kitten> => insert[g,6] |_self>

