
|context> => |context: bottles of beer>

n-1 |*> #=> arithmetic(|_self>, |->, |1>)

bottles |0> => |no more bottles>
bottles |1> => |1 bottle>
bottles |*> #=> |_self> __ |bottles>

first-line |*> #=> to-upper[1] bottles |_self> __ |of beer on the wall,> __ bottles |_self> __ |of beer.>

second-line |*> #=> |Take one down and pass it around,> __ bottles n-1 |_self> __ |of beer on the wall.>
second-line |0> => |Go to the store and buy some more, 99 bottles of beer on the wall.>

row |*> #=> first-line |_self> . second-line |_self> . | >
sing |*> #=> smerge["\n"] row sp2seq reverse range(|0>, |_self>)
