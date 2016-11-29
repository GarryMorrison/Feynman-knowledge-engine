
#######################################################################
# the semantic-db parser
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2014
# Update: 23/11/2016
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
  "softmax"          : "softmax",      # added 15/12/2015
  
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
# 26/3/2016:
  "drop-zero"        : "drop_zero",
  
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
  
# 27/8/2015: a couple of sigmoid aliases:
  "BF"                 : "binary_filter",
  "XF"                 : "xor_filter",

# 15/12/2015:
  "log"                : "log",              # log(x)
  
# 17/5/2016:
  "log+1"              : "log_1",            # log(1 + x)
  
  
# 14/1/2016:
  "square"             : "square",           # for now these two are sigmoids. Maybe wan't to change that later?
  "sqrt"               : "sqrt",    

# 12/9/2016:
  "floor"              : "floor",
  "ceiling"            : "ceiling",
}                                   

# some ket -> ket functions:
fn_table = {
  "apply-value"      : "apply_value",
  "extract-category" : "extract_category",
  "extract-value"    : "extract_value",

# 28/8/2015:
  "remove-leading-category" : "remove_leading_category",
  "find-leading-category"   : "find_leading_category",
  

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
# 29/8/2015:
  "clean-split"      : "clean_split_ket",                                                  
                                                  
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
  "to-coeff"           : "to_coeff",
# 12/10/2015: an alias:
  "clean-ket-label"    : "to_coeff",
  

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

# 19/6/2016:
  "hash-compress"      : "hash_compress",
  
# 12/9/2016:
  "words-to-list"      : "words_to_sp",  
}


