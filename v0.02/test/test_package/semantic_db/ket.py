class ket(object):
  def __init__(self,label='',value=1):
    self.label = label
    self.value = float(value)
#    self.value = int(value)     # sometimes useful to restrict to integers. eg, for smaller memory foot-print.

  def __str__(self):
    return self.display()
    
  def __len__(self):
    if self.label == '':                                  # returns 0 for |>.
      return 0
    return 1

  def __eq__(self,other):
    return self.label == other.label and self.value == other.value

  def __iter__(self):
    yield ket(self.label, self.value)

  def items(self):
    yield self.label, self.value

  def display(self,exact=False):
    if self.value == 1:
      s = "|%s>" % self.label      
    elif exact:                                           # tweaked for exact display, so dump to file and load again don't accidentally zero coeffs.
      s = "%s|%s>" % (self.value, self.label)
    else:
      s = "%s|%s>" % (float_to_int(self.value), self.label)      
    return s

  def long_display(self):                     # where is this used??
    if self.value == 1:
      return self.label
    else:
      return "%.3f    %s" % (self.value, self.label)
    
  def readable_display(self):                 # where is this used??
    if self.label == '':
      return ""
    if self.value == 1:
      return self.label
    else:
      if self.value.is_integer():
        return "{0:.0f} {1}".format(self.value,self.label) # not consistant style with display() and long_display().FIX.
      return "{0:.2f} {1}".format(self.value,self.label)      
        
  def __add__(self,x):
    return superposition(self) + x

  def __sub__(self,x):
    return superposition(self) - x
    
  def merge(self, x):                                      # |a> + 2.1|b> + 3|c> _ 7.9|d> + |e> + |f> == |a> + 2.1|b> + |cd> + |e> + |f>  
    label = self.label + x.select_elt(1).label             # assumes select_elt(k) returns a single ket, even for sp class.
    return ket(label)    

  def seq_add(self, x):                                    # ket('x').seq_merge(ket('y')) == |x> . |y>
    r = sequence(self) + x
    return r

  def get_value(self, s):
    if s == self.label:
      return self.value
    else:
      return 0


# deleted clean_add(self,x) and self_add(self,x). I don't know what they are meant to do, or where they are used. In new_context, I think ....  
# Add back in later if they turn out to be important!
# I still want to delete them, but left them in for now.  
#  def clean_add(self,x):
#    r = superposition(self)
#    r.clean_add(x)      
#    return r
#
#  def self_add(self,x):                                        # self_add(), add(), add_sp(), sub(), sub_sp() don't work the way you want them to! FIX! Or, delete.
##    logger.debug("inside ket self_add")
##    logger.debug("self: " + str(self))
##    logger.debug("x: " + str(x))
#    r = superposition(self) + x 
#    return r

#  def add(self, label, value=1):
#    r = superposition(self)
#    r.add(label, value)
#    return r
    
#  def add_sp(self, sp):
#    r = superposition(self)
#    r.add_sp(sp)
#    return r

#  def sub(self, label, value = 1):
#    r = superposition(self)
#    r.sub(label, value)
    
#  def sub_sp(self, sp):
#    r = superposition(self)
#    r.sub_sp(sp)
#    return r
      
  def old_apply_fn(self,fn,t1=None,t2=None):                   # should be able to improve this, so we don't need the if statements!
    if t1 == None:                                         # maybe this: https://stackoverflow.com/questions/1769403/understanding-kwargs-in-python
      r = fn(self)
    elif t2 == None:
      r = fn(self,t1)
    else:
      r = fn(self,t1,t2)
    return superposition(r)

  def old_apply_sp_fn(self,fn,t1=None,t2=None,t3=None,t4=None):
    if t1 == None:
      return fn(self)
    elif t2 == None:
      return fn(self,t1)
    elif t3 == None:
      return fn(self,t1,t2)
    elif t4 == None:
      return fn(self,t1,t2,t3)
    else:
      return fn(self,t1,t2,t3,t4)

  def old_apply_naked_fn(self,fn,t1=None,t2=None,t3=None):                  # TODO, test later.
    if t1 == None:
      return fn()
    elif t2 == None:
      return fn(t1)
    elif t3 == None:
      return fn(t1,t2)
    else:
      return fn(t1,t2,t3)

  def apply_fn(self, fn, *args):
    r = fn(self, *args)
    return superposition(r)
    
  def apply_sp_fn(self, fn, *args):
    return fn(self, *args)
    
  def apply_naked_fn(self, fn, *args):
    return fn(*args)             

