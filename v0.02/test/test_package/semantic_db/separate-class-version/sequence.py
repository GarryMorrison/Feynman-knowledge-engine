import copy
from semantic_db.ket import ket
from semantic_db.superposition import superposition


# sequence class. Has methods we need to chomp out that are not relevant here. TODO.
class sequence(object):
  def __init__(self, data = []):
#  def __init__(self, name='', data = []):
#    self.name = name
    #print('sequence data: %s' % data)
    if type(data) in [list]:
      self.data = data                            # copy.deepcopy(data)??
    if type(data) in [sequence]:
      self.data = copy.deepcopy(data.data)
    if type(data) in [ket]:
      self.data = [ket() + data]                  # cast ket to superposition
    if type(data) in [superposition]:
      self.data = [data]
    if type(data) in [str]:
      self.data = [superposition(data)]

  def __len__(self):
    return len(self.data)
    
  def __iter__(self):
    for x in self.data:
      yield x
    
  def __str__(self):
    if len(self) == 0:
      return '|>'
    return ' . '.join(str(x) for x in self.data)

  def __getitem__(self, key):
    return self.data[key]

  def __add__(self, seq):              # tidy later!
    if type(seq) in [sequence]:
      r = copy.deepcopy(self)
      r.data += seq.data
      return r
#    if type(seq) in [ket, superposition]:
#      r = copy.deepcopy(self)
#      r.data.append(seq)
    if type(seq) in [ket]:
      r = copy.deepcopy(self)
      r.data.append(ket() + seq)               # cast ket to superposition. Sequences of kets seems to bug out all over the place!
      return r
    if type(seq) in [superposition]:
      r = copy.deepcopy(self)                  # do we need the deepcopy? How test?
      r.data.append(seq)
      return r
    if type(seq) in [list]:
      r = copy.deepcopy(self)
      r.data += seq
      return r
    else:
      return NotImplemented

# to implement:
#    if symbol == '+':
#      seq.add(the_seq)
#    elif symbol == '-':
#      seq.sub(the_seq)
#    elif symbol == '_':
#      seq.merge(the_seq)
#    elif symbol == '.':
#      seq.seq_merge(the_seq)

  def tail_add_seq(self, seq):                       #(|a> . |b> + |c>) + (|x> . |y>) == |a> . |b> + |c> + |x> . |y>  I think. I need more thinking time....
    if len(seq) == 0:
      return
    if len(self.data) == 0:
      self.data = [superposition()]
    if type(seq) in [ket, superposition]:
      self.data[-1].add_sp(seq)
