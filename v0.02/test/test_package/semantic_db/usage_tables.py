#######################################################################
# the semantic-db usage tables
# ie, our only current documentation
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 22/2/2018
# Update: 28/2/2018
# Copyright: GPLv3
#
# Usage:
#
#######################################################################

from semantic_db.functions import function_operators_usage, sequence_functions_usage


# define our usage report function:
def usage(ops = None):
  if ops is None:                  # print usage table
    s = 'Usage:\n'

    s += '  built in operators:\n'
    for key in sorted(built_in_table_usage):
      s += '    ' + key + '\n'

    s += '\n  sigmoids:\n'
    for key in sorted(sigmoid_table_usage):
      s += '    ' + key + '\n'

    s += '\n  function operators:\n'
    for key in sorted(function_operators_usage):
      s += '    ' + key + '\n'

    s += '\n  sequence functions:\n'
    for key in sorted(sequence_functions_usage):
      s += '    ' + key + '\n'

    s += '\n  worked examples:\n'
    for key in sorted(examples_usage):
      s += '    ' + key + '\n'


  else:
    s = 'Usage:\n'
    for op in ops:
      if op in built_in_table_usage:
        s += 'built in operator:\n'
        s += '  ' + op + ':\n'
        s += built_in_table_usage[op] + '\n'

      if op in sigmoid_table_usage:
        s += 'sigmoid:\n'
        s += '  ' + op + ':\n'
        s += sigmoid_table_usage[op] + '\n'

      if op in function_operators_usage:
        s += 'function operator:\n'
        s += '  ' + op + ':\n'
        s += function_operators_usage[op] + '\n'

      if op in sequence_functions_usage:
        s += 'sequence function:\n'
        s += '  ' + op + ':\n'
        s += sequence_functions_usage[op] + '\n'

      if op in examples_usage:
        s += 'worked example:\n'
        s += '  ' + op + ':\n'
        s += examples_usage[op] + '\n'


  print(s, end='')



# define our operator usage types:
built_in_table_usage = {}
sigmoid_table_usage = {}
fn_table_usage = {}
fn_table2_usage = {}
compound_table_usage = {}
sp_fn_table_usage = {}
ket_context_table_usage = {}
sp_context_table_usage = {}
whitelist_table_1_usage = {}
whitelist_table_2_usage = {}
whitelist_table_3_usage = {}
whitelist_table_4_usage = {}
context_whitelist_table_1_usage = {}
context_whitelist_table_2_usage = {}
context_whitelist_table_3_usage = {}
context_whitelist_table_4_usage = {}

examples_usage = {}

# fill out the built_in_table_usage dictionary:
built_in_table_usage['pick-elt'] = """
    description:
      randomly pick an element from the given superposition, with equal probability

    examples:
      pick-elt split |a b c d e>    
"""

built_in_table_usage['weighted-pick-elt'] = """
    description:
      randomly pick an element from the given superposition, weighted by the coefficients

    examples:
      weighted-pick-elt rank split |a b c d e>
"""

built_in_table_usage['normalize'] = """
    description:
      normalize the coefficients of the given superposition so they sum to 1

    examples:
      normalize split |a b c d e>
        0.2|a> + 0.2|b> + 0.2|c> + 0.2|d> + 0.2|e>

      normalize (2|a> + |b>)
        0.667|a> + 0.333|b>
"""

built_in_table_usage['sdrop'] = """
    description:
      sequence version of drop

    examples:

    see also:
      drop
"""

#built_in_table['sreverse'] = 'sreverse'
built_in_table_usage['sreverse'] = """
    description:
      sequence version of reverse

    examples:

    see also:
      reverse
"""



built_in_table_usage['z'] = """
    description:

    examples:
"""



# let's build the sigmoid_table_usage dictionary:
sigmoid_table_usage['clean'] = """
    description:
      clean the coefficients of the given superpostion
      if x < 0, return 0
      else return 1

    examples:
      clean (3|a> + 2.2|b> - 3 |c> + |d>)
        |a> + |b> + 0|c> + |d>
"""

sigmoid_table_usage['threshold-filter'] = """
    description:
      threshold filter
      if x < t, return 0
      else return x

    examples:
      threshold-filter[2] (3|a> + 2.2|b> - 3 |c> + |d>)
        3|a> + 2.2|b> + 0|c> + 0|d>
"""

sigmoid_table_usage['not-threshold-filter'] = """
    description:
      not threshold filter
      if x <= t, return x
      else return 0

    examples:
      not-threshold-filter[2] (3|a> + 2.2|b> - 3 |c> + |d>)
        0|a> + 0|b> + -3|c> + |d>
"""

sigmoid_table_usage['binary-filter'] = """
    description:
      binary filter
      if x <= 0.96, return 0
      else return 1

    examples:
      binary-filter (2|a> + 0.9|b> -2|c>)
        |a> + 0|b> + 0|c>
"""

