from collections import OrderedDict

class NewContext(object):
  def __init__(self,name):
    self.name = name
    self.ket_rules_dict = OrderedDict()
    self.sp_rules_dict = OrderedDict()
    self.supported_operators_dict = OrderedDict()

  def set(self,name):                           # not 100% sure this is the best way, or correct.
    self.name = name                            # BTW, it is intended to erase what is currently defined for the current context.
    self.ket_rules_dict = OrderedDict()
    self.sp_rules_dict = OrderedDict()
    self.supported_operators_dict = OrderedDict()
    
# 3/12/2015:
  def context_name(self):
    return self.name    

# op is a string
# label is a string or a ket
# rule can be anything
# add_learn is either True or False
#
  def learn(self,op,label,rule,add_learn=False):
    # some prelims:
    if op == "supported-ops":                    # never learn "supported-ops", it is auto-generated and managed
      return
    if type(label) == ket:                       # label is string. if ket, convert back to string
      label = label.label
    if type(rule) == str:                        # rule is assumed to be ket, superposition, or stored rule (maybe fast sp too).
      rule = ket(rule)                           # if string, cast to ket

    if type(rule) == list:                       # if list, cast to superposition
      r = superposition()
      for x in rule:
        if type(x) == int or type(x) == float:
          r += ket("number: " + str(x))
        elif type(x) == str:
          r += ket(x)
      rule = r
                
    if len(rule) == 0:                           # do not learn rules that are |>
      return

    # 9/2/2016:
    self.supported_operators_dict[op] = True     # learn supported operators in this context

    if label not in self.ket_rules_dict:
      self.ket_rules_dict[label] = OrderedDict()
      self.ket_rules_dict[label]["supported-ops"] = superposition()
    #self.ket_rules_dict[label]["supported-ops"].clean_add(ket("op: " + op))  # this is probably a speed bump now.
    self.ket_rules_dict[label]["supported-ops"].max_add("op: " + op)          # this is probably a speed bump now.
                                                                             # but if we merge over to fast_sp, that should fix itself.
    if not add_learn:
      self.ket_rules_dict[label][op] = rule
    else:
      if op not in self.ket_rules_dict[label]:
        self.ket_rules_dict[label][op] = superposition()             # this breaks add_learn for stored_rules, and memoizing_rules. Do we want to fix it?
#      self.ket_rules_dict[label][op].clean_add(rule)
#      self.ket_rules_dict[label][op].self_add(rule)                  # does this change break anything?? If it does, we will need another approach.
      self.ket_rules_dict[label][op].add_sp(rule)                    # Hrmm... how test if it breaks? We don't have full test cases yet!
                                                                     # create inverse still seems to work, I think. 
  def add_learn(self,op,label,rule):
    return self.learn(op,label,rule,add_learn=True)                  # corresponds to "op |x> +=> |y>"

# op is a string, or a ket in form |op: some-operator>
# label is a string or a ket
#
  def recall(self,op,label,active=False):
    # some prelims:
    if type(op) == ket:
      op = op.label[4:]                         # map |op: age> to "age"
    if type(label) == ket:
      coeff = label.value
      ket_label = label.label
    else:
      coeff = 1
      ket_label = label
#    coeff = 1                                  # use this to switch off the multiply(coeff) feature

    match = False
    for trial_label in label_descent(ket_label):
      if trial_label in self.ket_rules_dict:
        if op in self.ket_rules_dict[trial_label]:
          rule = self.ket_rules_dict[trial_label][op]
          match = True
          break
    if not match:
      #logger.info("recall not found")
      #logger.info(op + " " + str(ket(ket_label)) + " not found")
      logger.info("%s %s not found" % (op,ket(ket_label)))
      rule = ket("",0)

    if active:
      rule = rule.activate(self,op,ket_label)
    return rule.multiply(coeff)