# sp_recall(self,op,sp,active=False)

  def apply_op(self,context,op):                                        # TODO? Maybe later, make it work with function operators too, rather than just literal operators?
    logger.debug("inside ket apply_op")
    r = context.sp_recall(op, [self] ,True)       # this is broken! Not sure why, yet. I think I fixed it.  
    logger.debug("inside ket apply_op, sp: " + str(r))
    if len(r) == 0:
      r = context.recall(op,self,True)  # see much later in the code for definition of recall.
    logger.debug("leaving ket apply_op")
    return r

  def select_elt(self,k):
    if k != 1 and k != -1:
      return ket()
    else:
      return ket(self.label, self.value)
          
# 5/2/2015: eg: without this: select[1,5] "" |bah> bugs out if "" |bah> is not defined.
  def select_range(self,a,b):      
    if a <= 1 <= b:
      return ket(self.label, self.value)
    return ket()
    
# 24/9/2015:
# top[5] SP, should return the top 5 kets in the superposition, without changing the order
# if more than 5 kets have the same value, return all those that match. If you want exactly k matches, we need to do something a little different.
#  def top(self,k):
#    if k == 0:
#      return ket("",0)
#    value = self.coeff_sort().select_range(k,k).the_value()
#    return self.drop_below(value)      
# bah! Makes no sense for the ket version.
# Here is fixed version:
  def top(self,k):
    if k == 0:
      return ket()
    return ket(self.label,self.value)

  def index_split(self,k):                      # OK. Now need to test it. Maybe improve for k other than {1,-1}.
    if k == 1:                                  # do we need it anymore? Isn't it just in the parser to help with |x> _ |y>??
      return ket(self.label,self.value), ket()
    if k == -1:
      return ket(), ket(self.label,self.value) 
  
  def pick_elt(self):
    return ket(self.label,self.value)

  def weighted_pick_elt(self):
    return ket(self.label,self.value)      

#  def find_index(self,one):
#    label = one.label if type(one) == ket else one
#    if self.label == label:
#      return 1
#    return 0
#
#  def find_value(self,one):
#    label = one.label if type(one) == ket else one
#    if self.label == label:
#      return self.value
#    return 0
#
#  def find_max_coeff(self):
#    return self.value
#
#  def find_min_coeff(self):
#    return self.value

  def normalize(self,t=1):
    r = ket(self.label, self.value)
    if r.value > 0:
      r.value = t
    return r

  def softmax(self):
    return ket(self.label,1)

  def rescale(self,t=1):
    r = ket(self.label, self.value) 
    if r.value > 0:
      r.value = t
    return r

  def multiply(self,t):
    return ket(self.label, self.value*t)
    
#  def add(self,t):                                        # Nope. Deleted for now. Conflicts with x.add(key,value)
#    return ket(self.label,self.value + t)
    

# 6/1/2015: hrmm... maybe abs, absolute_noise, and relative_noise should be sigmoids!
# newly added 2/4/2014:
# yeah. moved to sigmoid (4/5/2015) Hope we don't break anything!
#  def abs(self):
#    return ket(self.label,abs(self.value))
    
# newly added 7/4/2014:
# add noise to the ket/sp in range [0,t]
  def absolute_noise(self,t):
    return ket(self.label,self.value + random.uniform(0,t))  # hrmm.. so noise is additive only?
  
# newly added 7/4/2014:
# add noise to ket/sp in range [0,t*max_coeff]
  def relative_noise(self,t):
    max_coeff = self.value
    return ket(self.label,self.value + random.uniform(0,t*max_coeff))            
    
  def coeff_sort(self):
    return ket(self.label,self.value)

  def ket_sort(self):
    return ket(self.label,self.value)

#  def find_max_coeff(self):                                 # where are these used? find-topic??
#    return self.value
#
#  def find_min_coeff(self):
#    return self.value

  def number_find_max_coeff(self):
    return ket("number: " + str(self.value))

  def number_find_min_coeff(self):
    return ket("number: " + str(self.value))
    
#  def old_discrimination(self):
#    return ket(" ",self.value)
#
#  def discrimination(self):
#    if self.label == "":
#      return ket("discrimination",0)
#    return ket("discrimination")
    

# 24/2/2015:
# implements discrim-drop[t] SP
# ie: if discrim is > t return |>, else return value.
# don't know how I want this to work! 
#  def discrimination_drop(self,t):
#    return ket(self.label,self.value)    
    