sigmoid_table_usage['not-binary-filter'] = """
    description:
      binary filter
      if x <= 0.96, return 1
      else return 0

    examples:
      not-binary-filter (2|a> + 0.9|b> -2|c>)
        0|a> + |b> + |c>
"""

sigmoid_table_usage['pos'] = """
    description:
      positive filter
      if x <= 0, return 0
      else return x

    examples:
      pos (2|a> + 0.9|b> -2|c>)
        2|a> + 0.9|b> + 0|c>
"""

sigmoid_table_usage['abs'] = """
    description:
      absolute value

    examples:
      abs (2|a> + 0.9|b> -3|c>)
        2|a> + 0.9|b> + 3|c>
"""

sigmoid_table_usage['max-filter'] = """
    description:
      max filter
      if x <= t, return x
      else return t

    examples:

"""

sigmoid_table_usage['NOT'] = """
    description:
      binary not
      if x <= 0.04, return 1
      else return 0

    examples:

"""

sigmoid_table_usage['xor-filter'] = """
    description:
      xor
      if 0.96 <= x <= 1.04, return 1
      else return 0

    examples:

"""

sigmoid_table_usage['sigmoid-in-range'] = """
    description:
      the in-range sigmoid
      if a <= x <= b, return x
      else return 0

    examples:

"""

sigmoid_table_usage['invert'] = """
    description:
      multiplicative invert
      if x == 0, return 0
      else return 1/x

    examples:
      invert (0|x> + 3|y> - 0.5 |z>)
        0|x> + 0.333|y> - 2|z>
"""

sigmoid_table_usage['set-to'] = """
    description:
      set all coefficients to t
      return t

    examples:
      set-to[7] (0|x> + 3|y> - 0.5|z>)
        7|x> + 7|y> + 7|z>
"""

sigmoid_table_usage['subtraction-invert'] = """
    description:
      additive invert
      return t - x

    examples:
      subtraction-invert[0] (0|x> + 3|y> - 0.5|z>)
      0|x> + -3|y> + 0.5|z>
"""

sigmoid_table_usage['log'] = """
    description:
      logarithm of x
      if x <= 0, return 0
      if t is None, return math.log(x)  (ie, base e)
      else, return math.log(x, t)       (ie, base t)

    examples:
      log 2.71828|e>
        1.0|e>

      log[10] 100000 |x>
        5|x>
"""

sigmoid_table_usage['log+1'] = """
    description:
      logarithm of 1 + x
      if x <= 0, return 0
      if t is None, return math.log(1 + x)  (ie, base e)
      else, return math.log(1 + x, t)       (ie, base t)

    examples:

"""

sigmoid_table_usage['square'] = """
    description:
      square the coefficients

    examples:
      square (0.2|x> + 3|y> - 5|z>)
        0.04|x> + 9|y> + 25|z>
"""

sigmoid_table_usage['sqrt'] = """
    description:
      square root the coefficients

    examples:
      sqrt (9|x> + 25|y> + 49|z>)
        3|x> + 5|y> + 7|z>

      sqrt square (0.2|x> + 3|y> - 5|z>)
        0.2|x> + 3|y> + 5|z>
"""

sigmoid_table_usage['floor'] = """
    description:
      math.floor

    examples:
      floor (2.3|x> + 7.9|y>)
        2|x> + 7|y>
"""

sigmoid_table_usage['ceiling'] = """
    description:
      math.ceil

    examples:
      ceiling (2.3|x> + 7.9|y>)
        3|x> + 8|y>
"""

sigmoid_table_usage['inc'] = """
    description:
      increment the coefficient by one

    examples:
      inc |x>
        2|x>

      inc^7 0|x>
        7|x>
"""

sigmoid_table_usage['dec'] = """
    description:
      decrement the coefficient by one

    examples:
      dec |x>
        0|x>

      dec^10 0|x>
        -10 |x>
"""


