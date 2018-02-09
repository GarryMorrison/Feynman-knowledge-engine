#######################################################################
# the semantic-db parser
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2014
# Update: 8/2/2018
# Copyright: GPLv3
#
# Usage: 
#
#######################################################################

from parsley import makeGrammar

from the_semantic_db_processor_tables import *
from the_semantic_db_code import *

#context = context_list("parse compound sequence")

from string import ascii_letters
def valid_op(op):                                                       # do we still need this now we have a better parser?
  if not op[0].isalpha() and not op[0] == '!':
    return False
  return all(c in ascii_letters + '0123456789-+!?.' for c in op)
  

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


# operator parse:
our_grammar = """
# number copied from here:
# http://parsley.readthedocs.org/en/latest/tutorial2.html
number = ('-' | -> ''):sign (intPart:ds (floatPart(sign ds)
                                        | -> int(sign + ds)))
digit = :x ?(x in '0123456789') -> x
digits = <digit*>
digit1_9 = :x ?(x in '123456789') -> x
intPart = (digit1_9:first digits:rest -> first + rest) | digit
floatPart :sign :ds = <('.' digits exponent?) | exponent>:tail
                     -> float(sign + ds + tail)
exponent = ('e' | 'E') ('+' | '-')? digits


# my parsley code:

valid_ket_chars = :x ?(x not in '<|>')
naked_ket = '|' <valid_ket_chars*>:x '>' -> x
coeff_ket = (number | -> 1):value ws naked_ket:label -> (label, value)
signed_ket = ('-' | -> ''):sign ws (number | -> 1):value ws naked_ket:label -> (label, float(sign + str(value))) 

op_symbol = ('+' | '-' | '__' | '.' | '_')
symbol_ket = ws op_symbol:symbol ws coeff_ket:k -> (symbol, k)
literal_sequence = ws signed_ket:left ws symbol_ket*:right ws -> ket_calculate(left, right)


positive_int = <digit+>:n -> int(n)
fraction = number:numerator (ws '/' ws number | -> 1):denominator -> float_int(numerator/denominator)
#S0 = ' '*
ws = ' '*
S1 = ' '+
op_start_char = anything:x ?(x.isalpha() or x == '!') -> x
op_char = anything:x ?(x.isalpha() or x.isdigit() or x in '-+!?.')
simple_op = op_start_char:first <op_char*>:rest -> first + rest
filtered_char = anything:x ?(x not in '[]|><') -> x
filtered_parameter_string = '"' ( ~'"' filtered_char)*:c '"' -> ''.join(c)
parameters = (fraction | simple_op | filtered_parameter_string | '\"\"' | '*'):p -> str(p)

compound_op = simple_op:the_op '[' parameters:first (',' ws parameters)*:rest ']' -> ['c_op', the_op] + [first] + rest
#function_op = simple_op:the_op '(' ws literal_sequence:first (',' ws literal_sequence)*:rest ws ')' -> ['f_op', the_op] + [first] + rest
function_op = simple_op:the_op '(' ws full_compound_sequence:first (',' ws full_compound_sequence)*:rest ws ')' -> ['f_op', the_op] + [first] + rest
#function_op = simple_op:the_op ws '(' ws full_compound_sequence:first (',' ws full_compound_sequence)*:rest ws ')' -> ['f_op', the_op] + [first] + rest
general_op = (bracket_ops | compound_op | function_op | simple_op | number | '\"\"' ):the_op -> the_op
powered_op = general_op:the_op '^' positive_int:power -> (the_op, power)

op = (powered_op | general_op):the_op -> the_op
op_sequence = (ws op:first (S1 op)*:rest ws -> [first] + rest)
              | ws -> []
symbol_op_sequence = ws op_symbol:symbol ws op_sequence:seq -> (symbol, seq)
#bracket_ops = '(' ws (op_symbol | -> '+'):symbol op_sequence:first ws symbol_op_sequence*:rest ws ')' -> [[(symbol, first)] + rest]
bracket_ops = '(' ws (op_symbol | -> '+'):symbol op_sequence:first ws symbol_op_sequence*:rest ws ')' -> [(symbol, first)] + rest

#single_compound_sequence = op_sequence:ops naked_ket:first -> [ops, first]
#single_compound_sequence = op_sequence:ops (naked_ket | -> ''):first -> [ops, first]
bracket_sequence = '(' ws full_compound_sequence:seq ws ')' -> seq
single_compound_sequence = op_sequence:ops (naked_ket | bracket_sequence | -> ''):first -> [ops, first]

symbol_single_compound_sequence = ws op_symbol:symbol ws single_compound_sequence:seq -> (symbol, seq)
full_compound_sequence = ws (op_symbol | -> '+'):symbol single_compound_sequence:first ws symbol_single_compound_sequence*:rest ws -> [(symbol, first)] + rest

compiled_compound_sequence = full_compound_sequence:seq -> compile_compound_sequence(context, seq)

new_line = ('\r\n' | '\r' | '\n')
#char = :c ?(is_not_newline(c)) -> c
char = ~new_line anything
line = <char*>:s -> s
#line = <~new_line anything>*:s -> "".join(s)
object = (naked_ket | '(*)' | '(*,*)' | '(*,*,*)' | full_compound_sequence ):obj -> obj
stored_rule = ws (simple_op | -> ''):prefix_op ws object:obj ws ('#=>' | '!=>'):rule_type ws line:s -> learn_stored_rule(context, prefix_op, obj, rule_type, s)
#memoizing_rule = ws (simple_op | -> ''):prefix_op ws object:obj ws '!=>' ws line:s -> learn_memoizing_rule(context, prefix_op, obj, s)
#learn_rule =  ws (simple_op | -> ''):prefix_op ws object:obj ws ('=>' | '+=>'):rule ws compiled_compound_sequence:seq -> learn_standard_rule(context, prefix_op, obj, rule, seq)
learn_rule =  ws (simple_op | -> ''):prefix_op ws object:obj ws ('=>' | '+=>'):rule_type ws full_compound_sequence:parsed_seq -> learn_standard_rule(context, prefix_op, obj, rule_type, parsed_seq)
recall_rule = ws (simple_op | "\'\'" ):prefix_op ws object:obj -> recall_rule(context, prefix_op, obj)

sw_file = (learn_rule | stored_rule | new_line)*
process_rule_line = (learn_rule | stored_rule | compiled_compound_sequence | new_line)
"""

