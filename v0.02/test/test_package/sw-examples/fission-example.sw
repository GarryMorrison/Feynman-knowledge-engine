
----------------------------------------
|context> => |context: uranium fission products>

fission-channel-1 |U: 235> => |Ba: 141> + |Kr: 92> + 3.0|n>
fission-channel-2 |U: 235> => |Xe: 140> + |Sr: 94> + 2.0|n>
fission-channel-3 |U: 235> => |La: 143> + |Br: 90> + 3.0|n>
fission-channel-4 |U: 235> => |Cs: 137> + |Rb: 96> + 3.0|n>
fission-channel-5 |U: 235> => |I: 131> + |Y: 89> + 16.0|n>
list-of-fission-channels |U: 235> => |op: fission-channel-1> + |op: fission-channel-2> + |op: fission-channel-3> + |op: fission-channel-4> + |op: fission-channel-5>

fission |*> #=> apply(weighted-pick-elt list-of-fission-channels |_self>, |_self>)

fission-uranium-235 (*) #=> process-reaction(|_self>,|n> + |U: 235>,fission |U: 235>)
----------------------------------------
