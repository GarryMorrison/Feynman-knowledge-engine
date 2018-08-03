|context> => |context: eat from can>

current |state> => words-to-list |can opener, closed can and hungry>
learn-state (*) #=> learn(|op: current>, |state>, |_self>)
use |can opener> #=> learn-state process-reaction(current |state>, |can opener> + |closed can>, |can opener> + |open can>)
eat-from |can> #=> learn-state process-reaction(current |state>, |open can> + |hungry>, |empty can> + |not hungry>)