#    if type(seq) in [ket]:
#      self.data[-1].add_sp(ket() + seq)
#    if type(seq) in [superposition]:
#      self.data[-1].add_sp(seq)
    if type(seq) in [sequence]:
      head, *tail = seq.data
      self.data[-1].add_sp(head)
      self.data += tail 

  def tail_sub_seq(self, seq):                       #(|a> . |b> + |c>) - (|x> . |y>) == |a> . |b> + |c> - |x> . |y>  I think. I need more thinking time....
    if len(seq) == 0:
      return
    if len(self.data) == 0:
      self.data = [superposition()]
    if type(seq) in [ket, superposition]:
      self.data[-1].sub_sp(seq)
    if type(seq) in [sequence]:
      head, *tail = seq.data
      self.data[-1].sub_sp(head)
      self.data += tail 

  def add_seq(self, seq):
    if len(seq) == 0:
      return
    if len(self) == 0:
      self.data = [superposition()]                               # is this right? should it be self.data = []?
    print('self: %s' % str(self))
    print('seq: %s' % str(seq))
    if type(seq) in [ket, superposition]:
      len_seq = 1
    else:
      len_seq = len(seq.data)
    max_len = max(len(self), len_seq)
    one = self.data + [superposition()] * (max_len - len(self.data))
    if type(seq) in [ket, superposition]:
      two = [seq] + [superposition()] * (max_len - 1)
    if type(seq) in [sequence]:
      two = seq.data + [superposition()] * (max_len - len(seq.data))
    print('one: %s' % [str(x) for x in one])
    print('two: %s' % [str(x) for x in two])
    self.data = []
    for k in range(max_len):
      self.data.append( one[k] + two[k] )      

  def sub_seq(self, seq):
    if len(seq) == 0:
      return
    if len(self) == 0:
      self.data = [superposition()]
    max_len = max(len(self), len(seq))
    one = self.data + [superposition()] * (max_len - len(self.data))
    if type(seq) in [ket, superposition]:
      two = [seq] + [superposition()] * (max_len - 1)
    if type(seq) in [sequence]:
      two = seq.data + [superposition()] * (max_len - len(seq.data))
    print('one: %s' % [str(x) for x in one])
    print('two: %s' % [str(x) for x in two])
    self.data = []
    for k in range(max_len):
      self.data.append( one[k] - two[k] )      

  def merge_seq(self, seq, space=''):                       #(|a> . |b> + |c>) _ (|x> . |y>) == |a> . |b> + |cx> . |y>  I think. I need more thinking time....
    if len(seq) == 0:
      return
    if len(self.data) == 0:
      self.data = [superposition()]
    if type(seq) in [superposition]:
      self.data[-1].merge_sp(seq, space)
    if type(seq) in [sequence]:
      head, *tail = seq.data
      self.data[-1].merge_sp(head, space)
      self.data += tail 

  def distribute_merge_seq(self, seq, space=''):            # |a> _ (|x> + |y>) == |ax> + |ay>             # this function feels like an ugly hack! Ditto the above add_seq/sub_seq/merge_seq!
    if len(seq) == 0:                                       # |a> _ (|x> . |y>) == |ax> . |ay>             # maybe I should implement sp.distribute_merge_sp(x)?? 
      return                                                # |a> _ (|x> - |y>) == |ax> - |ay> 
    print('distribute: self: %s' % self)
    print('distribute: seq:  %s' % seq)
    print('distribute: type(self): %s' % type(self))
    print('distribute: type(seq):  %s' % type(self))
    
    if len(self.data) == 0:
      self.data = [superposition()]
    if type(seq) in [superposition]:
      tail = self.data[-1]
      r = superposition()
      for x in seq:
        print('x: %s' % x)
        r2 = superposition(tail)
        r2.merge_sp(x, space)
        r.add_sp(r2)
      self.data[-1] = r
    if type(seq) in [sequence]:
      head = self.data[:-1]
      tail = self.data[-1]
      print('head: %s' % str(head))
      print('tail: %s' % str(tail))
      self.data = head
      for sp in seq.data:
        r = superposition()
        for x in sp:
          print('x: %s' % str(x))
          r2 = superposition(tail)
          r2.merge_sp(x, space)
          print('r2: %s' % str(r2))
          r.add_sp(r2)
        self.data.append(r)
                    
  
    

  def old_display(self):                   # print out a sequence class
    for k,x in enumerate(self.data):
      if type(x) in [superposition]:
        print("seq |%s: %s> => %s" % (self.name, str(k), x.coeff_sort())) # not super happy with this.
      else:
        print("seq |%s: %s> => %s" % (self.name, str(k), x))

  def long_display(self):                   # print out a sequence class
    for k,x in enumerate(self.data):
      if type(x) in [superposition] and False:                             # switched this branch off for now. I currently prefer not to change the order. 
        print("seq |%s> => %s" % (k, x.coeff_sort()))
      else:
        print("seq |%s> => %s" % (k, x))


  def display_minimalist(self):
    for x in self.data:
      if type(x) in [superposition]:
        print(x.coeff_sort())                                              # not super happy with this.
      else:
        print(x)

  def display(self,exact=False):
    if len(self.data) == 0:
      return '|>'
    return " . ".join(x.display(exact) for x in self)     # 1) get ket class to do the display. 2) need something better if we mix + - _ .  

  def readable_display(self):
    if len(self.data) == 0:
      return ""
    return " . ".join(x.readable_display() for x in self)

