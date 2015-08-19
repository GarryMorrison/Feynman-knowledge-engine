
#######################################################################
# the semantic-db parser
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2014
# Update: 19/8/2015
# Copyright: GPLv3
#
# Usage: 
#
#######################################################################

from string import ascii_letters
import copy
import os
from parsley import makeGrammar

from the_semantic_db_code import *
from the_semantic_db_functions import *


# Some hash tables mapping ops to the python equivalent.
# Left hand side is BKO language, right is python.

# functions built into ket/superposition classes.
built_in_table = {
  "display"          : "display",
  "transpose"        : "transpose",
# "select-elt"       : "select_elt",
  "pick-elt"         : "pick_elt",
  "pick-an-element-from" : "pick_elt", # added 13/7/2015, to make it closer to natural language
  "weighted-pick-elt" : "weighted_pick_elt", # added 5/8/2015. Been meaning to add this one for a long time! 
# "find-index"       : "find_index",
# "find-value"       : "find_value",
  "normalize"        : "normalize",
  "rescale"          : "rescale",
# "rescale"          : "rescale",
# "sigmoid"          : "apply_sigmoid",
# "function"         : "apply_fn",
# "similar"          : "similar",
# "collapse-fn"      : "apply_fn_collapse",
  "collapse"         : "collapse",
  "count"            : "number_count",
  "how-many"         : "number_count",
  "count-sum"        : "number_count_sum",
  "sum"              : "number_count_sum",
  "measure-currency" : "number_count_sum",  
  "product"          : "number_product",
  "drop"             : "drop",
# "drop-below"       : "drop_below",
# "drop-above"       : "drop_above",
# "select-range"     : "select_range",
# "delete-elt"       : "delete_elt",
  "reverse"          : "reverse",
  "shuffle"          : "shuffle",
  "coeff-sort"       : "coeff_sort",
  "ket-sort"         : "ket_sort",
  "max-elt"          : "find_max_elt",
  "min-elt"          : "find_min_elt",
  "max"              : "find_max",
  "min"              : "find_min",

# new:
  "discrimination"   : "discrimination",
  "discrim"          : "discrimination",

# special:
    "type"           : "type",                    # implemented for debugging purposes.

# new 7/9/2014:
#  "long"            : "long_display",
# new, 4/1/2015:
  "not-empty"        : "is_not_empty",
  "do-you-know"      : "is_not_empty",

# new 6/1/2015:
  "max-coeff"        : "number_find_max_coeff",
  "min-coeff"        : "number_find_min_coeff",

# 17/7/2015: our first compound op in this table. Normally you would put this in the compound op table, but it has no parameters, so it wont work there! (I tried).
# yeah, sloppy code though! I find this somewhat unpleasant!
# hopefully we eventually find a cleaner way to do all this.
# and by "this", I mean all these different tables and so on.   
  "reverse-rank"     : "reverse().apply_sp_fn(rank).reverse",
  
}                                                                                      

# table of sigmoids:
sigmoid_table = {
  "clean"              : "clean",
# "threshold-filter"   : "threshold_filter",   # we can't handle paramters with our ops yet.
  "binary-filter"      : "binary_filter",
  "not-binary-filter"  : "not_binary_filter",
  "pos"                : "pos",
  "NOT"                : "NOT",
  "xor-filter"         : "xor_filter",
# "mult"               : "mult",               # yeah, the sigmoid version works, but moved to compound table 
                                              # ".multiply({0})" Decided it was common enough that it needed to be built in.
  "invert"             : "invert",

# 4/5/2015:
  "sigmoid-abs"        : "sigmoid_abs",       # maybe just call it "abs"? We only need the "sigmoid_" prefix for python, so not to stomp on abs().
  "abs"                : "sigmoid_abs",
}                                   

# some ket -> ket functions:
fn_table = {
  "apply-value"      : "apply_value",
  "extract-category" : "extract_category",
  "extract-value"    : "extract_value",
  "to-number"        : "category_number_to_number",
  "shout"            : "shout",
#  "discrim"           : "discrimination",  # Broken. discrim (3|a> + 9|b>) returns 12| >. Doh! It should be 9 - 3, not 9 + 3.
  "F"                : "to_Fahrenheit",     # should these be to-F, to-C, to-K?
  "C"                : "to_Celsius",
  "K"                : "to_Kelvin",
  "to-km"            : "to_km",
  "to-meter"         : "to_meter",
  "to-mile"          : "to_mile",
  "to-miles"         : "to_mile",
  
  "to-value"         : "to_value",
  "to-category"      : "to_category",
  
# 3/6/2014:
  "day-of-the-week"  : "day_of_the_week",

# 23/6/2014:
  "long"             : "long_display",            # BUG! I have no idea why this insists on using the "37|ket>"" instead of "37 ket" notation!
  "split"            : "split_ket",               # ahh.... it is running long_display with respect to kets, not superposition as I expected!
                                                  # maybe shift to another table to fix.
# 29/6/2014:
#  "sp-as-list"       : "sp_as_list",             # Nope! Belongs in the sp_fn_table.

# 10/11/2014:
  "expand-hierarchy" : "expand_hierarchy",
  "chars"            : "chars",
  
# 4/1/2015:
  "pop-float"        : "pop_float",
  "push-float"       : "push_float",
  "cat-depth"        : "category_depth", 
  
# 4/2/2015:
  "to-comma-number"  : "number_to_comma_number",
  
# 5/2/2015:
  "current-time"     : "current_time",
  "current-date"     : "current_date",
  
# 9/2/2015:
  "extract-3-tail"   : "extract_3_tail",
# 19/7/2015:
  "extract-3-tail-chars"   : "extract_3_tail_chars",
  

# 1/3/2015:
  "to-coeff"         : "to_coeff",

# 3/3/2015:
  "extract-movie-year" : "extract_year",
  "ket-length"         : "ket_length", 

# 27/4/2015:
  "lower-case"         : "lower_case",
  "upper-case"         : "upper_case",
  "one-gram"           : "one_gram",
# 14/5/2015:
  "two-gram"           : "two_gram",
  "three-gram"         : "three_gram",  

# 30/4/2015:
  "plus-or-minus"      : "plus_or_minus",  

# 5/8/2015:
  "split-chars"        : "split_chars",  
}