examples_usage['numbers-to-words'] = """
    description:
      convert integers into words
      
    code:
      ones |0> #=> |>
      ones |1> => |one>
      ones |2> => |two>
      ones |3> => |three>
      ones |4> => |four>
      ones |5> => |five>
      ones |6> => |six>
      ones |7> => |seven>
      ones |8> => |eight>
      ones |9> => |nine>

      tens |10> => |ten>
      tens |11> => |eleven>
      tens |12> => |twelve>
      tens |13> => |thirteen>
      tens |14> => |fourteen>
      tens |15> => |fifteen>
      tens |16> => |sixteen>
      tens |17> => |seventeen>
      tens |18> => |eighteen>
      tens |19> => |nineteen>

      ten |20> => |twenty>
      ten |30> => |thirty>
      ten |40> => |forty>
      ten |50> => |fifty>
      ten |60> => |sixty>
      ten |70> => |seventy>
      ten |80> => |eighty>
      ten |90> => |ninety>

      tens |*> #=> smerge[" "] sdrop ( ten times-by[10] int-divide-by[10] |_self> . ones mod[10] |_self> )
      hundreds-rule |*> #=> smerge[" and "] (hundreds int-divide-by[100] mod[1000] |_self> . tens mod[100] |_self>)
      thousands-rule |*> #=> thousands int-divide-by[1000] mod[1000000] |_self>
      millions-rule |*> #=> millions int-divide-by[1000000] mod[1000000000] |_self>

      hundreds |0> #=> |>
      hundreds |*> #=> ones |_self> __ |hundred>

      thousands |0> #=> |>
      thousands |*> #=> hundreds-rule |_self> __ |thousand>

      millions |0> #=> |>
      millions |*> #=> hundreds-rule |_self> __ |million>

      n2w |0> => |zero>
      n2w |*> #=> smerge[", "] sdrop (millions-rule |_self> . thousands-rule |_self> . hundreds-rule |_self>)

    examples:
      n2w |0>
        |zero>

      n2w |3>
        |three>

      n2w |15>
        |fifteen>

      n2w |53>
        |fifty three>

      n2w |735>
        |seven hundred and thirty five>

      n2w |12000>
        |twelve thousand>

      n2w |12500>
        |twelve thousand, five hundred>

      n2w |987654321>
        |nine hundred and eighty seven million, six hundred and fifty four thousand, three hundred and twenty one>

      -- or all at once:
      table[number, n2w] split |0 3 15 53 735 12000 987654321>
        +-----------+----------------------------------------------------------------------------------------------------------+
        | number    | n2w                                                                                                      |
        +-----------+----------------------------------------------------------------------------------------------------------+
        | 0         | zero                                                                                                     |
        | 3         | three                                                                                                    |
        | 15        | fifteen                                                                                                  |
        | 53        | fifty three                                                                                              |
        | 735       | seven hundred and thirty five                                                                            |
        | 12000     | twelve thousand                                                                                          |
        | 987654321 | nine hundred and eighty seven million, six hundred and fifty four thousand, three hundred and twenty one |
        +-----------+----------------------------------------------------------------------------------------------------------+

    source code:
      load numbers-to-words.sw
"""

examples_usage['big-numbers-to-words'] = """
    description:
      convert integers into words

    code:
      ones |1> => |one>
      ones |2> => |two>
      ones |3> => |three>
      ones |4> => |four>
      ones |5> => |five>
      ones |6> => |six>
      ones |7> => |seven>
      ones |8> => |eight>
      ones |9> => |nine>

      tens |10> => |ten>
      tens |11> => |eleven>
      tens |12> => |twelve>
      tens |13> => |thirteen>
      tens |14> => |fourteen>
      tens |15> => |fifteen>
      tens |16> => |sixteen>
      tens |17> => |seventeen>
      tens |18> => |eighteen>
      tens |19> => |nineteen>

      ten |20> => |twenty>
      ten |30> => |thirty>
      ten |40> => |forty>
      ten |50> => |fifty>
      ten |60> => |sixty>
      ten |70> => |seventy>
      ten |80> => |eighty>
      ten |90> => |ninety>

      tens |*> #=> smerge[" "] sdrop ( ten times-by[10] int-divide-by[10] |_self> . ones mod[10] |_self> )
      hundreds-rule |*> #=> smerge[" and "] (hundreds int-divide-by[100] mod[1000] |_self> . tens mod[100] |_self>)

      hundreds |0> #=> |>
      hundreds |*> #=> ones |_self> __ |hundred>

      thousands |0> #=> |>
      thousands |*> #=> hundreds-rule |_self> __ |thousand>

      millions |0> #=> |>
      millions |*> #=> hundreds-rule |_self> __ |million>

      billions |0> #=> |>
      billions |*> #=> hundreds-rule |_self> __ |billion>

      trillions |0> #=> |>
      trillions |*> #=> hundreds-rule |_self> __ |trillion>

      op |seq> => |op: hundreds-rule> . |op: thousands> . |op: millions> . |op: billions> . |op: trillions>

      n2w |0> => |zero>
      n2w |*> #=> smerge[", "] sreverse op-zip(op |seq>, split-num |_self>)

      split-num |*> #=> process-if if(is-less-than[1000] |_self>, |less than 1000:> __ |_self>, |greater than 1000:> __ |_self>)
      process-if |less than 1000: *> #=> remove-leading-category |_self>
      process-if |greater than 1000: *> #=> mod[1000] remove-leading-category |_self> . split-num int-divide-by[1000] remove-leading-category |_self>

    examples:
      n2w |123456789012345>
        |one hundred and twenty three trillion, four hundred and fifty six billion, seven hundred and eighty nine million, twelve thousand, three hundred and forty five>

    source code:
      load big-numbers-to-words.sw      
"""