def float_int(x):
  if x.is_integer():
    return int(x)
  return x

def ket_calculate(start,pairs):
  print('pairs: %s' % (pairs))

  seq = sequence()
  sp = superposition(*start)
  for op, value in pairs:
    if op == '+':
      sp.add(*value)
    elif op == '-':
      sp.sub(*value)
    elif op == '_':     
      sp.merge_sp(superposition(*value))
    elif op == '__':
      sp.merge_sp(superposition(*value), ' ')
    elif op == '.':
      seq += sp
      sp = superposition(*value)
  seq += sp
  return seq

from pprint import pprint
def my_print(name, value=''):
  #return
  if value is '':
    print(name)
  else:
    print(name + ': ', end='')
    pprint(value)

def process_operators(context, ops, seq, self_object = None):
  if len(ops) == 0:
    return seq
  python_code = ''
  for op in reversed(ops):
    if type(op) is list:                                      # found either a compound-op, a function-op or bracket-ops
      my_print('op[0]', op[0])
      if op[0] is 'c_op':
        my_print('compound_op')
        python_code = process_single_op(op[1:])
        if len(python_code) > 0:
          seq = eval('seq' + python_code)
      elif op[0] is 'f_op':
        my_print('function_op')
        null, fnk, *data = op
        my_print('fnk', fnk)
        my_print('data', data)

        python_code = ''
        if len(data) == 1:                                    # 1-parameter function:
          if fnk in whitelist_table_1:
            python_code = "%s(*seq_list)" % whitelist_table_1[fnk]
          else:
            the_seq = compile_compound_sequence(context, data[0], self_object)
            seq = process_operators(context, [fnk], the_seq, self_object)
        if len(data) == 2:                                    # 2-parameter function:
          if fnk in whitelist_table_2:
            python_code = "%s(*seq_list)" % whitelist_table_2[fnk]
        elif len(data) == 3:                                  # 3-parameter function:
          if fnk in whitelist_table_3:
            python_code = "%s(*seq_list)" % whitelist_table_3[fnk]
        elif len(data) == 4:                                  # 4-parameter function:
          if fnk in whitelist_table_4:
            python_code = "%s(*seq_list)" % whitelist_table_4[fnk]
        if len(python_code) > 0:
          my_print("whitelist_table: python code", python_code)
          seq_list = [compile_compound_sequence(context, x, self_object) for x in data]
          str_seq_list = [str(x) for x in seq_list]
          my_print('str_seq_list', str_seq_list)
          seq = eval(python_code)
          python_code = ''
      elif op[0][0] in ['+', '-', '_', '.']:
        my_print('bracket ops')
        my_print('bracket ops seq', str(seq))
        version_1 = True
        if version_1:
          new_seq = sequence([])
          for bracket_op in op:
            my_print('bracket_op', bracket_op)
            symbol, bracket_ops = bracket_op
            my_print('symbol', symbol)
            my_print('bracket_ops', bracket_ops)
            the_seq = process_operators(context, bracket_ops, seq, self_object)

            if symbol == '+':
              new_seq.add_seq(the_seq)
            elif symbol == '-':
              new_seq.sub_seq(the_seq)
            elif symbol == '_':
              new_seq.merge_seq(the_seq)
            elif symbol == '__':
              new_seq.merge_seq(the_seq, ' ')
            elif symbol == '.':
              new_seq += the_seq
            my_print('new_seq', str(new_seq))
          seq = new_seq
        else:                                                         # finish this branch!
          for sp in seq:                                              # haven't handled sequences yet. eg, (op3 _ op2) (|x> . |y> + |z>)
            r = sequence([])
            for x in sp:
              new_seq = sequence([])
              for bracket_op in op:
                my_print('bracket_op', bracket_op)
                symbol, bracket_ops = bracket_op
                my_print('symbol', symbol)
                my_print('bracket_ops', bracket_ops)
                the_seq = process_operators(context, bracket_ops, x, self_object)
         
                if symbol == '+':
                  new_seq.add_seq(the_seq)
                elif symbol == '-':
                  new_seq.sub_seq(the_seq)
                elif symbol == '_':
                  new_seq.merge_seq(the_seq)                           # do we need distributed_merge_seq here too? I suspect yes. 
                elif symbol == '__':
                  new_seq.merge_seq(the_seq, ' ')
                elif symbol == '.':
                  new_seq += the_seq
                my_print('new_seq', str(new_seq))
              r.add_seq(new_seq)
            seq = r
    elif type(op) is tuple:                                            # powered op found.
      tuple_op, power = op
      my_print('tuple_op', tuple_op)
      my_print('power', power)
      for _ in range(power):                                           # is there a better way to implement this?
        seq = process_operators(context, [tuple_op], seq, self_object)
    else:
      python_code = process_single_op(op)
      if len(python_code) > 0:
        seq = eval('seq' + python_code)
  return seq