# op is a string
# label is a string or a ket
# rule can be anything
# add_learn is either True or False
#
  def sp_learn(self,op,label,rule,add_learn=False):     # op (*) => |y>. Note, the plan is for sp rules to have higher precedence than ket rules.
    # some prelims:                                     # Plan to implement this in apply_op(context,"op")
    if op == "supported-ops":                    # never learn "supported-ops", it is auto-generated and managed
      return
    if type(label) == ket:                       # label is string. if ket, convert back to string
      label = label.label
    #label = "*"                                  # hrmm... for now. Almost certainly tweak later!
    if type(rule) == str:                        # rule is assumed to be ket, superposition, or stored rule (maybe fast sp too).
      rule = ket(rule)                           # if string, cast to ket
    if len(rule) == 0:                           # do not learn rules that are |>
      return

    if label not in self.sp_rules_dict: 
      self.sp_rules_dict[label] = OrderedDict()
      self.sp_rules_dict[label]["supported-ops"] = superposition()
    self.sp_rules_dict[label]["supported-ops"].max_add("op: " + op)          # this is probably a speed bump now.
                                                                             # but if we merge over to fast_sp, that should fix itself.
    if not add_learn:
      self.sp_rules_dict[label][op] = rule
    else:
      if op not in self.sp_rules_dict[label]:
        self.sp_rules_dict[label][op] = superposition()
      self.sp_rules_dict[label][op].clean_add(rule)

  def sp_add_learn(self,op,label,rule):
    return self.sp_learn(op,label,rule,True)       # corresponds to "op (*) +=> |y>"

# op is a string, or a ket in form |op: some-operator>
# seq_list is a list of sequences 
#
  def sp_recall(self, op, seq_list, active=False):    # work in progress ...
    logger.debug("inside sp_recall")
    #return ket("",0)                         # currently the code that follows this is broken, so this is the temp work-around.
    # some prelims:
    if type(op) == ket:
      op = op.label[4:]                         # map |op: age> to "age"
    #ket_label = "*"                             # probably tweak later. Eg if I decide to implement op(*,*), op(*,*,*) etc. Also, maybe op(fixed-object) #=> ... 
    #ket_label = sp
    if type(seq_list) is str:
      ket_label = seq_list
    elif type(seq_list) is list:
      if len(seq_list) == 1:
        ket_label = '*'
      elif len(seq_list) == 2:
        ket_label = '*,*'
      elif len(seq_list) == 3:
        ket_label = '*,*,*'
      elif len(seq_list) == 4:
        ket_label = '*,*,*,*'

    match = False                               # If/when I implement op(*,*) et al, I need a tidy way to handle stored rules and |_self1> vs |_self2> etc! No idea how to do that currently.  
    if ket_label in self.sp_rules_dict:
      if op in self.sp_rules_dict[ket_label]:
        rule = self.sp_rules_dict[ket_label][op]
        match = True
    
    if not match:
      logger.debug("%s (*) not found" % (op))   # tweak later! Probably want to switch this off completely once testing is done. 
      rule = ket("",0)

    if active:
#      rule = rule.activate(self,op,sp)        # how handle op (*) #=> foo |_self> ??  op (|a> + |b>) returns foo (|a> + |b>)
#    return rule.multiply(coeff)              # I'm not sure multiply(coeff) makes sense for sp_recall().
      if type(rule) in [memoizing_rule, stored_rule]:
        try:
          #resulting_rule = extract_compound_superposition(self,rule,sp)[0]  # we need to fix ECS so that it can handle superpositions as self-objects. Currently it can only handle strings.
          logger.debug('rule: %s' % rule)
          logger.debug('seq: %s' % seq_list[0])
          resulting_rule = extract_compound_superposition(self, rule , seq_list[0])[0]
        except Exception as e:
          resulting_rule = ket()
          logger.warning("except while processing stored_rule: %s" % e)
        if type(rule) is memoizing_rule:
          self.sp_learn(op,sp,resulting_rule)
        rule = resulting_rule
    logger.debug("leaving sp_recall")
    return rule                                


# op is a string, or a ket in form |op: some-operator>
# label is a string or a ket
#
  def dump_rule(self,op,label,exact=False):
    # some prelims:
    if type(op) == ket:
      op = op.label[4:]
    ket_name = label if type(label) == ket else ket(label) # maybe tidy this.

    rule = self.recall(op,label)
    rule_string = " => "
    if type(rule) == stored_rule:
      rule_string = " #=> "
    if type(rule) == memoizing_rule:
      rule_string = " !=> "
      

    return op + " " + ket_name.display() + rule_string + rule.display(exact)