examples_usage['bottles-of-beer'] = """
    description:
      sing the bottles of beer song

    code:
      n-1 |*> #=> arithmetic(|_self>, |->, |1>)

      bottles |0> => |no more bottles>
      bottles |1> => |1 bottle>
      bottles |*> #=> |_self> __ |bottles>

      first-line |*> #=> to-upper[1] bottles |_self> __ |of beer on the wall,> __ bottles |_self> __ |of beer.>

      second-line |*> #=> |Take one down and pass it around,> __ bottles n-1 |_self> __ |of beer on the wall.>
      second-line |0> #=> |Go to the store and buy some more,> __ bottles max |bottles> __ |of beer on the wall.>

      row |*> #=> first-line |_self> . second-line |_self> . |>

      max |bottles> => |10>
      sing |*> #=> smerge["\\n"] row sp2seq reverse range(|0>, max |bottles>)

    examples:
      max |bottles> => |4>
      sing
        |4 bottles of beer on the wall, 4 bottles of beer.
        Take one down and pass it around, 3 bottles of beer on the wall.

        3 bottles of beer on the wall, 3 bottles of beer.
        Take one down and pass it around, 2 bottles of beer on the wall.

        2 bottles of beer on the wall, 2 bottles of beer.
        Take one down and pass it around, 1 bottle of beer on the wall.

        1 bottle of beer on the wall, 1 bottle of beer.
        Take one down and pass it around, no more bottles of beer on the wall.

        No more bottles of beer on the wall, no more bottles of beer.
        Go to the store and buy some more, 4 bottles of beer on the wall.
        >

    source code:
      load bottles-of-beer.sw
"""

examples_usage['eat-from-can'] = """
    description:
      use consume-reaction to open and then eat from a can
      
    code:
      current |state> => words-to-list |can opener, closed can and hungry>
      learn-state (*) #=> learn(|op: current>, |state>, |_self>)
      use |can opener> #=> learn-state consume-reaction(current |state>, |closed can>, |open can>)
      eat-from |can> #=> learn-state consume-reaction(current |state>, |open can> + |hungry>, |empty can> + |not hungry>)

    examples:
      current |state>
        |can opener> + |closed can> + |hungry>

      use |can opener>
        |can opener> + |hungry> + |open can>

      eat-from |can>
        |can opener> + |empty can> + |not hungry>

    source code:
      load eat-from-can.sw
"""

examples_usage['greetings'] = """
    description:
      random greet a list of people      

    code:
      hello |*> #=> |Hello,> __ |_self> _ |!>
      hey |*> #=> |Hey Ho!> __ |_self> _ |.>
      wat-up |*> #=> |Wat up my homie!> __ |_self> __ |right?>
      greetings |*> #=> |Greetings fine Sir. I belive they call you> __ |_self> _ |.>
      howdy |*> #=> |Howdy partner!>
      good-morning |*> #=> |Good morning> __ |_self> _ |.>
      gday |*> #=> |G'day> __ |_self> _ |.>

      list-of |greetings> => |op: hello> + |op: hey> + |op: wat-up> + |op: greetings> + |op: howdy> + |op: good-morning> + |op: gday>
      greet (*) #=> apply(pick-elt list-of |greetings>, list-to-words |_self>)

      friends |Sam> => |Charlie> + |George> + |Emma> + |Jack> + |Robert> + |Frank> + |Julie>
      friends |Emma> => |Liz> + |Bob>

   examples:
     greet (|Sam> + |Jack>)
       |G'day Sam and Jack.>

     greet friends |Sam>
       |Hey Ho! Charlie, George, Emma, Jack, Robert, Frank and Julie.>

     greet friends |Emma>
       |Wat up my homie! Liz and Bob right?>

    source code:
      load greetings.sw
"""

examples_usage['fission-uranium'] = """
    description:
      another example of consume-reaction()
      this time a toy example of fissioning uranium 235

    code:
      fission-channel-1 |U: 235> => |Ba: 141> + |Kr: 92> + 3|n>
      fission-channel-2 |U: 235> => |Xe: 140> + |Sr: 94> + 2|n>
      fission-channel-3 |U: 235> => |La: 143> + |Br: 90> + 3|n>
      fission-channel-4 |U: 235> => |Cs: 137> + |Rb: 96> + 3|n>
      fission-channel-5 |U: 235> => |I: 131> + |Y: 89> + 16|n>

      -- a more realistic example would have probabilities, as coefficients, for each of the channels.
      list-of-fission-channels |U: 235> => |op: fission-channel-1> + |op: fission-channel-2> + |op: fission-channel-3> + |op: fission-channel-4> + |op: fission-channel-5>

      fission |*> #=> apply(weighted-pick-elt list-of-fission-channels |_self>, |_self>)

      fission-uranium-235 (*) #=> consume-reaction(|_self>,|n> + |U: 235>,fission |U: 235>)

    examples:
      fission |U: 235>
        |Xe: 140> + |Sr: 94> + 2|n>

      fission |U: 235>
        |La: 143> + |Br: 90> + 3|n>

      fission |U: 235>
        |I: 131> + |Y: 89> + 16|n>

      fission-uranium-235 (|n> + 10|U: 235>)
        9|U: 235> + |Cs: 137> + |Rb: 96> + 3|n>

      fission-uranium-235^50 (|n> + 100|U: 235>)
        50|U: 235> + 12|Ba: 141> + 12|Kr: 92> + 237|n> + 11|I: 131> + 11|Y: 89> + 7|Xe: 140> + 7|Sr: 94> + 12|La: 143> + 12|Br: 90> + 8|Cs: 137> + 8|Rb: 96>

    source code:
      load fission-uranium.sw
"""