# 7/4/2014 me wonders. do fn_table and fn_table2 really need to be separate?  
# some other functions. Some are ket -> ket, some are ket -> superposition.
fn_table2 = {
  "read"              : "read_text",
#  "spell"             : "spell_word",                          # removed 16/9/2016. We have a new spell that uses high order sequences
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
  
# 18/1/2016:
  "similar-input"      : ".similar_input(context,\"{0}\")",  
  
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
# newly added 24/9/2015:
  "union"              : ".apply_sp_fn(operator_union,context,\"{0}\")",

# newly added 10/5/2016:
  "simm-add"           : ".apply_sp_fn(simm_add,context,\"{0}\")",

     
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
#  "such-that"             : ".apply_fn(such_that,context,\"{0}\")",
# 28/4/2016: changed from ket -> ket to sp -> sp, hopefully better big-O
  "such-that"             : ".apply_sp_fn(sp_such_that,context,\"{0}\")",
  
# 24/2/2015:
  "discrim-drop"          : ".discrimination_drop({0})",
  
# 4/3/2015:                 yeah, we are starting to define compound operators now. Though is slightly inelegant in terms of injection attacks!
#  "times"                 : ".apply_fn(pop_float).multiply({0}).apply_fn(push_float)",
  
# 14/1/2016:
#  "times-by"              : ".apply_fn(pop_float).multiply({0}).apply_fn(push_float)",    # OK. These sort of work, but not perfect. I think I will change how they are implemented.  
#  "divide-by"             : ".apply_fn(pop_float).multiply(1/{0}).apply_fn(push_float)",  # eg: plus[3] 2|number: 7> returns |number: 17>
#  "plus"                  : ".apply_fn(pop_float).add({0}).apply_fn(push_float)",         # I think we would prefer 2|number: 10> 
#  "minus"                 : ".apply_fn(pop_float).add(-{0}).apply_fn(push_float)",
#  "add"                   : ".apply_fn(pop_float).add({0}).apply_fn(push_float)",
#  "take"                  : ".apply_fn(pop_float).add(-{0}).apply_fn(push_float)",

# 14/1/2016: new and improved. These have better properties, and avoid the pop-float, push-float mess.
  "times"                 : ".apply_fn(times_numbers,{0})",
  "times-by"              : ".apply_fn(times_numbers,{0})",
  "divide-by"             : ".apply_fn(times_numbers,1/{0})",
  "plus"                  : ".apply_fn(plus_numbers,{0})",
  "minus"                 : ".apply_fn(plus_numbers,-{0})",
  "add"                   : ".apply_fn(plus_numbers,{0})",
  "take"                  : ".apply_fn(plus_numbers,-{0})",
# 21/1/2016:
  "mod"                   : ".apply_fn(mod_numbers,{0})",
  "is-mod"                : ".apply_fn(is_mod_numbers,{0})",
  
  
# 12/3/2015: another compound operator: pick[n]
  "pick"                  : ".shuffle().select_range(1,{0})",
  
# 24/9/2015:
  "top"                   : ".top({0})",
# 13/10/2015:
  "inhibition"            : ".inhibition({0})",               

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
#  "image-load"             : ".apply_naked_fn(improved_image_load,\"{0}\")",  
# 2/3/2016:
  "image-load"             : ".apply_naked_fn(new_image_load,\"{0}\")",
# 3/3/2016:
  "image-histogram"        : ".apply_naked_fn(image_histogram,\"{0}\")",
# 4/3/2016:
  "image-save"             : ".apply_fn(new_image_save,\"{0}\")",
  
  

# 11/5/2015:
#  "image-save"             : ".apply_sp_fn(improved_image_save_show,\"{0}\")",  

# 12/5/2015:
  "average-categorize"     : ".apply_naked_fn(average_categorize,context,\"{0}\")",
  
# 5/5/2016:
#  "average-categorize-suppress" : ".apply_naked_fn(average_categorize_suppress,context,\"{0}\")",
# 6/5/2016:
  "average-categorize-suppress" : ".apply_naked_fn(list_average_categorize_suppress,context,\"{0}\")",

  
# 5/8/2015:
  "select-chars"           : ".apply_fn(select_chars,\"{0}\")",

# 24/8/2015:
  "ket-hash"               : ".apply_fn(ket_hash,\"{0}\")",
  "hash-data"              : ".apply_sp_fn(hash_data,\"{0}\")",     

# 25/8/2015: a couple of aliases
  "hash"                   : ".apply_fn(ket_hash,\"{0}\")",
  "sp-to-dat"              : ".apply_sp_fn(hash_data,\"{0}\")",
  
# 26/11/2015:
  "letter-ngrams"          : ".apply_fn(make_ngrams,\"{0}\",\"letter\")",       
  "word-ngrams"            : ".apply_fn(make_ngrams,\"{0}\",\"word\")",
  
# 15/12/2015:
  "log"                    : ".apply_sigmoid(log,{0})",
# 17/5/2016:
  "log+1"                  : ".apply_sigmoid(log_1,{0})",
  
  
# 17/12/2015:
  "delete"                 : ".apply_fn(edit_delete,\"{0}\")",
  "insert"                 : ".apply_fn(edit_insert,\"{0}\")",    
  "substitute"             : ".apply_fn(edit_substitute,\"{0}\")",
  
# 9/2/2016:
  "guess-ket"              : ".apply_fn(guess_ket,context,\"{0}\")",
  "guess-operator"         : ".apply_naked_fn(guess_operator,context,\"{0}\")",
  
# 20/3/2016:
  "path-op"                : ".apply_fn(path_op,context,\"{0}\")",
  
# 15/5/2016:
  "learn-ket-norms"        : ".apply_naked_fn(learn_ket_normalizations,context,\"{0}\")",     

# 28/6/2016:
  "append-column"          : ".apply_fn(append_column,\"{0}\")",
  "random-column"          : ".apply_fn(random_column,\"{0}\")",
  
# 28/7/2016:
#  "have-in-common"         : ".apply_sp_fn(have_in_common,context)",   # have-in-common has no parameters, so wont work here!  

# 12/9/2016:
  "bar-chart"              : ".apply_sp_fn(bar_chart,\"{0}\")",
# 29/9/2016:
  "sbar-chart"              : ".apply_sp_fn(bar_chart,\"{0}\",True)",
    
  
# 26/9/2016:
  "print-sequence"         : ".apply_fn(print_sequence,context,\"{0}\")",
  
# 31/10/2016:
  "new-print-sequence"     : ".apply_fn(new_print_sequence,context,\"{0}\")",
  
# 17/11/2016:
  "follow-sequence"         : ".apply_sp_fn(follow_sequence,context,\"{0}\")",  
    
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
  
# 9/2/2016:
  "guess-ket"          : "guess_ket",
  
# 15/9/2016:
  "recall-sequence"    : "recall_sequence",
  "recall-chunked-sequence"    : "recall_chunked_sequence",
  
# 16/9/2016:
  "spell"              : "spell",
  
# 25/9/2016:
  "print-sequence"     : "print_sequence",
  
# 31/10/2016:
  "new-print-sequence" : "new_print_sequence",
  
  
# 5/10/2016:
#  "follow-sequence"    : "follow_sequence",            # nope! wrong spot!             
}