def compile_compound_sequence(context, compound_sequence, self_object = None):
  my_print('cs', compound_sequence)
  my_print('self', self_object)

  seq = sequence([])
  for seq2 in compound_sequence:
    symbol, (ops, object) = seq2
    my_print('symbol', symbol)
    my_print('ops', ops)
    my_print('object', object)

    distribute = True
    the_seq = sequence([])
    if type(object) is str:                                       # found a ket
      if object == '_self' and type(self_object) in [str, ket, superposition, sequence]:
        the_seq = sequence(self_object)
      elif object.startswith('_self') and type(self_object) is list:          # this branch needs to handle |_self> too.
        try:
          position = int(object[5:])
        except:
          position = 1
        try:
          the_seq = sequence(self_object[position - 1])
        except Exception as e:
          my_print('self object exception', e)
          the_seq = sequence(superposition(object))
      else:
        the_seq = sequence(superposition(object))

    if type(object) is list:
      my_print('fish')
      the_seq = compile_compound_sequence(context, object, self_object)
      distribute = True

    my_print('\n----------\nfinal')
    my_print('ops', ops)
    my_print('the_seq', str(the_seq))
    my_print('distribute', distribute)
    my_print('----------\n')
    the_seq = process_operators(context, ops, the_seq, self_object)
    #my_print('really final the_seq', str(the_seq))


    if symbol == '+':
      seq.tail_add_seq(the_seq)
    elif symbol == '-':
      seq.tail_sub_seq(the_seq)
    elif symbol == '_':
      if not distribute:
        seq.merge_seq(the_seq)
      if distribute:
        seq.distribute_merge_seq(the_seq)
    elif symbol == '__':
      if not distribute:
        seq.merge_seq(the_seq, ' ')
      if distribute:
        seq.distribute_merge_seq(the_seq, ' ')
    elif symbol == '.':
      seq += the_seq
  return seq