# 7/4/2014 me wonders. do fn_table and fn_table2 really need to be separate?  
# some other functions. Some are ket -> ket, some are ket -> superposition.
fn_table2 = {
  "read"              : "read_text",
  "spell"             : "spell_word",
# don't get the point of this one!
#  "factor"            : "factor_numbers",
  "factor"            : "factor_number",
  "near-number"       : "near_numbers",
  "strange-int"       : "strange_int",
  "is-prime"          : "is_prime",
  "strange-int-prime" : "strange_int_prime",
  "strange-int-depth" : "strange_int_depth",
  "strange-int-delta" : "strange_int_delta",
  "strange-int-list"  : "strange_int_list",
}

# 3/2/2015: NB: all functions in this table are almost certainly vulnerable to injection attacks, cf SQL injection attacks!
# Fix!!! 
# table of compound operators.
# They need to be handled separately from those in the tables above, because they have parameters.
compound_table = {
  "select-elt"         : ".select_elt({0})",
# "find-index"           # can't support these two until we have more advanced parsing.
# "find-value            # eg: find-index[|person: Fred>] |x> currently would split on the space in the ket.
  "normalize"          : ".normalize({0})",
  "rescale"            : ".rescale({0})",
  "similar"            : ".similar(context,\"{0}\")",
# 23/2/2015:
  "self-similar"       : ".self_similar(context,\"{0}\")",
  
  "find-topic"         : ".find_topic(context,\"{0}\")",
# "collapse-function"  : ".apply_fn_collapse({0})",  # broken for now. eg, how handle collapse-fn[spell] |x> ??
  "drop-below"         : ".drop_below({0})",         # Not needed anyway. Just use: collapse spell |x>
  "drop-above"         : ".drop_above({0})",
  "select-range"       : ".select_range({0})",       # may comment this one out, but fine for now to have two versions.
  "select"             : ".select_range({0})",
  "delete-elt"         : ".delete_elt({0})",
  "threshold-filter"   : ".apply_sigmoid(threshold_filter,{0})",
  "not-threshold-filter" : ".apply_sigmoid(not_threshold_filter,{0})",
 
#  "mult"              : ".apply_sigmoid(mult,{0})",  # this is now moved to ket/sp since it is common enough.
  "mult"               : ".multiply({0})",
  "sigmoid-in-range"   : ".apply_sigmoid(sigmoid_in_range,{0})",
  "smooth"             : ".apply_fn_collapse(smooth,{0})",
  "set-to"             : ".apply_sigmoid(set_to,{0})",             

# 4/1/2015:
  "subtraction-invert" : ".apply_sigmoid(subtraction_invert,{0})",

# newly added: 7/4/2014:
  "absolute-noise"     : ".absolute_noise({0})",
  "relative-noise"     : ".relative_noise({0})",
  
# newly added 8/5/2014:
  "common"             : ".apply_sp_fn(common,context,\"{0}\")",   
# newly added 12/5/2014:
  "exp"                : ".apply_sp_fn(exp,context,\"{0}\")",
# newly added 17/4/2015:
  "full-exp"           : ".apply_sp_fn(full_exp,context,\"{0}\")",
  
# newly added 19/5/2014
# rel-kets tweaked 13/2/2015:
  "relevant-kets"      : ".apply_sp_fn(relevant_kets,context,\"{0}\")",
  "intn-relevant-kets" : ".apply_sp_fn(intersection_relevant_kets,context,\"{0}\")",
  "rel-kets"           : ".apply_sp_fn(relevant_kets,context,\"{0}\")",    
  "intn-rel-kets"      : ".apply_sp_fn(intersection_relevant_kets,context,\"{0}\")",    

#  "matrix"            : ".apply_naked_fn(matrix,context,\"{0}\")",
#  "multi-matrix"      : ".apply_naked_fn(multi_matrix,context,\"{0}\")",

# newly added 21/5/2014:
  "matrix"             : ".apply_naked_fn(multi_matrix,context,\"{0}\")",  # this deprecates/replaces the naked_fn(matrix,...) version.
  "merged-matrix"      : ".apply_naked_fn(merged_multi_matrix,context,\"{0}\")",
  "naked-matrix"       : ".apply_naked_fn(merged_naked_matrix,context,\"{0}\")",

# newly added 22/5/2014:
  "map"                : ".apply_sp_fn(map,context,\"{0}\")",

# newly added 28/5/2014:
  "categorize"         : ".apply_naked_fn(categorize,context,\"{0}\")",  
  
# newly added 5/6/2014:
  "vector"             : ".apply_sp_fn(vector,context,\"{0}\")",
# added 6/6/2014:
  "print-pixels"       : ".apply_sp_fn(print_pixels,context,\"{0}\")",
  
# added 27/6/2014:
  "active-buffer"      : ".apply_sp_fn(console_active_buffer,context,\"{0}\")",
  
# added 28/7/2014:
  "train-of-thought"   : ".apply_sp_fn(console_train_of_thought,context,\"{0}\")",
  
# added 4/8/2014:
  "exp-max"            : ".apply_sp_fn(exp_max,context,\"{0}\")",
  
# added 7/8/2014:
  "sp-propagate"       : ".apply_sp_fn(sp_propagate,context,\"{0}\")",
  "op-propagate"       : ".apply_sp_fn(sp_propagate,context,\"{0}\")",  # an alias

# 12/1/2015
  "load-image"         : ".apply_sp_fn(load_image,context,\"{0}\")",
# 20/4/2015
  "save-image"         : ".apply_sp_fn(save_image,context,\"{0}\")",       # why do these need to be apply_sp_fn instead of just apply_fn?

# 29/1/2015:
  "table"              : ".apply_sp_fn(pretty_print_table,context,\"{0}\")",
  
# 1/2/2015:
  "sort-by"            : ".apply_sp_fn(sort_by,context,\"{0}\")",
  
# 2/2/2015:
  "strict-table"       : ".apply_sp_fn(pretty_print_table,context,\"{0}\",True)",
  
# 3/2/2015:
  "sleep"              : ".apply_sp_fn(bko_sleep,\"{0}\")",
  
# 5/2/2015:
  "rank-table"         : ".apply_sp_fn(pretty_print_table,context,\"{0}\",False,True)",
  "strict-rank-table"  : ".apply_sp_fn(pretty_print_table,context,\"{0}\",True,True)",
 
# 25/2/2015:
  "greater-than"       : ".apply_fn(greater_than,{0})",
  "greater-equal-than" : ".apply_fn(greater_equal_than,{0})",
  "less-than"          : ".apply_fn(less_than,{0})",
  "less-equal-than"    : ".apply_fn(less_equal_than,{0})",
  "equal"              : ".apply_fn(equal,{0})",
  "in-range"           : ".apply_fn(in_range,{0})",

  "is-greater-than"       : ".apply_fn(greater_than,{0}).is_not_empty()",
  "is-greater-equal-than" : ".apply_fn(greater_equal_than,{0}).is_not_empty()",
  "is-less-than"          : ".apply_fn(less_than,{0}).is_not_empty()",
  "is-less-equal-than"    : ".apply_fn(less_equal_than,{0}).is_not_empty()",
  "is-equal"              : ".apply_fn(equal,{0}).is_not_empty()",
  "is-in-range"           : ".apply_fn(in_range,{0}).is_not_empty()",

# 12/4/2015:
# not 100% sure this is the best way to do this, but for now is fine.
  "coeff-greater-than"       : ".apply_fn(push_float).apply_fn(greater_than,{0}).apply_fn(pop_float)",
  "coeff-greater-equal-than" : ".apply_fn(push_float).apply_fn(greater_equal_than,{0}).apply_fn(pop_float)",
  "coeff-less-than"          : ".apply_fn(push_float).apply_fn(less_than,{0}).apply_fn(pop_float)",
  "coeff-less-equal-than"    : ".apply_fn(push_float).apply_fn(less_equal_than,{0}).apply_fn(pop_float)",
  "coeff-equal"              : ".apply_fn(push_float).apply_fn(equal,{0}).apply_fn(pop_float)",
  "coeff-in-range"           : ".apply_fn(push_float).apply_fn(in_range,{0}).apply_fn(pop_float)",

  "is-coeff-greater-than"       : ".apply_fn(push_float).apply_fn(greater_than,{0}).is_not_empty()",
  "is-coeff-greater-equal-than" : ".apply_fn(push_float).apply_fn(greater_equal_than,{0}).is_not_empty()",
  "is-coeff-less-than"          : ".apply_fn(push_float).apply_fn(less_than,{0}).is_not_empty()",
  "is-coeff-less-equal-than"    : ".apply_fn(push_float).apply_fn(less_equal_than,{0}).is_not_empty()",
  "is-coeff-equal"              : ".apply_fn(push_float).apply_fn(equal,{0}).is_not_empty()",
  "is-coeff-in-range"           : ".apply_fn(push_float).apply_fn(in_range,{0}).is_not_empty()",

  
# 21/2/2015:
  "round"                 : ".apply_fn(round_numbers,{0})",

# 22/2/2015:
  "such-that"             : ".apply_fn(such_that,context,\"{0}\")",
  
# 24/2/2015:
  "discrim-drop"          : ".discrimination_drop({0})",
  
# 4/3/2015:                 yeah, we are starting to define compound operators now. Though is slightly inelegant in terms of injection attacks!
  "times"                 : ".apply_fn(pop_float).multiply({0}).apply_fn(push_float)",
  
# 12/3/2015: another compound operator: pick[n]
  "pick"                  : ".shuffle().select_range(1,{0})",           

# 24/3/2015:
  "find-unique"         : ".apply_naked_fn(find_unique,context,\"{0}\")",

# 2/6/2015:
  "find-inverse"        : ".apply_naked_fn(find_inverse,context,\"{0}\")",  
  
# 2/4/2015:
  "intn-find-topic"         : ".intn_find_topic(context,\"{0}\")",
  
# 17/4/2015:
  "apply-weights"          : ".apply_sp_fn(apply_weights,\"{0}\")",  

# 4/5/2015:
  "max-filter"             : ".apply_sigmoid(max_filter,{0})",

# 10/5/2015:
  "image-load"             : ".apply_naked_fn(improved_image_load,\"{0}\")",  

# 11/5/2015:
  "image-save"             : ".apply_sp_fn(improved_image_save_show,\"{0}\")",  

# 12/5/2015:
  "average-categorize"     : ".apply_naked_fn(average_categorize,context,\"{0}\")",
  
# 5/8/2015:
  "select-chars"           : ".apply_sp_fn(select_chars,\"{0}\")",   

}