# previously called dump_all_rules()
  def dump_ket_rules(self,label,exact=False):
    # some prelims:
    if type(label) == ket:
      ket_label = label.label
    else:
      ket_label = label

    if ket_label not in self.ket_rules_dict:
      return ""

    return "\n".join(self.dump_rule(op,label,exact) for op in self.ket_rules_dict[ket_label] if exact or (op != "supported-ops") )

  def dump_sp_rule(self,op,label,exact=False):
    # some prelims:
    if type(op) == ket:
      op = op.label[4:]
    sp_name = label

    rule = self.sp_recall(op, label)
    rule_string = " => "
    if type(rule) == stored_rule:
      rule_string = " #=> "
    if type(rule) == memoizing_rule:
      rule_string = " !=> "
     
    return op + " (" + sp_name + ")" + rule_string + rule.display(exact)

  def dump_sp_rules(self,label,exact=False):
    if label not in self.sp_rules_dict:
      return ""
    return "\n".join(self.dump_sp_rule(op,label,exact) for op in self.sp_rules_dict[label] if exact or (op != "supported-ops") )


  # instead of dumping all the rules for a known ket, dump all the rules for all kets in the given superposition:
  # sp should be a ket, or superposition
  #
  def dump_multiple_ket_rules(self,sp,exact=False):                           # Hrmm... Long since forgotten what this is meant to do! Where is it even used?? Answer: in the console.
    if type(sp) == str:                                             # and the name conflicts with what I was going to call some-sp-op (*) #=> some-rule |_self> 
      sp = ket(sp)                                                  # Let's find a better name! Done. dump_sp_rules => dump_multiple_ket_rules
    return "\n\n".join(self.dump_ket_rules(x,exact) for x in sp )

  # dump everything we know about the current context:
  def dump_universe(self,exact=False,show_context_header=True):      # I think this is right, but need to test it. 
    if show_context_header:
      context_string = "|context> => |context: " + self.name + ">"
      sep = "\n----------------------------------------\n"
    else:
      context_string = ""
      sep = ""
#    return sep + context_string + "\n\n" + "\n\n".join(self.dump_ket_rules(x,exact) for x in self.ket_rules_dict ) + sep
    result_string = ""
    if len(self.ket_rules_dict) > 0:
      result_string += "\n\n" + "\n\n".join(self.dump_ket_rules(x,exact) for x in self.ket_rules_dict )
    if len(self.sp_rules_dict) > 0:
      result_string += "\n\n" + "\n\n".join(self.dump_sp_rules(x,exact) for x in self.sp_rules_dict )
    return sep + context_string + result_string + sep  

# not 100% sure we want this, but I'll add it for now:
# See, new_context() only has 1 context, so dump_multiverse() doesn't make a whole lot of sense.
# context.multi_save(filename) is one reason I decided to add it.
  def dump_multiverse(self,exact=False):
    return self.dump_universe(exact) 

  # create inverse for a single learn rule:
  # not sure we want this factored out. But leave as is for now.
  def create_single_learn_rule_inverse(self,op,label):
    # some prelims:
    if type(op) == ket:
      op = op.label[4:]
    if op.startswith("inverse-"):              # don't take the inverse of an inverse.
      return
    if type(label) == ket:
      label = label.label

    if label not in self.ket_rules_dict:
      return
    if op not in self.ket_rules_dict[label]:
      return

    rule = self.ket_rules_dict[label][op]
    if type(rule) in [ket, superposition, fast_superposition]:      # don't learn inverse for stored_rules.
      for x in rule:
        if x.label != "":
          self.add_learn("inverse-" + op,x,label)                   # do we want ket(label)?
                                                                    # also, NB: the add_learn. ie, slow with current superposition class.
                                                                    # will be faster with fast_superposition class (which I will swap in eventually!)

  # create inverse for a single known ket:
  def create_ket_rules_inverse(self,label):
    if type(label) == ket:
      label = label.label
    if label not in self.ket_rules_dict:
      return

    for op in self.ket_rules_dict[label]:
      self.create_single_learn_rule_inverse(op,label)


  # it would be nice for this to be idempotent, but I don't think it is.
  # also, slightly concerned we may create infinite loops, though no example of that seen so far.
  #
  # create inverse for all known kets:
  def create_universe_inverse(self):
    for label in self.ket_rules_dict:
      self.create_ket_rules_inverse(label)

