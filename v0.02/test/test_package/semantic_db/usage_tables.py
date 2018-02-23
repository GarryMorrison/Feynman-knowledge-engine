#######################################################################
# the semantic-db usage tables
# ie, our only current documentation
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 22/2/2018
# Update: 23/2/2018
# Copyright: GPLv3
#
# Usage:
#
#######################################################################

from semantic_db.functions import function_operators_usage, superposition_functions_usage


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

    s += '\n  superposition functions:\n'
    for key in sorted(superposition_functions_usage):
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

      if op in superposition_functions_usage:
        s += 'superposition function:\n'
        s += '  ' + op + ':\n'
        s += superposition_functions_usage[op] + '\n'


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