# 7/4/2014: new addition, functions that map sp -> ket/sp
# Pretty sure this breaks the linearity. 
# Ie, the functions here are in general not linear, while most other ops/fns are.
# 30/6/2014: heh. I'd forgotten I had this! 
sp_fn_table = {
  "list-to-words"      : "sp_to_words",
  "read-letters"       : "read_letters",
  "read-words"         : "read_words", 
  "merge-labels"       : "merge_labels",
  "sp-as-list"         : "sp_as_list",

# 6/3/2015:
  "display-algebra"    : "display_algebra",

# 26-4-2015:
  "rank"               : "rank",          

# 19/5/2015:
  "image-show"         : "improved_image_save_show",  

}

# 2/2/2015: new addition functions that map ket -> ket/sp but needs context info.
ket_context_table = {
  "int-coeffs-to-word" : "int_coeffs_to_word",

# 14/4/2015:
#  "list-kets"          : "list_kets",    # deleted. Same funtionality as starts-with, essentially.
  "starts-with"        : "starts_with",
  
# 4/5/2015:
  "show-image"         : "show_image",    
}


def sanitize_op(op):
  if not op[0].isalpha():
    return None
  if all(c in ascii_letters + '0123456789-' for c in op):
    return op
  else:
     return None

def valid_op(op):
  if not op[0].isalpha() and not op[0] == '!':
    return False
  return all(c in ascii_letters + '0123456789-+!?.' for c in op)