def learn_stored_rule(context, op, one, rule_type, s):
  my_print('op', op)
  my_print('one', one)
  my_print('rule_type', rule_type)
  my_print('s', s)
  if rule_type == '#=>':
    context.learn(op, one, stored_rule(s))
  elif rule_type == '!=>':
    context.learn(op, one, memoizing_rule(s))
#  context.print_universe()

def learn_standard_rule(context, op, one, rule_type, parsed_seq):
  my_print('op', op)
  my_print('one', one)
  my_print('type(one)', type(one))
  my_print('rule_type', rule_type)

  if type(one) is str:
    seq = compile_compound_sequence(context, parsed_seq, [one])
    my_print('seq', str(seq))

    if op == '' and one == 'context' and rule_type == '=>':
      name = seq[0].label
      if name.startswith('context: '):
        context.set(name[9:])
    elif rule_type == '=>':
      context.learn(op, one, seq)
    elif rule_type == '+=>':
      context.add_learn(op, one, seq)
  elif type(one) is list:                          # indirect learn rule found
    indirect_object = compile_compound_sequence(context, one)
    my_print('indirect learn object', str(indirect_object))  
    for sp in indirect_object:
      for one in sp:
        seq = compile_compound_sequence(context, parsed_seq, [one])
        if rule_type == '=>':
          context.learn(op, one, seq)
        elif rule_type == '+=>':
          context.add_learn(op, one, seq)


def recall_rule(context, op, one):
  return context.recall(op, one)
#  return ket(one).apply_op(context, op)

def extract_compound_sequence(context, unparsed_seq, self_object = None):      # need to make context explicit somewhere ... rather than a global....
  parsed_seq = op_grammar(unparsed_seq).full_compound_sequence()
  my_print('parsed_seq', parsed_seq)
  my_print('self_object', self_object)
  seq = compile_compound_sequence(context, parsed_seq, self_object)
  return seq

def process_sw_file(context, sw_text):
  op_grammar(sw_text).sw_file()  

def is_not_newline(c):
  return c not in ['\r', '\n']

#from the_semantic_db_code import *
context = context_list('in the processor')
#context = ''
  
bindings_dictionary = {
  'ket_calculate'                  : ket_calculate,
  'compile_compound_sequence'      : compile_compound_sequence,
  'float_int'                      : float_int,
  'learn_stored_rule'              : learn_stored_rule,
#  'learn_memoizing_rule'           : learn_memoizing_rule,
  'learn_standard_rule'            : learn_standard_rule,
  'recall_rule'                    : recall_rule,
  'context'                        : context,
  'is_not_newline'                 : is_not_newline,
}

op_grammar = makeGrammar(our_grammar, bindings_dictionary)