# let's merge in the pieces, into one function:
# doh! so much for that! Pretty sure infinite loop.
  def infinite_loop____create_universe_inverse(self):
    for label in self.ket_rules_dict:
      for op in self.ket_rules_dict[label]:
        rule = self.ket_rules_dict[label][op]
        if type(rule) in [ket, superposition, fast_superposition]:      # don't learn inverse for stored_rules.
          for x in rule:
            if x.label != "":
              self.add_learn("inverse-" + op,x,label)

  def create_inverse_op(self,op):
    if type(op) == ket:
      op = op.label[4:] 
    for label in self.ket_rules_dict:
      if op in self.ket_rules_dict[label]:
        rule = self.ket_rules_dict[label][op]
        if type(rule) in [ket, superposition, fast_superposition]:      # don't learn inverse for stored_rules.
          for x in rule:
            if x.label != "":
              self.add_learn("inverse-" + op,x,label)


# do we need unlearn stuff?
# unlearn rule, unlearn everything to do with a ket, and so on??
# might not be that hard ...

  # what I'm calling pattern recognition.
  # just simm applied to relevant kets
  def pattern_recognition(self,pattern,op,t=0):                         # this function should be quite easy to parallelize in the future.
    if type(op) == ket:
      op = op.label[4:]
    result = superposition()                                            # later swap out superposition to fast_superposition
    for label in self.ket_rules_dict:                                   # though when I do so I will probably rename fast_sp to plain superposition.
      if op in self.ket_rules_dict[label]:
#        candidate_pattern = self.recall(op,label,True)                 # do we need active=True here? probably. OK. On a trial basis :)
        candidate_pattern = self.ket_rules_dict[label][op]              # currently is an exception if any patterns are stored rules! Fixed.
        if type(candidate_pattern) in [stored_rule, memoizing_rule]:
          candidate_pattern = candidate_pattern.activate(self,op,label) # do we really want to activate memoizing rules just by running similar-input[op]??
#        value = silent_simm(pattern,candidate_pattern)
        value = fast_simm(pattern,candidate_pattern)                    # see if this speeds things up!
        if value > t:                                                   # "value >= t" instead?
          result.data.append(ket(label,value))                          # "result += ket(label,value)" when swap in fast_superposition
    return result.coeff_sort()


# essentially identical in structure to pattern_recognition.
# I wonder if they should be merged into one more generic function?? Not for now, at least.
  def map_to_topic(self,e,op,t=0):
    if type(op) == ket:
      op = op.label[4:]
    result = superposition()                                            # later swap out superposition to fast_superposition
    for label in self.ket_rules_dict:
      if op in self.ket_rules_dict[label]:
#        frequency_list = self.recall(op,label,True)                    # do we need active=True here? probably. OK. On a trial basis :)
        frequency_list = self.ket_rules_dict[label][op]                 # this cut runtime in half!
        if type(frequency_list) in [stored_rule, memoizing_rule]:
          frequency_list = frequency_list.activate(self,op,label)       # do we really want to activate memoizing rules just by running find-topic[op]??       
        value = normed_frequency_class(e,frequency_list)
        if value > t:                                                   # "value >= t" instead?
          result.data.append(ket(label,value))                          # "result += ket(label,value)" when swap in fast_superposition
    return result.normalize(100).coeff_sort()


  # given an operator, return superposition of kets that support that operator:
  # slightly weird we have this here, and then a wrapper around it in the functions code, and this latter is what the processor uses.
  #
  # 22/2/2015 tweak: relevant_kets(self,"*") returns all known kets.
  def relevant_kets(self,op):
    result = superposition()
    if op == "*":
      for label in self.ket_rules_dict:
        result.add(label)
    else:
      for label in self.ket_rules_dict:
        if op in self.ket_rules_dict[label]:
          result.add(label)                                     # "result += ket(label)" when swap in fast_sp
    return result
    
  # 9/2/2016:
  # returns a superposition,with all coeffs 1, of all operators in a given context
  def supported_operators(self):
    result = superposition()
    for op in self.supported_operators_dict:
      result.add("op: " + op)
    return result
        

# 14/4/2015:
# given a ket, return matching lists of kets.
# eg: list-kets |movie: *>, should return all movies.
# list-kets |*> should return all KET's that have: OP KET => SP 
# Now, just need to test it!
# decided to rename and tweak, and call it starts-with.
# eg: starts-with |animal: > to list all animals.
# e is a ket.
  def starts_with(self,e):
    label = e.the_label()