def process_single_op(op):
  logger.debug("op: " + str(op)) 

  if type(op) is list:                                    # compound op found:
    logger.debug("compound op found")
    the_op = op[0]
    parameters = ",".join(op[1:])                         # not 100% sure this is the best way to handle parameters. eg, maybe we should pass a list? 
    if the_op not in compound_table:
      logger.debug(the_op + " not in compound_table")
      python_code = ""
    else:
      python_code = compound_table[the_op].format(parameters)   # probably risk of injection attack here

  elif op in built_in_table:                # tables don't have injection bugs, since they must be in tables, hence already vetted.
    logger.debug("op in built in table")           # unless I guess a hash-table collision between safe and unsafe?
    python_code = ".{0}()".format(built_in_table[op])
  elif op in sigmoid_table:
    logger.debug("op in sigmoid table")
    python_code = ".apply_sigmoid({0})".format(sigmoid_table[op])
  elif op in fn_table:                                    # I'm a little uncertain aboud the distinction between
    logger.debug("op in fn table")                               # fn_table vs fn_table2
    python_code = ".apply_fn({0})".format(fn_table[op])
  elif op in fn_table2:
    logger.debug("op in fn table 2")
    python_code = ".apply_fn({0})".format(fn_table2[op])
  elif op in sp_fn_table:
    logger.debug("op in sp fn table")
    python_code = ".apply_sp_fn({0})".format(sp_fn_table[op])    
  elif op in ket_context_table:
    logger.debug("op in ket context table")
    python_code = ".apply_fn({0},context)".format(ket_context_table[op])
  else:
    if op == "\"\"":
      python_code = ".apply_op(context,\"\")"
    elif op == "ops":                     # short-cut so we don't have to type supported-ops all the damn time!
      python_code = ".apply_op(context,\"supported-ops\")"
    elif not valid_op(op):
#      return ""
# add code so that op2 7 op1 |x> is the same as op2 mult[7] op1 |x>
      try:
        value = float(op)
        python_code = ".multiply({0})".format(op)
      except:
        if op == '-':       # treat - |x> as mult[-1] |x>
          python_code = ".multiply(-1)"
        else:
          return ""
    else:
      logger.debug("op is literal")               # NB: we have to be very careful here, or it will cause SQL-injection type bugs!!
      python_code = ".apply_op(context,\"{0}\")".format(op)  # fix is not hard. Process the passed in op to a valid op form.
  logger.debug("py: " + python_code)                                   # lower+upper+dash+number and thats roughly it.
  return python_code


# operator parse:
our_operator_grammar = """
S0 = ' '*
S1 = ' '+

digit = :x ?(x in '0123456789') -> x
positive_int = <digit+>:n -> int(n)

# what about handle more than one dot char??
# fix eventually, but not super important for now
# what about minus sign?
simple_float = ('-' | -> ''):sign <(digit | '.')+>:n -> float_int(sign + n)

op_start_char = anything:x ?(x.isalpha() or x == '!') -> x
# allow dot as an op char??
op_char = anything:x ?(x.isalpha() or x.isdigit() or x in '-+!?.') -> x
literal_op = op_start_char:first <op_char*>:rest -> first + rest

parameters = (simple_float | literal_op | '\"\"')
compound_op = literal_op:the_op '[' parameters:first (',' parameters)*:rest ']' -> [the_op] + [first] + rest

general_op = (compound_op | literal_op | simple_float | '\"\"' | '-'):the_op -> the_op

powered_op = general_op:the_op '^' positive_int:power -> (the_op,power)

op = (powered_op | general_op):the_op -> the_op

op_sequence = (S0 op:first (S1 op)*:rest S0 -> [first] + rest)
              | S0 -> []
"""

# what happens if we have eg: "3.73.222751" (ie, more than one dot?)
def float_int(x):
  if float(x).is_integer():
    return str(int(x))
  return x

op_grammar = makeGrammar(our_operator_grammar,{"float_int" : float_int})