# sigmoids apply to the values of kets, and leave ket labels alone.
  def apply_sigmoid(self,sigmoid,t1=None,t2=None):
    r = ket(self.label, self.value)
    if t1 == None:
      r.value = sigmoid(r.value)
    elif t2 == None:
      r.value = sigmoid(r.value,t1)
    else:
      r.value = sigmoid(r.value,t1,t2)
    return r

# do we need a superposition version of this? Probably...
# implements: similar[op] |x>
  def old_similar(self,context,op):              # should I use .apply_op(context,op,True)? 
    f = self.apply_op(context,op)            # use apply_op or context.recall() directly?
    print("f:",f.display())                  # in light of active=True thing, apply_op() seems the right answer.
#    return context.pattern_recognition(f,op) # yeah, but what about in pat_rec?
    return context.pattern_recognition(f,op).delete_ket(self)    # we delete self, ie |x>, from the result, since it is always a 100% match anyway.

# 23/2/2015:
# implements: similar[op1,op2] |x>
  def similar(self,context,ops):              
    try:
      op1,op2 = ops.split(',')
    except:
      op1 = ops
      op2 = ops 
    f = self.apply_op(context,op1)            
    return context.pattern_recognition(f,op2).delete_ket(self)    # we delete self, ie |x>, from the result, since it is always a 100% match anyway.
    
# 23/2/2015: 
# implements: self-similar[op1,op2] |x>
# ie don't delete |x>
  def self_similar(self,context,ops):
    try:
      op1,op2 = ops.split(',')
    except:
      op1 = ops
      op2 = ops 
    f = self.apply_op(context,op1)            
    return context.pattern_recognition(f,op2) 
    
# 14/1/2016: we need to test it though.
# implements: similar-input[op] |x>                                  # I don't think this makes much sense, in light of: similar-input[op] some |superposition>  
#  def similar_input(self,context,op):              
#    return context.pattern_recognition(self,op).delete_ket(self)    # we delete self, ie |x>, from the result, since it is always a 100% match anyway.
    
# 14/1/2016: 
# implements: self-similar-input[op] |x>
# ie don't delete |x>
#  def self_similar_input(self,context,op):                          # NB: the name change
  def similar_input(self,context,op):
    return context.pattern_recognition(self,op) 


# implements: find-topic[op] |x> 
  def find_topic(self,context,op):           
    return context.map_to_topic(self,op)

# 2/4/2015: intn-find-topic[op] |a b c>
# this goes some way to a search engine.
# currently we don't have a superposition version of this. Not sure it is needed.
#
  def intn_find_topic(self,context,op):
    words = self.label.lower().split()
    logger.debug("words: " + words)
    if len(words) == 0:
      return ket("",0)
    results = [context.map_to_topic(ket(x),op) for x in words]
    logger.debug("len results: " + str(len(results)))
    if len(results) == 0:                    # this should never be true!
      return ket("",0)
    r = results[0]
    for sp in results:
      logger.debug("sp: " + str(sp))
      r = intersection(r,sp)
    return r.normalize(100).coeff_sort()
         
  def count(self):                                                # duplicates len(x), but keep it anyway, because of its brother count_sum().
    if self.label == "":
      return 0
    return 1

  def count_sum(self):
    return self.value

  def number_count(self):
    if self.label == "":
      return ket("number: 0")
    return ket("number: 1")

  def number_count_sum(self):           
    return ket("number: " + float_to_int(self.value))

  def drop(self):
    if self.value > 0:
      return ket(self.label, self.value)
    else:
      return ket()

  def drop_below(self,t):
    if self.value >= t:
      return ket(self.label,self.value)
    else:
      return ket()
  
  def drop_above(self,t):
    if self.value <= t:
      return ket(self.label,self.value)
    else:
      return ket()
      
  def drop_zero(self):                                        # don't know where we use this.
    if abs(x.value) > 0.0001:
      return ket(self.label,self.value)
    else: 
      return ket("",0)
    
# I'm using this in show_range, arithemetic etc, so can feed in sp or ket.
# deprecated. Now use x.the_label()
# usage: X.ket()
# the other half is in superposition.
#  def ket(self):
#    return ket(self.label,self.value)
#
#  def the_label(self):
#    return self.label
#  
#  def the_value(self):
#    return self.value

  def is_not_empty(self):
    if self.label == "":
      return ket("no")
    return ket("yes")

  def activate(self,context=None,op=None,self_label=None):
    return ket(self.label,self.value)            # not sure if we need this:
    #return self                                 # or if this will suffice.
