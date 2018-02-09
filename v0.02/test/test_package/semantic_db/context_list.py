class context_list(object):
  def __init__(self,name):
    self.name = name
    c = new_context(name)
    self.data = [c]
    self.index = 0

  def set(self,name):                              # maybe write a set_index, where you specify index number, instead of context name
    match = False
    for k,context in enumerate(self.data):
      if context.name == name:
        self.index = k
        match = True
        break
    if not match:
      c = new_context(name)
      self.data.append(c)
      self.index = len(self.data) - 1

  def show_context_list(self):                      # maybe include a count of the number of kets known to that context
    text = "context list:\n"
    for k,context in enumerate(self.data):
      pre = "* " if k == self.index else "  "
      text += pre + context.name + " (" + str(len(context.ket_rules_dict)) + ")\n"
    return text

# new 12/2/2015:
# assumes k is an integer:
  def set_index(self,k):
    if k < 0 or k >= len(self.data):
      return False
    self.index = k
    return True
    
  def show_context_list_index(self):
    text = "context list:\n"
    for k,context in enumerate(self.data):
      pre = "* " if k == self.index else "  "
      text += " " + str(k) + ") " + pre + context.name + " (" + str(len(context.ket_rules_dict)) + ")\n"
    return text  

  def context_name(self):
    return self.data[self.index].context_name()

  def learn(self,op,label,rule,add_learn=False):
    self.data[self.index].learn(op,label,rule,add_learn)

  def add_learn(self,op,label,rule):
    self.data[self.index].add_learn(op,label,rule)

  def recall(self,op,label,active=False):
    return self.data[self.index].recall(op,label,active)

  def sp_learn(self,op,label,rule,add_learn=False):
    self.data[self.index].sp_learn(op,label,rule,add_learn)

  def sp_add_learn(self,op,label,rule):
    self.data[self.index].sp_add_learn(op,label,rule)

  def sp_recall(self,op,label,active=False):
    return self.data[self.index].sp_recall(op,label,active)

  def dump_ket_rules(self,label,exact=False):
    return self.data[self.index].dump_ket_rules(label,exact)

  def dump_multiple_ket_rules(self,label,exact=False):                  # is this really a label here, or a sp?
    return self.data[self.index].dump_multiple_ket_rules(label,exact)

  def display_sp(self,sp):
    return self.data[self.index].display_sp(sp)

  def display_all(self):
    return self.data[self.index].display_all()


  def to_freq_list(self):
    return self.data[self.index].to_freq_list()    # later rewrite so it returns results from all context's.      

# make the all context-to-freq it's own function.
  def multiverse_to_freq_list(self):
    result = superposition()
    for context in self.data:
      result += context.to_freq_list()
    return result
    

  def dump_universe(self,exact=False):
    return self.data[self.index].dump_universe(exact)

  def create_universe_inverse(self):
    self.data[self.index].create_universe_inverse()
    
  def create_multiverse_inverse(self):
    for context in self.data:
      context.create_universe_inverse()

  def create_inverse_op(self,op):
    self.data[self.index].create_inverse_op(op)
      
  def pattern_recognition(self,pattern,op,t=0):
    return self.data[self.index].pattern_recognition(pattern,op,t)

# currently unimplemented. It was dropped from the recent new_context() class work. Maybe re-instate it?
#  def verbose_pattern_recognition(self,pattern,op="pattern"):
#    return self.data[self.index].verbose_pattern_recognition(pattern,op)
  
  def map_to_topic(self,e,op,t=0):
    return self.data[self.index].map_to_topic(e,op,t)   
 
  def relevant_kets(self,op):
    return self.data[self.index].relevant_kets(op)

  # 9/2/2016
  def supported_operators(self):
    return self.data[self.index].supported_operators()
    
    
#  def list_kets(self,e):
#    return self.data[self.index].list_kets(e)    
# renames to starts-with
  def starts_with(self,e):
    return self.data[self.index].starts_with(e)    
         
  
  def global_recall(self,op,label):              # where do we even use this?
    result = superposition()                     # does it need active=True too?
    for context in self.data:
      result += context.recall(op,label)
    return result

  def dump_multiverse(self,exact=False):
    result = ""
    for context in self.data:
      result += context.dump_universe(exact)
    return result

  def save(self,filename,exact_dump=True):
    return self.data[self.index].save(filename,exact_dump)

  def append_save(self,filename,exact_dump=True):
    return self.data[self.index].append_save(filename,exact_dump)

  def multi_save(self,filename,exact_dump=True):             # we need to test this. I think it is working.  
    try:
      file = open(filename,'w')
      file.write(self.dump_multiverse(exact_dump))
      file.close()
    except:
      logger.info("failed to multi save: " + filename)

  def load(self,filename):                                    # BUG: doesn't set the context properly. Not 100% sure why, yet. I think it is related to C.set("changed context") 
    try:                                                      # Well, here in context_list() it works just fine! C.load("sw-examples/fib-play.sw"); print(C.dump_multiverse())
      with open(filename,'r') as f:
        for line in f:
          if line.startswith("exit sw"):      # use "exit sw" as the code to stop processing a .sw file.
            return
          #parse_rule_line(self,line)             # this is broken! bug found when loading fragment-document.sw fragments
          process_sw_file(self, line)             # later maybe process entire file at once. Not sure which method is faster.
    except Exception as e:
      logger.info("failed to load: " + filename)
      logger.info('reason: %s' % e)

# 3/12/2015: new feature context.print_universe() and context.print_multiverse()
  def print_universe(self,exact_dump=False):
    print(self.data[self.index].dump_universe(exact_dump))

  def print_multiverse(self,exact_dump=False):
    print(self.dump_multiverse(exact_dump))