def process(context,ops,x):
  logger.debug("ops: " + ops)
  logger.debug("x: " + str(x))
  try:
    parsed_operators = op_grammar(ops).op_sequence()
  except:
    return None
  logger.debug("parsed_ops: " + str(parsed_operators))
  code = "x"
  for op in reversed(parsed_operators):
    if type(op) is tuple:                     # powered-op found.
      the_op,power = op                       # unpack tuple.       
      logger.debug("powered-op power: " + str(power))
      tmp = process_single_op(the_op)
      for k in range(power):
        code += tmp
    else:
      code += process_single_op(op)
  if code == "x":
    return None
  logger.debug("python: " + code)      
  return eval(code)



# 17/2/2014:

def extract_leading_ket(s):
  try:
    head, rest = s.split("|",1)
    head = head.strip()        
  
    if len(head) == 0:
      value = 1
    else:
      value = float(head)  

    label, rest = rest.split(">",1)   
    return ket(label,value), rest
  except:
    return s

def extract_leading_bra(s):
  if s[0] != "<":
    return s
  try:
    label, rest = s[1:].split("|",1)
    return bra(label), rest
  except:
    return s



def old_old_extract_literal_superposition(s):
  rest = s
  result = superposition()

  try:
    x, rest = extract_leading_ket(rest)
    result.data.append(x)
  except:
    return result, rest

  while True:
    try:
      null, rest = rest.split("+",1)
      x, rest = extract_leading_ket(rest)
      result.data.append(x)
    except:
      return result, rest

def old_extract_literal_superposition(s):
  rest = s
  result = superposition()

  while True:
    try:
      x, rest = extract_leading_ket(rest)
      result.data.append(x)
      saved = rest
      null, rest = rest.split("+",1)
      print("els saved:",saved)
      print("els null:",null)
      print("null len:",len(null.strip()))
      print("els result:",result)

      if len(null.strip()) != 0:
        print("els null not zero")
        return result, saved

    except:
      print("els final result:",result)
      return result, rest


def extract_literal_superposition(s,self_object=None):
  rest = s
  saved = rest
  result = superposition()

  while True:
    try:
      x, rest = extract_leading_ket(rest)
      if x.label == "_self":
        x.label = self_object                  # assumes of course that self_object is a string.
      result.data.append(x)
    except:
      return result, saved

    try:
      saved = rest
      null, rest = rest.split("+",1)
#      print("els saved:",saved)
#      print("els null:",null)
#      print("null len:",len(null.strip()))
#      print("els result:",result)

      if len(null.strip()) != 0:
        print("els null not zero")
        return result, saved

    except:
      print("els final result:",result)
      return result, rest

# 7/1/2015
# This might help speed up Kevin Bacon numbers.
# Anyway, useful.
# Note a clean superposition is one that has all coeff 1 and implicit.
# |a> + |b> + |c> is a clean superposition.
# 3|a> + 1|b> + |c> is not.
# NB: it does not sub in values for |_self>
# NB: it breaks badly if the superposition is not clean!
def extract_clean_superposition(line):
  line = line.rstrip()          # in case there is white-space at the end of the line.
  r = superposition()           # assumes there is never any white-space at the start of the line!
  for x in line[1:-1].split("> + |"):
    r.data.append(ket(x))
  return r  

def old_parse_rule_line(C,s):
  if s.strip().startswith("--"):
    return False
  try:
    op, rest = s.split("|",1)
    op = op.strip()
    label, rest = rest.split(">",1)
  except:
    return False

  if op.startswith("--") or op == "supported-ops":
    return False

# handle stored_rules:
  try:
    null, rest = rest.split("#=>",1)
    rest = rest.strip()
    print("FYI: just learnt this stored rest:" + rest + ":")
    rule = stored_rule(rest)
#    print("FYI: stored rule worked ...")
    C.learn(op,label,rule)
#    print("FYI: just learnt this stored rule:",rule)
    return True
  except Exception as e:
#    print("FYI: exception for stored rule")
#    print("reason:",e)
    pass

  add_learn = False
  try:
    null, rest = rest.split("+=>",1)
    add_learn = True
  except:
    try:
      null, rest = rest.split("=>",1)
    except:
      return False

  try:  # maybe tweak to handle: O|tmp> => op2 op1 |_self>
    rule, null = extract_compound_superposition(C,rest,label)
  except:
    return False

  print("op:",op)
  print("label:",label)
  print("rest:",rest.rstrip())
  print("rule:",rule,"\n")

  if op == "" and label == "context":
    if len(rule.data) > 0:
      name = rule.data[0].label
      if name.startswith("context: "):
        name = name[9:]
      C.set(name)
    return True

  if not add_learn:
    C.learn(op,label,rule)
  else:
    C.add_learn(op,label,rule)
  return True