examples_usage['simple-adjective-sentence'] = """
    description:
      proof of concept of writing sentences
      in this case a simple adjective sentence
      obviously, the plan is to scale this up massively
      also, the plan is to eventually auto-learn adjectives from reading text
      but that is a ways off!!

    code:
      current |person> => |old man>
      learn-person |*> #=> learn(|op: current>, |person>, |_self>)

      adjectives |old man> => 10|crotchety> + 8|grumpy> + 5|friendly> + |kindly> + 0.2|sleepy>
      comma |old man> => |,>
      
      adjectives |old woman> => 2|kindly> + |sleepy> + |pleasant> + |strange>
      comma |old woman> => |,>
      
      adjectives |teenager> => |enthusiastic> + |energetic>
      comma |teenager> #=> |>

      pick-adjective (*) #=> clean weighted-pick-elt adjectives |_self>
      how-many-adjectives |*> #=> clean weighted-pick-elt (8|0> + 2|1> + 0.5|2> + 0.2|3>)


      insert-adjective |*> #=> |>
      insert-adjective |1> #=> ( pick-adjective _ comma ) current |person>
      insert-adjective |2> #=> ( pick-adjective . pick-adjective _ comma ) current |person>
      insert-adjective |3> #=> ( pick-adjective . pick-adjective . pick-adjective _ comma ) current |person>

      adjective-list |*> #=> smerge[", "] insert-adjective how-many-adjectives learn-person |_self>

      the-sentence |*> #=> smerge[" "] sdrop (|The> . adjective-list |_self> . |_self> _ |.>)
      sentence |*> #=> the-sentence pick-elt (|old man> + |old woman> + |teenager>)

    examples:
      sentence
        |The kindly, old man.>

      sentence
        |The old woman.>

      sentence
        |The teenager.>

      sentence
        |The strange, kindly, old woman.>

      sentence
        |The energetic teenager.>

    source code:
      load the-old-man.sw
"""

examples_usage['random-sentence'] = """
    description:
      learn some sentence fragments, and then produce a valid sentence
      motivated by this: http://write-up.semantic-db.org/221-generating-random-grammatically-correct-sentences.html

      in gm notation:
        A = {the.woman.saw}
        B = {through.the.telescope}
        C = {{}, young}
        D = {girl, boy}
        E = {{}, old, other}
        F = {man, woman, lady}
        G = E.F
        H = {the}
        I = H.C.D
        J = H.E.F
        K = {{},I,J}

        L = A.K.B

        M = {I,J}
        N = {saw}
        O = M.N.K.B

        P = {through.the}
        Q = {telescope, binoculars, night.vision.goggles}

        R = M.N.K.P.Q

    code:
      frag |A> => |the woman saw>
      frag |B> => |through the telescope>
      frag |C> #=> spick-elt (|> . |young>)
      frag |D> #=> spick-elt (|girl> . |boy>)
      frag |E> #=> spick-elt (|> . |old> . |other>)
      frag |F> #=> spick-elt (|man> . |woman> . |lady>)
      frag |G> #=> frag (|E> . |F>)
      frag |H> => |the>
      frag |I> #=> frag (|H> . |C> . |D>)
      frag |J> #=> frag (|H> . |E> . |F>)
      frag |K> #=> frag spick-elt (|> . |I> . |J>)
      frag |L> #=> frag (|A> . |K> . |B>)
      frag |M> #=> frag spick-elt (|I> . |J>)
      frag |N> => |saw>
      frag |O> #=> frag (|M> . |N> . |K> . |B>)
      frag |P> => |through the>
      frag |Q> #=> spick-elt (|telescope> . |binoculars> . |night vision goggles>)
      frag |R> #=> frag (|M> . |N> . |K> . |P> . |Q>)

      sentence |*> #=> to-upper[1] smerge[" "] sdrop frag |R> _ |.>

    examples:
      sentence
        |The other lady saw the old woman through the telescope.>

      sentence
        |The young boy saw the young girl through the binoculars.>

      sentence
        |The old woman saw the other man through the telescope.>

      sentence
        |The young boy saw the young girl through the night vision goggles.>

    future:
      scale it up, and maybe write a gm-to-code converter?

    source code:
      load the-woman-saw.sw
"""