# 28/7/2016: new addition, functions that map sp -> sp but needs context info.
# I tried putting it in the compound op table, but that failed since it has no parameters.
#
sp_context_table = {
#28/7/2016:
  "have-in-common"    : "have_in_common",
  
# 5/10/2016:
  "follow-sequence"    : "follow_sequence",

# 20/11/2016:
  "recall-sentence"    : "recall_sentence",
  
# 23/11/2016:
  "recall-sentence-v2"    : "recall_sentence_v2",
                 
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


# operator parse:
our_operator_grammar = """
S0 = ' '*
S1 = ' '+

digit = :x ?(x in '0123456789') -> x
positive_int = <digit+>:n -> int(n)

# what about handle more than one dot char??
# fix eventually, but not super important for now
# what about minus sign?
#simple_float = ('-' | -> ''):sign <(digit | '.')+>:n -> float_int(sign + n)
# handle 9.3/5.2
simple_float = ('-' | -> ''):sign <(digit | '.')+>:numerator ('/' <(digit | '.')+> | -> '1'):denominator -> float_int(sign + numerator,denominator)


op_start_char = anything:x ?(x.isalpha() or x == '!') -> x
# allow dot as an op char??
op_char = anything:x ?(x.isalpha() or x.isdigit() or x in '-+!?.') -> x
simple_op = op_start_char:first <op_char*>:rest -> first + rest
parameters = (simple_float | simple_op | '\"\"' | '*'):p -> str(p)

# more elegant, process at the end version:
compound_op = simple_op:the_op '[' parameters:first (',' parameters)*:rest ']' -> [the_op] + [first] + rest
general_op = (compound_op | simple_op | simple_float | '\"\"' | '-'):the_op -> the_op
powered_op = general_op:the_op '^' positive_int:power -> (the_op,power)

# process as you go version:
# I eventually decided this version was too ugly! 
#compound_op = simple_op:the_op '[' parameters:first (',' parameters)*:rest ']' -> process_compound_op(the_op,[first] + rest)
#general_op = (compound_op | simple_op | simple_float | '\"\"' | '-'):the_op -> process_single_op(the_op)
#powered_op = general_op:the_op '^' positive_int:power -> process_power_op(the_op,power)

op = (powered_op | general_op):the_op -> the_op
op_sequence = (S0 op:first (S1 op)*:rest S0 -> [first] + rest)
              | S0 -> []

add_sequence = S0 '+' S0 op_sequence:k -> ('+',k)
sub_sequence = S0 '-' S0 op_sequence:k -> ('-',k)
sequence_ops = (add_sequence | sub_sequence)
bracket_ops = S0 '(' op_sequence:first S0 (sequence_ops+:rest S0 ')' S0 -> [('+',first)] + rest
                                          | ')' S0 -> [('+',first)] )

valid_ket_chars = anything:x ?(x not in '<|>') -> x
naked_ket = '|' <valid_ket_chars*>:x '>' -> x
coeff_ket = (number | -> 1):value S0 naked_ket:label -> ket(label,value)

add_ket = S0 '+' S0 coeff_ket:k -> ('+', k)
sub_ket = S0 '-' S0 coeff_ket:k -> ('-', k)
merge_ket = S0 '_' S0 coeff_ket:k -> ('_', k)
#sequence_ket = S0 '.' S0 coeff_ket:k -> ('.', k)

ket_ops = (add_ket | sub_ket | merge_ket | sequence_ket)
literal_superposition = S0 coeff_ket:left S0 (ket_ops+:right S0 -> ket_calculate(left,right)
                                          | -> left)                                          
"""

# what happens if we have eg: "3.73.222751" (ie, more than one dot?)
def float_int(n,d):
  x = float(n)/float(d)
  if x.is_integer():
    return int(x)                                      # still haven't decided if should return float/int or string.
  return x                                             # seems compound-op is easier if we return a string.

def process_compound_op(op,parameters):
  parameters = ",".join(parameters) 
  if op not in compound_table:
    logger.debug(op + " not in compound_table")
    python_code = ""
  else:
    python_code = compound_table[op].format(parameters)   # possibly risk of injection attack here
  return python_code
  
def process_power_op(op,power):
  python_code = op
  for k in range(power):                                   # is there a better way to do this? Does it matter?
    python_code += op
  return python_code

def is_number(x):
  try:
    v = float(x)
    return True
  except:
    return False

# converts a single operator into python
# this takes quite a bit of work, because there are such a variety of different operator types, and they all need to be handled separately.
#
# At some stage I want to rearchitect this beast. Instead of a million separate tables, I just want one. But that is for later.    
#
def process_single_op(op):
  logger.debug("process_single_op: op: " + str(op)) 

  if type(op) is list:                                         # compound op found:
    logger.debug("compound op found")
    the_op = op[0]
    parameters = ",".join(op[1:])                         # not 100% sure this is the best way to handle parameters. eg, maybe we should pass a list? 
    if the_op not in compound_table:
      logger.debug(the_op + " not in compound_table")
      python_code = ""
    else:
      python_code = compound_table[the_op].format(parameters) # probably risk of injection attack here

  elif type(op) is tuple:                                               # powered op found:
    logger.debug("powered op found")
    the_op, power = op
    processed_op = process_single_op(the_op)                            # recursion, hope it works.
    python_code = ""
    for k in range(power):
      python_code += processed_op
    
#  elif is_number(op):                                                    # simple-float found
  elif type(op) in [int, float]:  
    python_code = ".multiply({0})".format(str(op))
  
  elif op == '-':       # treat - |x> as mult[-1] |x>                   # not sure we want to keep this. I think simple-float has this covered. Just use '-1', not '-' 
    python_code = ".multiply(-1)"

  elif op == "\"\"":
    python_code = ".apply_op(context,\"\")"

  elif op == "ops":                                          # short-cut so we don't have to type supported-ops all the time!
    python_code = ".apply_op(context,\"supported-ops\")"
    
                                                             # must be a simple-op. Let's find in which table:
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
  elif op in sp_context_table:
    logger.debug("op in sp context table")
    python_code = ".apply_sp_fn({0},context)".format(sp_context_table[op])
  elif not valid_op(op):                                 # doesn't the parsley handle this?
    logger.info("why are we in the not valid_op section of process_single_op??")
    return ""
  else:
    logger.debug("op is literal")               # NB: we have to be very careful here, or it will cause SQL-injection type bugs!!
    python_code = ".apply_op(context,\"{0}\")".format(op)  # fix is not hard. Process the passed in op to a valid op form.
  logger.debug("in process_single_op: python:" + python_code)                                   # lower+upper+dash+number and thats roughly it.
  return python_code
    

parse_dictionary = {
  "float_int"           : float_int, 
#  "process_compound_op" : process_compound_op,
#  "process_single_op"   : process_single_op,
#  "process_power_op"    : process_power_op, 
  }
  
op_grammar = makeGrammar(our_operator_grammar,parse_dictionary)

# converts an op-sequence into python:
def process_op_sequence(ops):
  logger.debug("process_op_sequence: ops: " + ops)
  try:
    parsed_operators = op_grammar(ops).op_sequence()
    logger.debug("parsed_ops: " + str(parsed_operators))
    processed_operators = [ process_single_op(op) for op in parsed_operators ]
  except Exception as e:
    logger.debug("process_op_sequence: exception reason: " + str(e))
    return None
  return "".join(reversed(processed_operators))

# this function will probably go away in future, now that process_op_sequence does most of the work.
def process(context,ops,x):
  logger.debug("process: ops: " + ops)
  logger.debug("process: x: " + str(x))
  python_code = "x" + process_op_sequence(ops)
  if python_code == "x":
    return None
  logger.debug("in process: python: " + python_code)      
  return eval(python_code)                                                    
  
    


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
      #print("els final result:",result)
      logger.debug("els final result: %s" % result)      
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
      logger.debug("els final result: %s" % result)
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
    r.data.append(ket(x))       # breaks if a ket is repeated. The fix is: r += ket(x), but that is a tar pit until fast_sp is subbed in. Something I should do soon!! 
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

# new name. For now just an alias:
def parse_learn_rule(context,s):
  return parse_rule_line(context,s)

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


# 20/9/2015: load_sw(), save_sw(), save_sw_multi() are all now deprecated. I will probably remove them from here at some stage. Probably replace them with functions printing: "moved to new_context() class" 
# They are now in the new_context() class:
#    context.save(filename)
#    context.load(filename)
#    context.append_save(filename)
#    context.multi_save(filename)
#
# Now, make use of parse_rule_line()
# load sw file:
def load_sw(c,file):
  try:
    with open(file,'r') as f:
      for line in f:
        if line.startswith("exit sw"):      # use "exit sw" as the code to stop processing a .sw file.
          return
        parse_rule_line(c,line)             # this is broken! bug found when loading fragment-document.sw fragments
  except Exception as e:
    print("failed to load:",file)
    print("reason:",e)

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
# works fine, though is hinting at getting slow for large sw files. Yeah. It is now very slow on my large sw collection.
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
  

# where is this mess even used! I presume when sub in parsley, this will largely go away.
# tweaked so that left_object can be a string, a ket or a superposition. Need to test it though.
def process_op_ket(C,line,left_object=None):
  if type(left_object) is str:
    left_object = ket(left_object)              
  try:
    op, rest = line.split("|",1)
    op = op.strip()
    label, rest = rest.split(">",1)
    our_ket = ket(label)
    if label == "_self" and left_object is not None:
      our_ket = left_object
    return process(C,op,our_ket), rest
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

# 18/6/2016:
  "fast-simm"           : "fast_simm",              # will this work even though it is defined in code file, and not functions?

  "nfc"                 : "normed_frequency_class",  # pretty unlikely this will be used at command line since needs freq lists.
  "ket-nfc"             : "ket_normed_frequency_class",
#  "apply"               : "apply",                  # 10/11/2014: What is this function?? Commented out!
  "range"               : "show_range",
  "ket-simm"            : "ket_simm",
  "to-base"             : "decimal_to_base",
  "general-to-specific" : "general_to_specific",
  
# 4/1/2015:
  "equal"               : "equality_test",
  
# 22/2/2015:
  "ED"                  : "Euclidean_distance",
  
# 26/2/2015:
  "mbr"                 : "mbr",
  "measure"             : "mbr",

# 19/1/2016:
  "is-mbr"              : "is_mbr",  
  
# 9/4/2015:
  "subset"              : "subset",
  
# 11/8/2015:
  "exclude"             : "exclude",
  
# 16/9/2015:
  "filter-down-to"      : "filter_down_to",
  
# 5/11/2016:
  "vsa-mult"            : "vsa_mult",          
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
  
# 11/9/2015:
  "process-reaction" : "process_reaction",
# 17/2/2016:
  "process-consuming-reaction" : "process_reaction",               # an alias
  "process-catalytic-reaction" : "process_catalytic_reaction",
    
  
# 16/9/2015:
  "respond-to-pattern" : "respond_to_pattern",
  
# 9/2/2016:
  "rename-kets"   : "rename_kets",
  "rewrite"       : "rename_kets",      
}

