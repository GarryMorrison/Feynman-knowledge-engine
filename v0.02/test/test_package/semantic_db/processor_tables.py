#######################################################################
# the semantic-db processor operator tables
# yeah, ugly, will fix later.
# also, more documentation later!
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 9/2/2018
# Update: 22/2018
# Copyright: GPLv3
#
# Usage: 
#
#######################################################################


# Some hash tables mapping ops to the python equivalent.
# Left hand side is BKO language, right is python.

# functions built into ket/superposition classes.
built_in_table_usage = {}
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
#  "max"              : "find_max",
#  "min"              : "find_min",

# new:
  "discrimination"   : "discrimination",
  "discrim"          : "discrimination",

# special:
#    "type"           : "type",                    # implemented for debugging purposes.

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
  
  "sdrop"            : "sdrop",                           # can we define these in usage_tables.py?
  "spick-elt"        : "spick_elt",
  "sreverse"         : "sreverse",
  
}                                                                                      

# table of sigmoids:
sigmoid_table_usage = {}
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
fn_table_usage = {}
fn_table = {
#  "apply-value"      : "apply_value",
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
fn_table2_usage = {}
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
compound_table_usage = {}
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

  "sselect"            : ".sselect_range({0})",
  
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
#  "table"              : ".apply_sp_fn(pretty_print_table,context,\"{0}\")",
  
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
  "int-divide-by"         : ".apply_fn(int_divide_numbers,{0})",
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
  
# 9/12/2016:
  "random-frame"            : ".apply_naked_fn(random_frame,\"{0}\")",
  "display-frame"           : ".apply_sp_fn(display_frame,\"{0}\")",
  "display-frame-sequence"  : ".apply_sp_fn(display_frame_sequence,context,\"{0}\")", 
  
# 19/12/2016:
#  "next"                   : ".apply_fn(sequence_predict_whats_next_skip,context,\"{0}\")",
  
# 6/6/2017:
  "float-sequence"         : ".apply_fn(float_sequence,context,\"{0}\")",                       # buggy ...

# 8/2/2018:
#  'ssplit'                 : '.apply_sp_fn(ssplit, \"{0}\")',
# 17/2/2018:
#  'insert'                 : '.apply_sp_fn(insert, \"{0}\")',        
      
}


# 7/4/2014: new addition, functions that map sp -> ket/sp
# Pretty sure this breaks the linearity. 
# Ie, the functions here are in general not linear, while most other ops/fns are.
# 30/6/2014: heh. I'd forgotten I had this! 
sp_fn_table_usage = {}
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

# 8/2/2018:
  'spell-out'          : 'spell_out',
#  'ssplit'             : 'ssplit',
}

# 2/2/2015: new addition functions that map ket -> ket/sp but needs context info.
ket_context_table_usage = {}
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

# 30/11/2016:
#  "next"                : "sequence_predict_whats_next_skip",
  
# 6/6/2017:
  "float-sequence"      : "float_sequence",               
}

# for operators that take sequences as input:
seq_fn_table = {}

# 28/7/2016: new addition, functions that map sp -> sp but needs context info.
# I tried putting it in the compound op table, but that failed since it has no parameters.
#
sp_context_table_usage = {}
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



# dummy len 1 fn:
def sp_len_1(x):
  return ket("sp") + x

# white listed functions that take 1 parameter:
whitelist_table_1_usage = {}
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
whitelist_table_2_usage = {}
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
whitelist_table_3_usage = {}
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
whitelist_table_4_usage = {}
whitelist_table_4 = {
  "algebra"       : "algebra",
}


# new: 24/11/2016:
# whitelisted functions that need context variable, and takes 1 extra parameter:
# eg: predict_whats_next_one(context,sp1)
context_whitelist_table_1_usage = {}
context_whitelist_table_1 = {
# 24/11/2016:
  "predict-whats-next" : "predict_whats_next_one",
  
# 29/11/2016:
#  "next"               : "sequence_predict_whats_next_skip",       # changed invoke from: next(|mary.went>) to next |mary.went>   
}


# new: 10/11/2014:
# whitelisted functions that need context variable, and takes 2 extra parameters:
# eg: apply(context,sp1,sp2)
context_whitelist_table_2_usage = {}
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
context_whitelist_table_3_usage = {}
context_whitelist_table_3 = {
# 25/11/2016:
  "predict-whats-next" : "predict_whats_next_three",
  "predict-whats-next-skip" : "predict_whats_next_skip_three",

}
# new: 27/11/2016:
# whitelisted functions that need context variable, and takes 4 extra parameters:
# eg: predict_whats_next_skip_four(context,one,two,three,four)
context_whitelist_table_4_usage = {}
context_whitelist_table_4 = {
# 27/11/2016:
#  "predict-whats-next" : "predict_whats_next_three",
  "predict-whats-next-skip" : "predict_whats_next_skip_four",
}