examples_usage['active-logic'] = """
    description:
      proof of concept using simple if-then machines
      in this case, concerning wet grass, the sprinkler and rain

    code:
      -- learn the meaning of not:
      not |no> => |yes>
      not |yes> => |no>
      not |don't know> => |don't know>

      -- define our if-then machines:
      pattern |node 1: 1> => |grass is wet> + |not rained last night>
      then |node 1: 1> => 2.0|sprinkler was on> + -1.0|rained last night> + -1.0|not grass is wet>

      pattern |node 2: 1> => |grass is wet> + |not sprinkler was on>
      then |node 2: 1> => 2.0|rained last night> + -1.0|sprinkler was on> + -1.0|not grass is wet>

      pattern |node 3: 1> => |sprinkler was on>
      then |node 3: 1> => |grass is wet> + -1.0|not sprinkler was on>

      pattern |node 3: 2> => |rained last night>
      then |node 3: 2> => |grass is wet> + -1.0|not rained last night>

      pattern |node 4: 1> => |not rained last night> + |not sprinkler was on>
      then |node 4: 1> => 2.0|not grass is wet> + -1.0|rained last night> + -1.0|sprinkler was on>


      -- learn state of activation:
      active |rained last night> => |don't know>
      active |not rained last night> #=> not active |rained last night>
      active |sprinkler was on> => |don't know>
      active |not sprinkler was on> #=> not active |sprinkler was on>
      active |grass is wet> => |don't know>
      active |not grass is wet> #=> not active |grass is wet>


      -- activation states we want to unlearn:
      the-unlearn |list> => |rained last night> + |sprinkler was on> + |grass is wet>


      -- unlearn operators:
      unlearn |*> #=> learn(|op: active>, |_self>, |don't know>)
      unlearn-everything |*> #=> unlearn the-unlearn |list>


      -- our 'active' operators:
      make-active |*> #=> learn(|op: active>, remove-prefix["not "] |_self>, not has-prefix["not "] |_self>)
      currently-active |*> #=> such-that[active] rel-kets[active] |>
      read-sentence |*> #=> make-active words-to-list |_self>


      -- define our conclude operators:
      conclude |*> #=> drop then similar-input[pattern] such-that[active] rel-kets[active] |>
      inverse-conclude |*> #=> pattern similar-input[then] such-that[active] rel-kets[active] |>


      -- define short-cuts for our tables:
      t |*> #=> table[state, unlearn-everything, read-sentence, currently-active, conclude, inverse-conclude] the-list-of |states>
      t2 |*> #=> table[state, unlearn-everything, read-sentence, currently-active, conclude] the-list-of |states>


      -- learn the list of states we want in our tables:
      the-list-of |states> => |grass is wet>
      the-list-of |states> +=> |sprinkler was on>
      the-list-of |states> +=> |rained last night>
      the-list-of |states> +=> |sprinkler was on and rained last night>
      the-list-of |states> +=> |grass is wet and not rained last night>
      the-list-of |states> +=> |grass is wet and not sprinkler was on>
      the-list-of |states> +=> |not rained last night>
      the-list-of |states> +=> |not sprinkler was on>
      the-list-of |states> +=> |not rained last night and not sprinkler was on>
      the-list-of |states> +=> |not grass is wet>

    examples:
      unlearn-everything
        3|don't know>

      read-sentence |grass is wet and not rained last night>
        |yes> + |no>

      currently-active
        |not rained last night> + |grass is wet>

      conclude
        |sprinkler was on>


      t2
        +------------------------------------------------+--------------------+---------------+---------------------------------------------+-----------------------------------------------+
        | state                                          | unlearn-everything | read-sentence | currently-active                            | conclude                                      |
        +------------------------------------------------+--------------------+---------------+---------------------------------------------+-----------------------------------------------+
        | grass is wet                                   | 3 don't know       | yes           | grass is wet                                | 0.50 sprinkler was on, 0.50 rained last night |
        | sprinkler was on                               | 3 don't know       | yes           | sprinkler was on                            | grass is wet                                  |
        | rained last night                              | 3 don't know       | yes           | rained last night                           | grass is wet                                  |
        | sprinkler was on and rained last night         | 3 don't know       | 2 yes         | rained last night, sprinkler was on         | grass is wet                                  |
        | grass is wet and not rained last night         | 3 don't know       | yes, no       | not rained last night, grass is wet         | sprinkler was on                              |
        | grass is wet and not sprinkler was on          | 3 don't know       | yes, no       | not sprinkler was on, grass is wet          | rained last night                             |
        | not rained last night                          | 3 don't know       | no            | not rained last night                       | 0.50 sprinkler was on, 0.50 not grass is wet  |
        | not sprinkler was on                           | 3 don't know       | no            | not sprinkler was on                        | 0.50 rained last night, 0.50 not grass is wet |
        | not rained last night and not sprinkler was on | 3 don't know       | 2 no          | not rained last night, not sprinkler was on | not grass is wet                              |
        | not grass is wet                               | 3 don't know       | no            | not grass is wet                            |                                               |
        +------------------------------------------------+--------------------+---------------+---------------------------------------------+-----------------------------------------------+

    source code:
      load improved-active-logic.sw
"""

