from collections import OrderedDict
#from semantic_db.ket import ket


# a superposition is a collection of float,string pairs, displayed using ket notation. 
class superposition(object):
  def __init__(self,first='',value=1):
#    self.dict = {}                                      # faster and cheaper than OrderedDict() if you don't need to preserve order
    self.dict = OrderedDict()
    if first is not '':
      if type(first) in [str]:                           # this is ugly! Mixing and matching string vs superposition? Maybe we should keep a ket class?? Also, ket is quicker to type!
        self.dict[first] = value                         # r1 = superposition('fred')
      elif type(first) in [ket, superposition]:          # r2 = superposition('fred',3.2)
        for key,value in first.items():                  # r4 = superposition(ket('fred'))
          if key != '':                                  # r5 = superposition(another-sp)
            self.dict[key] = value                         

  def __str__(self):
    if len(self.dict) == 0:
      return '|>'
    list_of_kets = []
    for key,value in self.dict.items():
      if value == 1:
        s = "|%s>" % key
      else:
        s = "%s|%s>" % (float_to_int(value), key)
      list_of_kets.append(s)
    return " + ".join(list_of_kets)

  def __iter__(self):
    for key,value in self.dict.items():
      yield ket(key, value)

  def items(self):
    for key,value in self.dict.items():
      yield key, value

  def __len__(self):
    return len(self.dict)

  def __getattr__(self, name):
    if name == 'label':
      if len(self.dict) == 0:
        return ""
      for key,value in self.dict.items():                      # NB. For a sp with more than 1 element, sp.label and sp.value returns label and value of the first element only.
        return key
    if name == 'value':
      if len(self.dict) == 0:
        return ""
      for key,value in self.dict.items():
        return value
    else:
      raise AttributeError
    

  def __truediv__(self, divisor):
    if type(divisor) in [int, float]:
      r = superposition()
      for key,value in self.dict.items():
        r.dict[key] = value/divisor
      return r
    else:
      return NotImplemented

  def __add__(self, sp):
    if type(sp) in [ket, superposition]:
      r = copy.deepcopy(self)
      for key,value in sp.items():
        r.add(key, value)
      return r
    if type(sp) in [sequence]:
      r = sequence(self)
      r.add_seq(sp)
      return r 
    else:
      return NotImplemented

  def __sub__(self, sp):
    if type(sp) in [ket, superposition]:
      r = copy.deepcopy(self)
      for key,value in sp.items():
        r.add(key, - value)
      return r
    else:
      return NotImplemented

  def add(self,s, value=1):          # what about adding a superposition? r.add(some-sp). Or r.add_sp(some-sp)? Yeah, and r.add_sp(some-ket)
    if s == '':                     # |x> + 3.72|> == |x>
      return
    if s in self.dict:
      self.dict[s] += float(value)
    else:
      self.dict[s] = float(value)

  def sub(self, s, value=1 ):
    if s == '':
      return
    if s in self.dict:
      self.dict[s] -= float(value)
    else:
      self.dict[s] = - float(value)

  def add_sp(self, sp):                      # handles r.add_sp(some-ket) and r.add_sp(some-sp). Breaks if sp is a stored_rule or a memoizing_rule. How fix?
    for key,value in sp.items():
      self.add(key, value)
      
  def sub_sp(self, sp):
    for key,value in sp.items():
      self.sub(key, value)

  def max_add(self, str, value = 1):
    if str == '':
      return
    if str in self.dict:
      self.dict[str] = max(self.dict[str], float(value))
    else:
      self.dict[str] = float(value)
      
  def max_add_sp(self, sp):
    for key, value in sp.items():
      self.max_add(key, value)

  def seq_add(self, x):                                        # this probably doesn't work the way you want either. y = sp1.seq_add(sp2) works. sp1.seq_add(sp2) does not.
    r = sequence(self) + x
    return r

  def merge_sp(self, x, space=''):                                      # |a> + 2.1|b> + 3|c> _ 7.9|d> + |e> + |f> == |a> + 2.1|b> + |cd> + |e> + |f>  
    if len(self) == 0:
      for key, value in x.items():
        self.add(key, value)
      return
    head = superposition()                                 # is there a better way to do this??
    tail = superposition()
    for k, (key, value) in enumerate(self.items()):
      if k != len(self.dict) - 1:
        head.add(key, value)
      else:
        tail.add(key, value)
    x_head = superposition()
    x_tail = superposition()
    for k, (key, value) in enumerate(x.items()):
      if k == 0:
        x_head.add(key, value)
      else:
        x_tail.add(key, value)
