# code for the yet to be added stored function rules:
# We have a stored learn rule:
# op |x> #=> foo |y> + bah |z> + some-action
# This stores the rule: "foo |y> + bah |z> + some-action"
# without processing it at learn time.
# Then it activates later when we do: op |x>  (where |x> is self_object)
# However, we don't want it to activate when we do a dump rule (at least I think so)
# Going to take some work to implement, but let's start with a class:
# Baring any bugs, I think it is working!
class stored_rule(object):        
  def __init__(self,rule):           # rule should be a string.
    self.rule = rule
    logger.debug("in stored_rule class: just stored: "  + rule)
  
  def type(self):                    # not 100% we need this, but no harm in putting it in anyway.
    return "stored rule"

  def display(self,exact=False):     # we don't need exact, but we do need to handle display with 1 parameter.
    return self.rule
    
  def readable_display(self):
    return "# " + self.rule
  
  def __str__(self):
    return self.display()
    
  def __len__(self):                # not sure what to return. so 1 sounds good for now.
    return 1    

  # where currently self_object is a string. Breaks even with ket, let alone sp.
  # eventually I want support for all three cases.    
  def activate(self,context,op,self_label=None):                         
    try:
      return extract_compound_superposition(context,self.rule,self_label)[0] # how does return work in try/except?
    except:                                                                   # works fine.
      logger.warning("FYI: except in stored_rule")
      return superposition()  
  
  def multiply(self,value):
    return self                                    # will probably do a better job of multiplication later. Is it even used?

# 14/1/2016:    
  def add(self,value):
    return self                                    # will probably do a better job of addition later. Is it even used?
  
  def add_sp(self, sp):                            # just for now. Tweak later.
    if type(sp) in [stored_rule]:
      self.rule += ' + ' + sp.rule
    if type(sp) in [ket, superposition]:
      self.rule += ' + ' + str(sp)  
