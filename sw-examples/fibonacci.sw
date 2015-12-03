|context> => |context: Fibonacci>

-- this has been wrong for a long time now!
-- time to correct it
-- fib |0> => |0>
fib |0> => |1>
fib |1> => |1>

n-1 |*> #=> arithmetic(|_self>,|->,|1>)
n-2 |*> #=> arithmetic(|_self>,|->,|2>)
fib |*> #=> arithmetic( fib n-1 |_self>, |+>, fib n-2 |_self>)
fib-ratio |*> #=> arithmetic( fib |_self> , |/>, fib n-1 |_self> )