#    result = head + ket(tail.label + x_head.label, tail.value) + x_tail
    result = head + ket(tail.label + space + x_head.label, x_head.value * tail.value) + x_tail
    self.dict = result.dict
    


#  def clean_add(self,one):                                    # I don't know where this is used. Maybe remove since it duplicates add_sp().
#    for key,value in one.items():
#      self.add(key,value)      

  def old_display(self):
    list_of_pairs = []
    for key,value in self.dict.items():
      if value == 1.0:
        s = "%s" % key
      else:
        s = "%s %s" % (float_to_int(value), key)
      list_of_pairs.append(s)
    return ",\t".join(list_of_pairs)
    
  def display(self,exact=False):
    if len(self.dict) == 0:
      return '|>'
    return " + ".join(x.display(exact) for x in self)     # 1) get ket class to do the display. 2) need something better if we mix + - _ .  

  def readable_display(self):
    if len(self.dict) == 0:
      return ""
    return ", ".join(x.readable_display() for x in self)
       
  def pair(self):                               # if the dict is longer than 1 elt, this returns a random pair
    for key,value in self.dict.items():         # presuming not using an OrderedDict
      return key, value

  def pick(self, n):                            # randomly pick and return n elements from the superposition
    r = superposition()
    for key in random.sample(list(self.dict), n):
      value = self.dict[key]
      r.add(key,value)
    return r

  def pick_elt(self):
    if len(self) == 0:
      return ket()
    key = random.choice(list(self.dict))
    value = self.dict[key]
    return ket(key, value)

  def weighted_pick_elt(self):                    # quick test in the console, looks to be roughly right.
    if len(self) == 0:
      return ket()
    total = sum(x.value for x in self)
    r = random.uniform(0,total)
    upto = 0
    for x in self:
      w = x.value
      if upto + w > r:
        return x
      upto += w
    assert False, "Shouldn't get here"    
    

  def get_value(self,str):                      # maybe convert to  __getitem__
    if str in self.dict:
      return self.dict[str]
    else:
      return 0                                 # maybe return None?

#  def the_value(self):                         # if the dict is longer than 1 elt, this returns a random value
#    for key,value in self.dict.items():
#      return value
#    return 0

  def rescale(self,t=1):
    if len(self.dict) == 0:
      return superposition()
    the_max = max(value for key,value in self.dict.items())
    result = superposition()
    if the_max > 0:
      for key,value in self.dict.items():
        result.dict[key] = t*self.dict[key]/the_max
    return result

  def normalize(self,t=1):
    if len(self.dict) == 0:
      return superposition()
    the_sum = sum(value for key,value in self.dict.items())
    result = superposition()
    if the_sum > 0:
      for key,value in self.dict.items():
        result.dict[key] = t*self.dict[key]/the_sum
    return result

  def softmax(self):
    if len(self) == 0:
      return ket()
    r = superposition()
    the_sum = sum(math.exp(value) for (key, value) in self.dict.items())
    for key, value in self.dict.items():
      r.add(key, math.exp(value)/the_sum)
    return r

  def multiply(self,t):
    r = superposition()
    for key,value in self.dict.items():
      r.add(key, value*t)
    return r
    return result

# add noise to the ket/sp in range [0,t]
  def absolute_noise(self,t):
    r = superposition()
    for key, value in self.dict.items():
      r.add(key, value + random.uniform(0,t))
    return r
        
# add noise to ket/sp in range [0,t*max_coeff]
  def relative_noise(self,t):
    max_coeff = self.find_max_coeff()
    r = superposition()
    for key, value in self.dict.items():
      r.add(key, value + random.uniform(0, t * max_coeff))
    return r
       

  def coeff_sort(self):                                                           # Nope. Doesn't seem to work.
    r = superposition()
    for key,value in sorted(self.dict.items(), key=lambda x: x[1], reverse=True): # 3|a> + 2|b> + |c> or |c> + 2|b> + 3|c>?
      r.add(key,value)
    return r
    
  def ket_sort(self):
    r = superposition()
    for key,value in natural_sorted(self.dict.items(), key=lambda x: x[0].lower()):
      r.add(key,value)
    return r
    
  def reverse(self):
    r = superposition()
    r.dict = OrderedDict(reversed(list(self.dict.items())))
    return r
    
  def shuffle(self):
    r = superposition()
    items = list(self.dict.items())
    random.shuffle(items)
    r.dict = OrderedDict(items)
    return r

  def select_top(self,k):
    r = superposition()
    for i,(key,value) in enumerate(self.dict.items()):
      r.add(key,value)
      if i + 1 >= k:
        break
    return r

