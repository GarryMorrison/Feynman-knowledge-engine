
----------------------------------------
|context> => |context: Fibonacci>

supported-ops |0> => |op: fib>
fib |0> => |1>

supported-ops |1> => |op: fib>
fib |1> => |1>

supported-ops |*> => |op: n-1> + |op: n-2> + |op: fib> + |op: fib-ratio>
n-1 |*> #=> arithmetic(|_self>,|->,|1>)
n-2 |*> #=> arithmetic(|_self>,|->,|2>)
fib |*> #=> arithmetic( fib n-1 |_self>, |+>, fib n-2 |_self>)
fib-ratio |*> #=> arithmetic( fib |_self> , |/>, fib n-1 |_self> )

supported-ops |2> => |op: fib>
fib |2> => |2>

supported-ops |3> => |op: fib>
fib |3> => |3>

supported-ops |4> => |op: fib>
fib |4> => |5>

supported-ops |5> => |op: fib>
fib |5> => |8>

supported-ops |6> => |op: fib>
fib |6> => |13>

supported-ops |7> => |op: fib>
fib |7> => |21>

supported-ops |8> => |op: fib>
fib |8> => |34>

supported-ops |9> => |op: fib>
fib |9> => |55>

supported-ops |10> => |op: fib>
fib |10> => |89>

supported-ops |11> => |op: fib>
fib |11> => |144>

supported-ops |12> => |op: fib>
fib |12> => |233>

supported-ops |13> => |op: fib>
fib |13> => |377>

supported-ops |14> => |op: fib>
fib |14> => |610>

supported-ops |15> => |op: fib>
fib |15> => |987>

supported-ops |16> => |op: fib>
fib |16> => |1597>

supported-ops |17> => |op: fib>
fib |17> => |2584>

supported-ops |18> => |op: fib>
fib |18> => |4181>

supported-ops |19> => |op: fib>
fib |19> => |6765>

supported-ops |20> => |op: fib>
fib |20> => |10946>

supported-ops |21> => |op: fib>
fib |21> => |17711>

supported-ops |22> => |op: fib>
fib |22> => |28657>

supported-ops |23> => |op: fib>
fib |23> => |46368>

supported-ops |24> => |op: fib>
fib |24> => |75025>

supported-ops |25> => |op: fib>
fib |25> => |121393>

supported-ops |26> => |op: fib>
fib |26> => |196418>

supported-ops |27> => |op: fib>
fib |27> => |317811>

supported-ops |28> => |op: fib>
fib |28> => |514229>

supported-ops |29> => |op: fib>
fib |29> => |832040>

supported-ops |30> => |op: fib>
fib |30> => |1346269>
----------------------------------------
