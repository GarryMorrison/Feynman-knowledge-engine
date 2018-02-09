# 13/2/2015:
# essentially a copy of stored_rule
# idea is:
# op |x> !=> some-rule
# on activation, we store: op |x> => some-rule
# eg, fib |*> !=> arithmetic( fib n-1 |_self>, |+>, fib n-2 |_self>)
# so no need to manually do:
# fib |10> => fib |10>
# fib |11> => fib |11> 
# and so on. It is done for us!
# At least that is the idea, not sure if I can get it to work.
# yup! works great. eg fib |100> is fast now! 
#     
class memoizing_rule(object):        
  def __init__(self,rule):           # rule should be a string.
    self.rule = rule
    logger.debug("in memoizing_rule class: just stored: " + rule)
  
  def type(self):                    # not 100% we need this, but no harm in putting it in anyway.
    return "memoizing stored rule"

  def display(self,exact=False):     # we don't need exact, but we do need to handle display with 1 parameter.
    return self.rule
    
  def readable_display(self):
    return "! " + self.rule
  
  def __str__(self):
    return self.display()
    
  def __len__(self):                # not sure what to return. so 1 sounds good for now.
    return 1    

  # where currently self_object is a string. Breaks even with ket, let alone sp.
  # eventually I want support for all three cases.    
  def activate(self,context,op,self_label):                         
    try:
      resulting_rule = extract_compound_superposition(context,self.rule,self_label)[0] # how does return work in try/except?
      context.learn(op,self_label,resulting_rule)
      return resulting_rule
    except:                                                                   # works fine.
      logger.warning("FYI: except in stored_rule")
      return superposition()  
  
  def multiply(self,value):
    return self                                    # will probably do a better job of multiplication later.

# 14/1/2016:
  def add(self,value):
    return self                                    # will probably do a better job of addition later.
