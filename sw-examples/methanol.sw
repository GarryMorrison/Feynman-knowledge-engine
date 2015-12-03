|context> => |context: methanol>


molecular-pieces |molecule: methanol> => |methanol: 1> + |methanol: 2> + |methanol: 3> + |methanol: 4> + |methanol: 5> + |methanol: 6>

atom-type |methanol: 1> => |atom: H>
bonds-to |methanol: 1> => |methanol: 4>

atom-type |methanol: 2> => |atom: H>
bonds-to |methanol: 2> => |methanol: 4>

atom-type |methanol: 3> => |atom: H>
bonds-to |methanol: 3> => |methanol: 4>

atom-type |methanol: 4> => |atom: C>
bonds-to |methanol: 4> => |methanol: 1> + |methanol: 2> + |methanol: 3> + |methanol: 5>

atom-type |methanol: 5> => |atom: O>
bonds-to |methanol: 5> => |methanol: 4> + |methanol: 6>

atom-type |methanol: 6> => |atom: H>
bonds-to |methanol: 6> => |methanol: 5>