# NB: we use: 1 <= k <= len, not 0 <= k < len to access ket objects.
# NB: though we still use -1 for the last element, -2 for the second last element, etc.
  def select_elt(self,k):
    if k >= 1 and k <= len(self.dict):
      label, value = list(self.dict.items())[k-1]      # is there a better way to do this! Mapping entire sp to list, just to keep 1 element!!
      return ket(label, value)                         # perhaps, https://stackoverflow.com/questions/10058140/accessing-items-in-a-ordereddict 
    elif k < 0:                                        # import itertools
      label, value = list(self.dict.items())[k]        # next(itertools.islice(d.values(), 0, 1))
      return ket(label, value)                         # next(itertools.islice(d.values(), 1, 2))
    else:
      return ket("",0)

  def select_range(self,a,b):
    a = max(1,a) - 1
    b = min(b,len(self.dict))
    r = superposition()
    for label, value in list(self.dict.items())[a:b]:
      r.add(label, value)
    return r

  def top(self,k):
    if k == 0:
      return ket()
    value = self.coeff_sort().select_range(k,k).value
    return self.drop_below(value)      

  def delete_elt(self,k):
    r = superposition()
    for i, (key, value) in enumerate(self.items()):
      if i != k - 1:
        r.add(key, value)
    return r

  def delete_elt_v2(self, k):
    r = copy.deepcopy(self)
    label, value = list(self.dict.items())[k-1]
    r.add(label, -value)                              # return r.drop() ??
    return r

  def delete_elt_v3(self, k):
    label, value = list(self.dict.items())[k-1]
    r = copy.deepcopy(self)
    del r.dict[label]
    return r

  def find_index(self,one):
    label = one.label if type(one) == ket else one
    for k,(key,value) in enumerate(self.dict.items()):
      if key == label:
        return k + 1
    return 0

  def find_value(self,one):
    label = one.label if type(one) == ket else one
    if label in self.dict:
      return self.dict[label]
    return 0

  def find_max_coeff(self):
    if len(self) == 0:
      return 0
    return max(x.value for x in self)

  def find_min_coeff(self):
    if len(self) == 0:
      return 0
    return min(x.value for x in self)

  def number_find_max_coeff(self):
    if len(self) == 0:
      value = 0
    else:
      value = max(x.value for x in self)
    return ket("number: " + str(value))

  def number_find_min_coeff(self):
    if len(self) == 0:
      value = 0
    else:
      value = min(x.value for x in self)
    return ket("number: " + str(value))


  def find_max_elt(self):
    if len(self) == 0:
      return ket()
    the_max = max(x.value for x in self)
    for key, value in self.dict.items():
      if value == the_max:
        return ket(key, value)
    logger.warning("I shouldn't be here in find_max_elt.")

  def find_min_elt(self):
    if len(self) == 0:
      return ket()
    the_min = min(x.value for x in self)
    for key, value in self.dict.items():
      if value == the_min:
        return ket(key, value)
    logger.warning("I shouldn't be here in find_min_elt.")

  def find_max(self):
    if len(self) == 0:
      return superposition()
    the_max = max(x.value for x in self)
    r = superposition()
    for key, value in self.dict.items():
      if value == the_max:
        r.add(key, value)
    return r

  def find_min(self):
    if len(self) == 0:
      return superposition()
    the_min = min(x.value for x in self)
    r = superposition()
    for key, value in self.dict.items():
      if value == the_min:
        r.add(key, value)
    return r

  def delete_ket(self,one):        # do we need a delete_sp() too?
    label = one.label if type(one) == ket else one
    r = copy.deepcopy(self)
    del r.dict[label]
    return r
    

  def drop(self):
    r = superposition()
    for key, value in self.dict.items():
      if value > 0:
        r.add(key, value)
    return r

  def drop_below(self,t):
    r = superposition()
    for key, value in self.dict.items():
      if value >= t:
        r.add(key, value)
    return r

  def drop_above(self,t):
    r = superposition()
    for key, value in self.dict.items():
      if value <= t:
        r.add(key, value)
    return r

  def count(self):
    return len(self)

  def count_sum(self):
    return sum(x.value for x in self)

  def number_count(self):
    result = len(self)
    return ket("number: " + str(result))

  def number_count_sum(self):  
    result = sum(x.value for x in self)
    return ket("number: " + float_to_int(result))

  def product(self):                          # need to put these in ket now.
    r = 1
    for x in self:
      r *= x.value
    return r

  def number_product(self):
    r = 1
    for x in self:
      r *= x.value
    return ket("number: " + str(r))
    
  