examples_usage['temperature-conversions'] = """
    description:
      converting between Fahrenheit, Celsius and Kelvin

    code:
      to-Kelvin |K: *> #=> |_self>
      to-Celsius |K: *> #=> |C:> __ round[2] minus[273.15] extract-value |_self>
      to-Fahrenheit |K: *> #=> |F:> __ round[2] minus[459.67] times-by[9/5] extract-value |_self>

      to-Kelvin |C: *> #=> |K:> __ round[2] plus[273.15] extract-value |_self>
      to-Celsius |C: *> #=> |_self>
      to-Fahrenheit |C: *> #=> |F:> __ round[2] plus[32] times-by[9/5] extract-value |_self>

      to-Kelvin |F: *> #=> |K:> __ round[2] times-by[5/9] plus[459.67] extract-value |_self>
      to-Celsius |F: *> #=> |C:> __ round[2] times-by[5/9] minus[32] extract-value |_self>
      to-Fahrenheit |F: *> #=> |_self>

      to-K |*> #=> to-Kelvin |_self>
      to-C |*> #=> to-Celsius |_self>
      to-F |*> #=> to-Fahrenheit |_self>

    examples:
      to-F |C: 42>
        |F: 107.6>

      to-C |F: 50>
        |C: 10>

      to-K |C: 0>
        |K: 273.15>

      to-F |C: 100>
        |F: 212>

    source code:
      load temperature-conversion.sw
"""

examples_usage['Fibonacci-and-factorial'] = """
    description:
      simple recursive Fibonacci and factorial
      NB: we use !=> instead of #=>
      ie, memoizing rules instead of plain stored-rules.
      otherwise this code gets very slow, very fast.

    code:
      fib |0> => |0>
      fib |1> => |1>
      fib |*> !=> arithmetic( fib minus[1] |_self>, |+>, fib minus[2] |_self>)
      fib-ratio |*> !=> arithmetic( fib |_self> , |/>, fib minus[1] |_self> )

      fact |0> => |1>
      fact |*> !=> arithmetic(|_self>, |*>, fact minus[1] |_self>)

    examples:
      table[number, fib, fib-ratio, fact] range(|1>, |30>)
        +--------+--------+--------------------+-----------------------------------+
        | number | fib    | fib-ratio          | fact                              |
        +--------+--------+--------------------+-----------------------------------+
        | 1      | 1      |                    | 1                                 |
        | 2      | 1      | 1.0                | 2                                 |
        | 3      | 2      | 2.0                | 6                                 |
        | 4      | 3      | 1.5                | 24                                |
        | 5      | 5      | 1.6666666666666667 | 120                               |
        | 6      | 8      | 1.6                | 720                               |
        | 7      | 13     | 1.625              | 5040                              |
        | 8      | 21     | 1.6153846153846154 | 40320                             |
        | 9      | 34     | 1.619047619047619  | 362880                            |
        | 10     | 55     | 1.6176470588235294 | 3628800                           |
        | 11     | 89     | 1.6181818181818182 | 39916800                          |
        | 12     | 144    | 1.6179775280898876 | 479001600                         |
        | 13     | 233    | 1.6180555555555556 | 6227020800                        |
        | 14     | 377    | 1.6180257510729614 | 87178291200                       |
        | 15     | 610    | 1.6180371352785146 | 1307674368000                     |
        | 16     | 987    | 1.618032786885246  | 20922789888000                    |
        | 17     | 1597   | 1.618034447821682  | 355687428096000                   |
        | 18     | 2584   | 1.6180338134001253 | 6402373705728000                  |
        | 19     | 4181   | 1.618034055727554  | 121645100408832000                |
        | 20     | 6765   | 1.6180339631667064 | 2432902008176640000               |
        | 21     | 10946  | 1.6180339985218033 | 51090942171709440000              |
        | 22     | 17711  | 1.618033985017358  | 1124000727777607680000            |
        | 23     | 28657  | 1.6180339901755971 | 25852016738884976640000           |
        | 24     | 46368  | 1.618033988205325  | 620448401733239439360000          |
        | 25     | 75025  | 1.618033988957902  | 15511210043330985984000000        |
        | 26     | 121393 | 1.6180339886704431 | 403291461126605635584000000       |
        | 27     | 196418 | 1.6180339887802426 | 10888869450418352160768000000     |
        | 28     | 317811 | 1.618033988738303  | 304888344611713860501504000000    |
        | 29     | 514229 | 1.6180339887543225 | 8841761993739701954543616000000   |
        | 30     | 832040 | 1.6180339887482036 | 265252859812191058636308480000000 |
        +--------+--------+--------------------+-----------------------------------+
"""