#    if len(label) == 0:
#      return ket("",0)
#    if label[-1] != "*":
#      return e
#    label = label.rstrip("*").rstrip(": ")
    result = superposition()
    for trial_label in self.ket_rules_dict:
      if trial_label.startswith(label):
        result.data.append(ket(trial_label))  
    return result
      

# try and pretty print the sp data, instead of the BKO scheme.
# First, display the data for a single ket:
# Fred
# friends: Sam, George, Harry
#     age: age: 32
# parents: Mary, Richard
#
#
# NB: we renamed display_ket() to pretty_print_ket(). May want to swap that back.
  def pretty_print_ket(self,one):     # one is a ket
    label = one.label if type(one) == ket else one
    head = "  " + label + "\n"
    frame = ""
    op_list = list(self.ket_rules_dict[label])
    if len(op_list) != 0:
      max_len = max(len(op) for op in op_list)
      sep = ": "
      frame = "\n".join("  " + op.rjust(max_len) + sep + self.recall(op,label).readable_display() for op in op_list) + "\n"
    return head + frame

  def display_sp(self,sp):     # sp is a ket or sp
    return "\n".join(self.pretty_print_ket(x) for x in sp)

  def display_all(self):
    head = "  context: " + self.name + "\n\n"
    return head + "\n".join(self.pretty_print_ket(label) for label in self.ket_rules_dict)

# there are other possible "pretty print" too. Maybe write code for this eventually...
# eg: (this one is common for end of movie credits)
# Fred
# friends: Sam
#          George
#          Harry
#     age: age: 32
# parents: Mary
#          Richard


# I don't recall how this works!
# anyway, meant to convert context into frequency list.
  def to_freq_list(self):
    result = superposition()
    for label in self.ket_rules_dict:
      count_label = - 1                                # we subtract 1 because we don't want to count the supported-ops term.
      for op in self.ket_rules_dict[label]:
        count_label += 1
        rule = self.recall(op,label)                   # do we need "active=True" here? Probably not.
        if type(rule) in [ket, superposition, fast_superposition]:
          result += rule.apply_sigmoid(clean)          # this will auto-speed up once we swap in fast_superpositions.
      result += ket(label,count_label)
    return result.coeff_sort()

# 20/9/2015:
# shift: 
# load_sw(context,filename)
# save_sw(context,filename)
# save_sw_multi(context,filename)
# from the processor file to the new_context() class. Though they are still there, they are deprecated.
#
  def save(self,filename,exact_dump=True):             # we need to test this. Looks right.
    try:
      file = open(filename,'w')
      file.write(self.dump_universe(exact_dump))
      file.close()
    except:
      logger.info("failed to save: " + filename)

  def append_save(self,filename,exact_dump=True):             # we need to test this. Looks right.
    try:
      file = open(filename,'a')
      file.write(self.dump_universe(exact_dump,False))
      file.close()
    except:
      logger.info("failed to append save: " + filename)

  def multi_save(self,filename,exact_dump=True):             # we need to test this. I think it is working.  
    try:
      file = open(filename,'w')
      file.write(self.dump_multiverse(exact_dump))           # though here in new_context() dump_multiverse() is identical to dump_universe().  
      file.close()                                           # Maybe just set multi_save() as a wrapper around ordinary save, to make it clearer?
    except:
      logger.info("failed to multi save: " + filename)

  def load(self,filename):                                    # BUG: doesn't set the context properly. Not 100% sure why, yet. I think it is related to C.set("changed context") 
    try:                                                      # cool! I implemented new_context().set and seems to work now. 
      with open(filename,'r') as f:
        for line in f:
          if line.startswith("exit sw"):      # use "exit sw" as the code to stop processing a .sw file.
            return                               # maybe move try/except to around parse_rule_line() instead of entire file?
          #parse_rule_line(self,line)             # this is broken! bug found when loading fragment-document.sw fragments
          process_sw_file(self, line)             # this is broken! bug found when loading fragment-document.sw fragments
    except Exception as e:
      logger.info("failed to load: %s\nReason: %s" % (filename, e))

# 3/12/2015: new feature context.print_universe() and context.print_multiverse()
  def print_universe(self,exact_dump=False):
    print(self.dump_universe(exact_dump))

  def print_multiverse(self,exact_dump=False):
    print(self.dump_multiverse(exact_dump))