# 28/7/2014: let's improve parse_rule so that we can learn rules indirectly.
# eg: 
# |you> => |Fred>
# age "" |you> => |24>
# another eg:
# |list> => |Sam> + |Mary> + |Liz>
# age "" |list> => |19>  -- they are all 19 years old.
# and a more interesting one:
# op-self "" |list> => 13 |_self>  -- ie, we need to run ECS for everyone in "" |list>
#
# This function is currently broken!
# age friends (|Fred> + |Sam>) => |age: 20>
# age-self friends split |Fred Sam> => 20 |_self>
# age |person: Fred> => |22>
# All work. Good.
# But:
# |person: Harry> => |bah>
# age|person: Harry> => |bah>
# are broken.
# With this debug info:
# head: |person: Harry>
# tail: |bah>
# op 1: |person:             -- this is the problem. It splits on space inside the ket!
# indirect_label 1: Harry>
#
# 29/7/2014: I think it is fixed!
# Using this:
#  P  S  action
# -1 -1  False
#  0 -1  P
# -1  0  S
#  0  0  min(P,S)
#
def parse_rule_line(C,s):
  if s.strip().startswith("--"):          # filter out comment lines.
    return False

  try:
    head,tail = s.split("=>",1)           # split the rule line into text before the rule symbol "=>", and after.
    rule_type = head[-1]
    if rule_type in ['#','+','!']:        # cases to handle:
      head = head[:-1]                    # op |x>#=> ...   (yeah, normally a space to separate ket from rule symbol, but valid with no space too!)
    else:                                 # op |x>+=> ...
      rule_type = ' '                     # op |x>=> ...
    head = head.strip()                   # op |x> !=> ... (memoizing rules, new as of 15/2/2015)
    tail = tail.strip()                   
  except:                                 
    return False

  print("head:",head)
  print("tail:",tail)
  
  pipe_min = head.find("|")
  space_min = head.find(" ")
  print("pipe_min: ",pipe_min)
  print("space_min:",space_min)
  
  if pipe_min < 0 and space_min < 0:         # filter out lines that don't have pipe or space char
    return False
  if (pipe_min >= 0 and space_min < 0) or (pipe_min >= 0 and space_min >=0 and pipe_min < space_min):
    op, rest = head.split("|",1)
    indirect_label = "|" + rest
  else:
    op, indirect_label = head.split(" ",1)

  print("op 1:",op)
  print("indirect_label 1:",indirect_label)

  if op == "supported-ops":               # we don't bother learning supported-ops rules. They are auto-generated by learn(). 
    return False

  indirect_label, null = extract_compound_superposition(C,indirect_label)     # I think this is the appropriate way to call ECS().      

  print("op 2:",op)
  print("indirect_label 2:",indirect_label)

  if rule_type == "#":                    # handle stored rules separately, as they are slightly different from the other two.
    print("inside parse_rule_line stored_rule")
    rule = stored_rule(tail)
    for label in indirect_label:          # presumably extract_compound_superposition() always returns a sp.
      C.learn(op,label,rule)                   # look into converting sp's into iterable objects. New python to learn!
    return True

  if rule_type == "!":                    # handle stored rules separately, as they are slightly different from the other two.
    print("inside parse_rule_line memoizing_rule")
    rule = memoizing_rule(tail)
    for label in indirect_label:
      C.learn(op,label,rule)    
    return True

  add_learn = False
  if rule_type == '+':
    add_learn = True

  try:
    for label in indirect_label.data:                                 # NB: indirect_label is a superposition
      print("parse_rule_line learn label:",label)
      rule, null = extract_compound_superposition(C,tail,label.label) # the last parameter needs to be string, not a ket.
      print("parse_rule_line learn rule:",rule)
      if op == "" and label.label == "context":                       # handle context in a special way!
        if len(rule.data) > 0:
          name = rule.data[0].label
          if name.startswith("context: "):
            name = name[9:]
          C.set(name)
      else:
        C.learn(op,label,rule,add_learn)
    return True
  except:
    return False    



# Now, make use of parse_rule_line()
# load sw file:
def load_sw(c,file):
  try:
    with open(file,'r') as f:
      for line in f:
        if line.startswith("exit sw"):      # use "exit sw" as the code to stop processing a .sw file.
          return
        parse_rule_line(c,line)             # this is broken! bug found when loading fragment-document.sw fragments
  except:
    print("failed to load:",file)

# and its brother:
# save current context:
def save_sw(c,name,exact_dump=True):
  try:
    file = open(name,'w')
    file.write(c.dump_universe(exact_dump))
    file.close()
  except:
    print("failed to save:",name)

# save multiverse:
def save_sw_multi(c,name):
  try:
    file = open(name,'w')
    file.write(c.dump_multiverse(True))
    file.close()  
  except:
    print("failed to save:",name)

# copied from here:
# http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
def human_readable_size(num):
  for x in ['B ','KB','MB','GB','TB']:
    if num < 1024.0:
      if x == 'B ':
        return "%3.0f %s" % (num,x)
      else:        
        return "%3.1f %s" % (num,x)
    num /= 1024.0

def broken_human_readable_size(num):         # Doh. Gets some answers wrong.
  for x in ['B ','KB','MB','GB','TB']:       # because "%3.0f" rounds up, and this method does not.
    if num < 1024:
      return "%3.0d %s" % (num,x)
    num //= 1024

import time
# find the stats of a .sw file:
# needs some tweaks yet ...
# works fine, though is hinting at getting slow for large sw files.
def extract_sw_stats(file):
  try:
    stats = []
    context = ""
    count = 0
    with open(file,'r') as f:
      for line in f:
        if line.startswith("supported-ops |"):
          count += 1
        elif line.startswith("|context> => |"):
          tmp_context = line[14:].split(">")[0]
          if tmp_context.startswith("context: "):
            tmp_context = tmp_context[9:]
          if len(tmp_context) > 0:                                                        
            if len(context) > 0 or count > 0:
              stats.append(context + " (" + str(count) + ")")
            context = tmp_context
            count = 0
    if len(context) > 0 or count > 0:
      stats.append(context + " (" + str(count) + ")")

# now find file size:
    size = human_readable_size(os.path.getsize(file))
    
# now find file date:
    date = time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(file)))
    return date + "   " + size + "   " + ", ".join(stats)
        
  except:
    print("failed to load:",file)    
    return ""