examples_usage['walking-a-grid'] = """
    description:
      a fun little insect with minimal intelligence.
      with current settings it heads mostly in a south direction (but this is easy to change)
      when it thinks it has hit the edge of the map, it changes its heading by turning right
      the numbers are how many time-steps the insect has been on that location
      ### is the current location of our insect

    code:
      -- learn map:
      |null> => learn-map[30,30]

      -- learn current location:
      current |cell> => |grid: 1: 22>

      -- define turn-right operator:
      turn-right |op: S> => |op: W>
      turn-right |op: SW> => |op: NW>
      turn-right |op: W> => |op: N>
      turn-right |op: NW> => |op: NE>
      turn-right |op: N> => |op: E>
      turn-right |op: NE> => |op: SE>
      turn-right |op: E> => |op: S>
      turn-right |op: SE> => |op: SW>

      -- define walk direction:
      heading |ops> => 0.25|op: SW> + |op: S> + 0.25|op: SE>
      -- heading |ops> => |op: S>
      next |*> #=> set-to[1] apply(weighted-pick-elt heading |ops>, |_self>)

      -- define turn-heading-right operator:
      turn-heading-right |*> #=> learn(|op: heading>, |ops>, turn-right heading |ops>)

      -- define step operator:
      step |*> #=> process-if if(do-you-know next |_self>, |valid step:> __ |_self>, |not valid step:> __ |_self>)
      process-if |valid step: *> #=> next remove-leading-category |_self>
      process-if |not valid step: *> #=> sselect[1,1] (remove-leading-category |_self> . turn-heading-right |>)
      -- process-if |not valid step: *> #=> sdrop (remove-leading-category |_self> . set-to[0] turn-heading-right |>)

      -- update-map operators (increment current spot, take a step, and display map):
      inc |*> #=> learn(|op: value>, current |cell>, plus[1] value current |cell>)
      n |*> #=> learn(|op: current>, |cell>, step current |cell>)
      d |*> #=> display-map[30,30]


      -- single map update:
      line |*> #=> inc |_self> . n |_self> . d |_self>

      -- set max steps:
      max |steps> => |30>

      -- walk max steps:
      walk |*> #=> sdrop set-to[0] line sp2seq range(|1>, max |steps>)

    examples:
      -- load the code:
      load walk-grid-v2.sw

      -- switch off info printing. 
      -- this is important if you want a clean display of the maps
      info off

      -- walk the map:
      walk
      walk
      walk
        h: 30
        w: 30
        1     .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
        2     .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
        3     .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .
        4     .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
        5     .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
        6     .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
        7     .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
        8     .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .
        9     .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .
        10    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .
        11    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .
        12    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .
        13    2  1  1  .  .  .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .
        14    .  1  .  1  1  1  .  1  1  1  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .
        15    .  .  1  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .
        16    .  1  .  .  .  .  .  .  .  .  .  1  1  1  1  1  1###  .  .  .  .  1  .  .  .  .  .  .  .
        17    .  .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
        18    .  .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
        19    .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
        20    2  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
        21    1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
        22    1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
        23    .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .
        24    .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .
        25    .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .
        26    .  .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .
        27    .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
        28    .  .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
        29    .  .  1  .  .  .  .  .  .  .  .  .  .  1  .  1  1  .  .  .  .  1  .  .  .  .  .  .  .  .
        30    .  .  2  1  2  1  1  1  1  1  1  1  2  .  1  .  .  1  1  1  2  3  .  .  .  .  .  .  .  .


      walk^5
        h: 30
        w: 30
        1     .  .  .  .  .  .  3  2  2  3  .  .  .  .  .  .  .  .  2  1  1  2  1  1  .  3  1  1  1  2
        2     .  .  .  .  .  .  .  .  .  1  1  1  1  .  .  .  .  .  1  2  1  2  .  .  1  .  .  .  .  1
        3     .  .  .  .  .  .  .  .  .  .  1  .  .  1  1  1  1  1  .  1  .  1  1  1  1  .  1  .  .  1
        4     .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  1  .  1  .  .  .  1  .  1  1  .
        5     .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  1  .  .  1  .  .  .  .  .  1  2
        6     .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  1  .  .  1  .  .  .  .  .  .  .
        7     .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  1  .  .  1  .  .  .  .  .  .  .
        8     .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .  .  .
        9     .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .  .  .
        10    .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .  .  .
        11    .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .  .  .
        12    .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .  .  .
        13    .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .  .  .  .
        14    .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .  .  .  .
        15    .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  1  .  .  1  .  .  .  .  .  .  .
        16    .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  1  .  .  .  1  .  .  .  .  .  .
        17    .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  .  1  .  .  1  .  .  .  .  .  .
        18    .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .  .  .
        19    .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  .  1  .  .  1  .  .  .  .  .  .
        20    .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .  .  .
        21    .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  .  1  .  .  1  .  .  .  .  .  .
        22    .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  1  .  .  .  1  .  .  .  .  .  .
        23    .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  1  .  .  .  .  1  .  .  .  .  .
        24    .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  1  .  .  .  .  1  .  .  .  .  .
        25    .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  1  .  .  .  1  .  .  .  .  .
        26    .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  1  .  .  .  1  .  .  .  .  .
        27    .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  1  .  .  1  .  .  .  .  .  .
        28    .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  1  .  .  1  .  .  .  .  .
        29    .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .
        30    .  .  .  .  .###  1  1  2  1  1  2  .  .  .  .  .  .  .  .  .  .  2  1  1  2  .  .  .  .

    source code:
      load walk-grid-v2.sw
"""