# the code needed for this not yet implemented.
# whitelisted functions that take 4 parameters:
whitelist_table_4 = {
  "algebra"       : "algebra",
}


# new: 24/11/2016:
# whitelisted functions that need context variable, and takes 1 extra parameter:
# eg: predict_whats_next_one(context,sp1)
context_whitelist_table_1 = {
# 24/11/2016:
  "predict-whats-next" : "predict_whats_next_one",
  
# 29/11/2016:
  "next"               : "sequence_predict_whats_next_skip",   
}


# new: 10/11/2014:
# whitelisted functions that need context variable, and takes 2 extra parameters:
# eg: apply(context,sp1,sp2)
context_whitelist_table_2 = {
  "apply-sp" : "apply_sp",
  "apply"    : "apply_sp",

# 17/1/2015:
  "clone"    : "clone_ket",

# 10/10/2016
  "whats-next" : "whats_next_two",
  
# 24/11/2016:
  "predict-whats-next" : "predict_whats_next_two",

# 25/11/2016:
  "predict-whats-next-skip" : "predict_whats_next_skip_two",
      
}

# new: 25/11/2016:
# whitelisted functions that need context variable, and takes 3 extra parameters:
# eg: predict_whats_next_three(context,one,two,three)
context_whitelist_table_3 = {
# 25/11/2016:
  "predict-whats-next" : "predict_whats_next_three",
  "predict-whats-next-skip" : "predict_whats_next_skip_three",

}
# new: 27/11/2016:
# whitelisted functions that need context variable, and takes 4 extra parameters:
# eg: predict_whats_next_skip_four(context,one,two,three,four)
context_whitelist_table_4 = {
# 27/11/2016:
#  "predict-whats-next" : "predict_whats_next_three",
  "predict-whats-next-skip" : "predict_whats_next_skip_four",
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
#  print("inside process_brackets:",line)
  logger.debug("inside process_brackets: %s " % line)
  try:
    fn, rest = line.split("(",1)
    fn = fn.strip()
    pieces = []
    while True:
      try:
        sp, rest = extract_compound_superposition(C,rest,left_label)     # sp is short for superposition
        pieces.append(sp)
        #print("inside while, rest:",rest)
        logger.debug("inside while, rest: %s" % rest)        
        null, rest = rest.split(",",1)
      except:
        break
    if len(pieces) == 0:
      return None
    null, rest = rest.split(")",1)
  except:
    return None

  #print("fn:  ",fn)
  #print("len: ",len(pieces))
  #for sp in pieces:
  #  print("sp: ",sp)
  #print("rest:",rest)

  logger.debug("fn:  %s " % fn)
  logger.debug("len: %s" % len(pieces))
  for sp in pieces:
    logger.debug("sp: %s" % sp)
  logger.debug("rest: %s" % rest)
    

# what if len(fn) == 0?

  if len(pieces) == 1:
    if fn in whitelist_table_1:
      print("op in whitelist 1")
      code = whitelist_table_1[fn] + "(pieces[0])"
      print("py:",code)
      result = eval(code)
      return result, rest
    elif fn in context_whitelist_table_1:
      print("op in context whitelist 1")
      code = context_whitelist_table_1[fn] + "(C,pieces[0])"
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
    elif main_fn in context_whitelist_table_3:
      match = True
      print("op in context whitelist 3")
      code = context_whitelist_table_3[main_fn] + "(C,pieces[0],pieces[1],pieces[2])"
  if len(pieces) == 4:
    if main_fn in whitelist_table_4:
      match = True
      print("op in whitelist 4")
      code = whitelist_table_4[main_fn] + "(pieces[0],pieces[1],pieces[2],pieces[3])"
    elif main_fn in context_whitelist_table_4:
      match = True
      print("op in context whitelist 4")
      code = context_whitelist_table_4[main_fn] + "(C,pieces[0],pieces[1],pieces[2],pieces[3])"

      
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