# we need code to handle the input in the semantic-agent console:
# we have three cases to handle:
# op3 op2 op1                     # use x as the implicit ket   # currently handled by process(c,line,x)
# op-b op-a |x>                   # specifiy |x>                # currently not handled
# op |x> => 3|a> + |b>            # learn rule                  # currenlty handled by parse_rule_line(C,line).
def old_process_input_line(C,line,x):
  if not parse_rule_line(C,line):
    try:
      op, rest = line.split("|",1)
    except:
      return process(C,line,x)
    try:
      op = op.strip()
      label, rest = rest.split(">",1)
      return process(C,op,ket(label))
    except:
      return 
  return 

def process_input_line(C,line,x):
  if not parse_rule_line(C,line):
    try:
      result, null = extract_compound_superposition(C,line)
      return result
    except:
      return process(C,line,x)
  

def process_op_ket(C,line,left_label=None):
  try:
    op, rest = line.split("|",1)
    op = op.strip()
    label, rest = rest.split(">",1)
    if label == "_self" and left_label is not None:
      label = left_label
    return process(C,op,ket(label)), rest
  except:
    return None

# eg: intersection(op|X>,op|Y>)
def old_process_function(C,line):
  try:
    fn, rest = line.split("(",1)
    fn = fn.strip()
    print("fn:",fn)
    sp1, rest = process_op_ket(C,rest)  # sp is short for superposition
    print("sp1:",sp1)
    null, rest = rest.split(",",1)
    sp2, rest = process_op_ket(C,rest)
    print("sp2:",sp2)
    null, rest = rest.split(")",1)
    print("rest:",rest)
  except:
    return None
#  return intersection(sp1,sp2)
  code = "{0}(sp1,sp2)".format(fn)        # this is seriously dangerous for injection attacks, ATM.
  print("python:",code)
  return eval(code)



# dummy len 1 fn:
def sp_len_1(x):
  return ket("sp") + x

# white listed functions that take 1 parameter:
whitelist_table_1 = {
#  "dump"          : "C.dump_sp_rules",        # buggy since, it returns a string! Not a ket/sp.
  "sp"             : "sp_len_1",
#  "to-number"      : "category_number_to_number",  # I think this is better in the ket->ket section.
#  "discrimination" : "discrimination",              # probably ditto.
#  "discrim"        : "discrimination",              # nah. That way leads to bugs. Belongs here.
                                                     # Heh. Added it to ket/sp classes. It belongs there now.
#  "read-letters"    : "read_letters",               # try this in sp_fn_table above.
#  "read-words"      : "read_words",                 # yup. This one too. This table is almost always the wrong place for functions!
}

# whitelisted functions, that take 2 parameters:
whitelist_table_2 = {
  "intersection"        : "intersection",
  "intn"                : "intersection",
  "common"              : "intersection",          # this is for those that haven't studied maths.
  "union"               : "union",                 # though if they haven't this work won't make much sense anyway!
  "mult"                : "multiply",
  "multiply"            : "multiply",              # for when you are not lazy :)
  "addition"            : "addition",
  "simm"                : "simm",
  "silent-simm"         : "silent_simm",
  "weighted-simm"       : "weighted_simm",          # hrmm... I thought this took 3 parameters, not 2!
  "nfc"                 : "normed_frequency_class",  # pretty unlikely this will be used at command line since needs freq lists.
  "ket-nfc"             : "ket_normed_frequency_class",
#  "apply"               : "apply",                  # 10/11/2014: What is this function?? Commented out!
  "range"               : "show_range",
  "ket-simm"            : "ket_simm",
  "to-base"             : "decimal_to_base",
  "general-to-specific" : "general_to_specific",
  
# 4/1/2015:
  "equal"               : "test_equal",
  
# 22/2/2015:
  "ED"                  : "Euclidean_distance",
  
# 26/2/2015:
  "mbr"                 : "mbr",
  "measure"             : "mbr",
  
# 9/4/2015:
  "subset"              : "subset",
  
# 11/8/2015:
  "exclude"             : "exclude",      
}

# whitelisted functions that take 3 parameters:
whitelist_table_3 = {
  "intersection"  : "tri_intersection",
  "intn"          : "tri_intersection",
  "common"        : "tri_intersection",
  "union"         : "tri_union",
  "arithmetic"    : "arithmetic",
  "range"         : "show_range",
  "algebra"       : "algebra",
  "if"            : "bko_if",
  "wif"           : "weighted_bko_if",
  "wsimm"         : "weighted_simm",
  "ket-wsimm"     : "ket_weighted_simm",
  "non-Abelian-algebra" : "non_Abelian_algebra",         # 2/2/2015, finally wire this one in!
}

# the code needed for this not yet implemented.
# whitelisted functions that take 4 parameters:
whitelist_table_4 = {
  "algebra"       : "algebra",
}

# new: 10/11/2014:
# whitelisted functions that need context variable, and takes 2 extra parameters:
# eg: apply(context,sp1,sp2)
context_whitelist_table_2 = {
  "apply-sp" : "apply_sp",
  "apply"    : "apply_sp",

# 17/1/2015:
  "clone"    : "clone_ket",  
}


def old_process_brackets(C,line,left_label=None):
  print("inside process_brackets:",line)
  try:
    fn, rest = line.split("(",1)
    fn = fn.strip()
    pieces = []
    while True:
      try:
        sp, rest = extract_compound_superposition(C,rest,left_label)     # sp is short for superposition
        pieces.append(sp)
        print("inside while, rest:",rest)
        null, rest = rest.split(",",1)
      except:
        break
    if len(pieces) == 0:
      return None
    null, rest = rest.split(")",1)
  except:
    return None

  print("fn:  ",fn)
  print("len: ",len(pieces))
  for sp in pieces:
    print("sp: ",sp)
  print("rest:",rest)  