#  def reweight(self, weights):
#    r = superposition()
#    for k, (key, value) in enumerate(self.dict.items()):
#      r.add(key, value * weights[k] )
#    return r

  def old_apply_fn(self,fn,t1=None,t2=None):
    result = superposition()
    for x in self:
      if t1 == None:
        r = fn(x)
      elif t2 == None:
        r = fn(x,t1)
      else:
        r = fn(x,t1,t2)
      result += r
    return result

# define a function that maps sp -> sp, instead of ket -> ket/sp.
# now we need to 1) add it to ket class, and 2) wire it into the processor.
# 5/2/2015: starting to wonder if there is a tidier way to do this!!
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

# need to check this works!
# 27/6/2014: hrmm... so let me get this right, a sp_fn applies to the applied superposition.
# and naked_fn ignores any passed in superpositions.
  def old_apply_naked_fn(self,fn,t1=None,t2=None,t3=None):
    if t1 == None:
      return fn()
    elif t2 == None:
      return fn(t1)
    elif t3 == None:
      return fn(t1,t2)
    else:
      return fn(t1,t2,t3)

  def apply_fn(self, fn, *args):
    r = superposition()
    for x in self:
      r += fn(x, *args)
    return r
    
  def apply_sp_fn(self, fn, *args):
    return fn(self, *args)
    
  def apply_naked_fn(self, fn, *args):
    return fn(*args)             
    
  def old_apply_op(self,context,op):                                      # bugs out when rule is a sequence, which is now most of the time, once parser is finished.
    logger.debug("inside sp apply_op")
    r = context.sp_recall(op, [self] ,True)  # op (*) has higher precedence than op |*>
    if len(r) == 0:
      r = superposition()
      if len(self) == 0:
        rule = context.recall(op, '', True)                           # op|> can return something other than |>. At least for now.
        r.add_sp(rule)
      else:
        for x in self:
          rule = context.recall(op, x, True)                          # should this be apply_op() instead? Nah, don't think so.
          r.add_sp(rule)
    logger.debug("sp apply_op: " + str(r))
    return r

  def apply_op(self,context,op):                                      # bugs out when rule is a sequence, which is now most of the time, once parser is finished.
    logger.debug("inside sp apply_op")
    r = context.sp_recall(op, [self] ,True)                           # op (*) has higher precedence than op |*>
    if len(r) == 0:
      r = sequence([])
      if len(self) == 0:
        rule = context.recall(op, '', True)                           # op|> can return something other than |>. At least for now.
        r.add_seq(rule)
      else:
        for x in self:
          rule = context.recall(op, x, True)                          # should this be apply_op() instead? Nah, don't think so.
          r.add_seq(rule)
    logger.debug("sp apply_op: " + str(r))
    return r

  def apply_sigmoid(self, sigmoid, t1=None, t2=None):                    # use *args notation.
    r = superposition()
    if t1 == None:
      for key,value in self.dict.items():
        value = sigmoid(value)
        r.add(key,value)
    elif t2 == None:
      for key,value in self.dict.items():
        value = sigmoid(value, t1)
        r.add(key,value)
    else:
      for key,value in self.dict.items():
        value = sigmoid(value, t1, t2)
        r.add(key,value)
    return r

  def is_not_empty(self):
    if len(self) == 0:
      return ket('no')
    return ket('yes')
           
  def activate(self,context=None,op=None,self_label=None):
    return self