#  def add(self, seq):
#    self.data.append(copy.deepcopy(seq))

  def similar_index(self, sp):
    r = superposition()
    for k, elt in enumerate(self.data):
      similarity = simm(elt, sp)
      if similarity > 0:
        r.add(str(k), similarity)
    return r.coeff_sort()

  def ngrams(self, p):
    seq = sequence(self.name)
    for i in range(min(len(self.data)+1,p) - 1):
      seq.data = self.data[0:i+1]
      yield seq
    for i in range(len(self.data) - p + 1):
      seq.data = self.data[i:i+p]
      yield seq

  def pure_ngrams(self, p):
    seq = sequence(self.name)
    for i in range(len(self.data) - p + 1):
      seq.data = self.data[i:i+p]
      yield seq

  def encode(self, encode_dict):
    seq = sequence(self.name, [])
    for x in self.data:
      sp = full_encoder(encode_dict, x)
      seq.add(sp)
    return seq

  def noise(self, t):
    seq = sequence(self.name, [])
    for x in self.data:
      try:
        value = x + np.random.normal(0, t)               # enable adding noise to superpositions??
      except:
        value = x
      seq.add(value)
    return seq

  def smooth(self, k):                                    # hrmm... maybe if type superposition, apply coeff_sort()?
    try:
      arr = [self.data[0]] + self.data + [self.data[-1]]
      for _ in range(k):
        new_arr = arr[:]
        for i in range(len(self.data)):
          new_arr[i+1] = arr[i]/4 + arr[i+1]/2 + arr[i+2]/4
        arr = new_arr
      seq = sequence(self.name, [])
      seq.data = arr[1:-1]
      return seq
    except:
      return self

  def delta(self, dx = 1):                           # how do we handle sequences of 2tuples?
    try:
      arr = self.data + [self.data[-1]]              # how do we want to handle boundaries?
      new_arr = arr                                  # do we need [:]?
      #for i in range(len(self.data)):
      for i in range(len(self.data) - 1):            # how do we want to handle boudaries?
        new_arr[i] = (arr[i+1] - arr[i])/dx
      seq = sequence(self.name, [])
      #seq.data = new_arr[:-1]
      seq.data = new_arr[:-2]
      return seq
    except Exception as e:
      #print("delta exception:", e)
      return self
    
  def seq2sp(self):                                      # needs more thinking. Also, only works for sequences of superpositions.
    r = superposition()                                  # don't even know if useful yet.
    for x in self.data:
      r += x
    return r

  def multiply(self, t):                                 # is there a better way than writing all these identical wrappers?
    seq = sequence([])
    for x in self.data:
      seq.data.append(x.multiply(t))
    return seq

  def apply_fn(self, *args):
    seq = sequence([])
    for x in self.data:
      y = x.apply_fn(*args)
      if type(y) in [ket, superposition]:
        seq += y
      elif type(y) in [sequence]:
        seq.data += y.data
    return seq

  def apply_sp_fn(self, *args):
    seq = sequence([])
    for x in self.data:
      y = x.apply_sp_fn(*args)
      if type(y) in [ket, superposition]:
        seq += y
      elif type(y) in [sequence]:
        seq.data += y.data
    return seq

  def apply_naked_fn(self, *args):
    seq = sequence([])
    for x in self.data:
      seq.data.append(x.apply_naked_fn(*args))
    return seq

  def apply_op(self, context, op):
    if len(self) == 0:
      seq = sequence([]) + ket().apply_op(context, op)      # do we want this?
    else:
      seq = sequence([])
      for x in self.data:
        print('type(x): %s' % type(x))
        print('x: %s' % str(x))
        y = x.apply_op(context, op)
        print('type(y): %s' % type(y))
        print('y: %s' % str(y))
        if type(y) in [ket, superposition]:
          seq.data.append(y)
        elif type(y) in [sequence]:
          seq.data += y.data
    return seq

  def apply_sigmoid(self, sigmoid, *args):
    if len(self) == 0:
      seq = sequence([]) + ket().apply_sigmoid(sigmoid, *args)   # do we need/want this?
    else:
      seq = sequence([])
      for x in self.data:
        seq.data.append(x.apply_sigmoid(sigmoid, *args))
    return seq

  def select_range(self, *args):
    seq = sequence([])
    for x in self.data:
      seq.data.append(x.select_range(*args))
    return seq

  def drop(self):                               # may want to filter out |>.  eg: drop (|a> . 0|b> . |c>).
    seq = sequence([])                          # option 1) |a> . |> . |c>
    for x in self.data:                         # option 2) |a> . |c>
      seq.data.append(x.drop())                  
    return seq

  def activate(self,context=None,op=None,self_label=None):
    return self