# what if len(fn) == 0?

  if len(pieces) == 1:
    if fn in whitelist_table_1:
      print("op in whitelist 1")
      code = whitelist_table_1[fn] + "(pieces[0])"
      print("py:",code)
      result = eval(code)
      return result, rest
    elif len(fn) == 0:
      return pieces[0], rest
    else:
      return process(C,fn,pieces[0]), rest

  if len(pieces) == 2: 
    tmp = fn.split()
    main_fn = tmp[-1]
    rest_fn = " ".join(tmp[:-1])

    if main_fn in whitelist_table_2:
      print("op in whitelist 2")
      code = whitelist_table_2[main_fn] + "(pieces[0],pieces[1])"
      print("py:",code)
      result = eval(code)
      if type(result) != ket and type(result) != superposition:
        print("result not ket/sp")
        if type(result) == float or type(result) == int:
          try:
            x, rest = extract_leading_ket(rest)
            result = ket(x.label,result)
          except:
            return result, rest
        else:
          return None

      if len(rest_fn) == 0:
        return result, rest
      else:
        print("rest_fn:",rest_fn)
        print("result:",result)
        return process(C,rest_fn,result), rest   # this raises an exception if result is not ket/sp.

  if len(pieces) == 3:
    tmp = fn.split()
    main_fn = tmp[-1]
    rest_fn = " ".join(tmp[:-1])

    if main_fn in whitelist_table_3:
      print("op in whitelist 3")
      code = whitelist_table_3[main_fn] + "(pieces[0],pieces[1],pieces[2])"
      print("py:",code)
      result = eval(code)
      print("result:",result)
     
  return None

def process_brackets(C,line,left_label=None):
  print("inside process_brackets:",line)
  try:
    fn, rest = line.split("(",1)
    fn = fn.strip()
    pieces = []
    while True:
      try:
        sp, rest = extract_compound_superposition(C,rest,left_label)     # sp is short for superposition
        pieces.append(sp)
        print("inside while, rest:",rest)
        null, rest = rest.split(",",1)
      except:
        break
    if len(pieces) == 0:
      return None
    null, rest = rest.split(")",1)
  except:
    return None

  print("fn:  ",fn)
  print("len: ",len(pieces))
  for sp in pieces:
    print("sp: ",sp)
  print("rest:",rest)  

# what if len(fn) == 0?

  if len(pieces) == 1:
    if fn in whitelist_table_1:
      print("op in whitelist 1")
      code = whitelist_table_1[fn] + "(pieces[0])"
      print("py:",code)
      result = eval(code)
      return result, rest
    elif len(fn) == 0:
      return pieces[0], rest
    else:
      return process(C,fn,pieces[0]), rest

  tmp = fn.split()
  main_fn = tmp[-1]
  rest_fn = " ".join(tmp[:-1])

  match = False                                     # I have been intending to merge the len 2 and len 3 
  if len(pieces) == 2:                              # into the one block of code. No hurry.
    if main_fn in whitelist_table_2:
      match = True
      print("op in whitelist 2")
      code = whitelist_table_2[main_fn] + "(pieces[0],pieces[1])"
    elif main_fn in context_whitelist_table_2:
      match = True
      print("op in context whitelist 2")
      code = context_whitelist_table_2[main_fn] + "(C,pieces[0],pieces[1])"
  if len(pieces) == 3:
    if main_fn in whitelist_table_3:
      match = True
      print("op in whitelist 3")
      code = whitelist_table_3[main_fn] + "(pieces[0],pieces[1],pieces[2])"

  if match:
    print("py:",code)
    result = eval(code)

  if not match:
    result = ket("",0)

# not sure I want to keep this code block.
# maybe simm should return v|simm> instead of just a float. Now implemented this as ket_simm().
# well, a variant of simm that does that. Recall some code needs it as a float.
  if type(result) != ket and type(result) != superposition:
    print("result not ket/sp")
    if type(result) == float or type(result) == int:
      try:
        x, rest = extract_leading_ket(rest)        # may want something more elaborate here too.
        result = ket(x.label, x.value * result)
      except:
        return result, rest
    else:
      return None

  if len(rest_fn) == 0:
    return result, rest
  else:
    print("rest_fn:",rest_fn)
    print("result:",result)
    return process(C,rest_fn,result), rest   # this raises an exception if result is not ket/sp.

     
  return None


# this function is going to end up doing a lot of heavy lifting!
def old_extract_compound_superposition(C,s):
  rule, rest = extract_literal_superposition(s)   # first try for a literal superposition
  if len(rule.data) == 0:                         # try for: op2 op1 |x>
    try:
      rule, rest = process_op_ket(C,s)
    except:
      return None

  return rule, rest

def previous_extract_compound_superposition(C,s):
  rule, rest = extract_literal_superposition(s)
  if len(rule.data) == 0:
    try:
      rule, rest = process_brackets(C,s)
    except:
      try:
        rule, rest = process_op_ket(C,s)
      except:
        return None
  return rule, rest

# I forget! Can self_object be a string, ket and sp? 
# I know it can be a ket, but the other two cases??
# doh! Only seems to work with string at the moment.
# I think I want all three cases eventually .... 
def extract_compound_superposition(C,s,self_object=None):
  rest = s
  result = superposition()

  while True:
    try:
      rule, rest = extract_literal_superposition(rest,self_object)
      if len(rule.data) == 0:
        try:
          rule, rest = process_brackets(C,rest,self_object)
        except:
          try:
            rule, rest = process_op_ket(C,rest,self_object)
          except:
            return None
      result += rule

      saved = rest
      null, rest = rest.split("+",1)
      if len(null.strip()) != 0:
        print("ecs saved:",saved)
        return result, saved
    except:
      return result, rest


