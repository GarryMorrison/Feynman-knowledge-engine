#######################################################################
# the semantic-db code
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2018
# Update: 31/7/2018
# Copyright: GPLv3
#
# Usage: 
#
#######################################################################

from collections import OrderedDict
import copy
import logging
from pprint import pprint

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger()


# from semantic_db.functions import *
# from semantic_db.sigmoids import *

# put this here for now:
# http://stackoverflow.com/questions/4836710/does-python-have-a-built-in-function-for-string-natural-sort
# 6/8/2014: Doh! There is a bug in sorting things like 0 vs 00 vs 000.
def natural_sorted(list, key=lambda s: s):
    """
    Sort the list into natural alphanumeric order.
    """

    def get_alphanum_key_func(key):
        convert = lambda text: int(text) if text.isdigit() else text
        return lambda s: [convert(c) for c in re.split('([0-9]+)', key(s))]

    sort_key = get_alphanum_key_func(key)
    #    list.sort(key=sort_key)
    return sorted(list, key=sort_key)


# convert float to int if possible:
def float_to_int(x, t=3):
    if float(x).is_integer():
        return str(int(x))
    return str(round(x, t))


def my_print(name, value=''):
    return
    if value is '':
        print(name)
    else:
        print(name + ': ', end='')
        pprint(value)


class ket(object):
    def __init__(self, label='', value=1):
        self.label = label
        self.value = float(value)

    #    self.value = int(value)     # sometimes useful to restrict to integers.

    def __str__(self):
        return self.display()

    def __len__(self):
        if self.label == '':  # returns 0 for |>.
            return 0
        return 1

    def slen(self):
        return ket('number: 1')

    def __eq__(self, other):  # do we use this anywhere?
        return self.label == other.label and self.value == other.value

    def __iter__(self):
        yield ket(self.label, self.value)

    def items(self):
        yield self.label, self.value

    def display(self, exact=False):
        if self.value == 1:
            s = "|%s>" % self.label
        elif exact:  # tweaked for exact display, so dump to file and load again don't accidentally zero coeffs.
            s = "%s|%s>" % (self.value, self.label)
        else:
            s = "%s|%s>" % (float_to_int(self.value), self.label)
        return s

    def long_display(self):  # where is this used??
        if self.value == 1:
            return self.label
        else:
            return "%.3f    %s" % (self.value, self.label)

    def readable_display(self):  # where is this used??
        if self.label == '':
            return ""
        if self.value == 1:
            return self.label
        else:
            if self.value.is_integer():
                return "{0:.0f} {1}".format(self.value, self.label)  # not consistent style with display() and long_display().FIX.
            return "{0:.2f} {1}".format(self.value, self.label)

    def __add__(self, x):
        return superposition(self) + x

    def __sub__(self, x):
        return superposition(self) - x

    def merge(self, x):  # |a> + 2.1|b> + 3|c> _ 7.9|d> + |e> + |f> == |a> + 2.1|b> + |cd> + |e> + |f>
        label = self.label + x.select_elt(1).label  # assumes select_elt(k) returns a single ket, even for sp class.
        return ket(label)

    def seq_add(self, x):  # ket('x').seq_merge(ket('y')) == |x> . |y>
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

    def apply_naked_fn(self, fn, *args):
        return fn(*args)

    def apply_fn(self, fn, *args):
        r = fn(self, *args)
        return superposition(r)

    def apply_sp_fn(self, fn, *args):
        return fn(self, *args)

    def apply_seq_fn(self, fn, *args):  # need to test this!
        return fn(self, *args)

    def apply_op(self, context, op):  # TODO? Maybe later, make it work with function operators too, rather than just literal operators?
        r = context.seq_fn_recall(op, [ket(), self], True)  # this is broken! Not sure why, yet. I think I fixed it.
        if len(r) == 0:
            r = context.recall(op, self, True)  # see much later in the code for definition of recall.
        return r

    def select_elt(self, k):
        if k != 1 and k != -1:
            return ket()
        else:
            return ket(self.label, self.value)

    # 5/2/2015: eg: without this: select[1,5] "" |bah> bugs out if "" |bah> is not defined.
    def select_range(self, a, b):
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
    def top(self, k):
        if k == 0:
            return ket()
        return ket(self.label, self.value)

    def index_split(self, k):  # OK. Now need to test it. Maybe improve for k other than {1,-1}.
        if k == 1:  # do we need it anymore? Isn't it just in the parser to help with |x> _ |y>??
            return ket(self.label, self.value), ket()
        if k == -1:
            return ket(), ket(self.label, self.value)

    def pick_elt(self):
        return ket(self.label, self.value)

    def weighted_pick_elt(self):
        return ket(self.label, self.value)

    def pick(self, n):
        if n == 0:
            return ket()
        return ket(self.label, self.value)


    #  def find_index(self,one):
    #    label = one.label if type(one) == ket else one
    #    if self.label == label:
    #      return 1
    #    return 0
    #
    def find_value(self, one):
        label = one.label if type(one) is ket else one
        if self.label == label:
            return self.value
        return 0

    #  def find_max_coeff(self):
    #    return self.value
    #
    #  def find_min_coeff(self):
    #    return self.value

    def normalize(self, t=1):
        r = ket(self.label, self.value)
        if r.value > 0:
            r.value = t
        return r

    def softmax(self):
        return ket(self.label, 1)

    def rescale(self, t=1):
        r = ket(self.label, self.value)
        if r.value > 0:
            r.value = t
        return r

    def multiply(self, t):
        return ket(self.label, self.value * t)

    #  def add(self,t):                                        # Nope. Deleted for now. Conflicts with x.add(key,value)
    #    return ket(self.label,self.value + t)

    # 6/1/2015: hrmm... maybe abs, absolute_noise, and relative_noise should be sigmoids!
    # newly added 2/4/2014:
    # yeah. moved to sigmoid (4/5/2015) Hope we don't break anything!
    #  def abs(self):
    #    return ket(self.label,abs(self.value))

    # newly added 7/4/2014:
    # add noise to the ket/sp in range [0,t]
    def absolute_noise(self, t):
        return ket(self.label, self.value + random.uniform(0, t))  # hrmm.. so noise is additive only?

    # newly added 7/4/2014:
    # add noise to ket/sp in range [0,t*max_coeff]
    def relative_noise(self, t):
        max_coeff = self.value
        return ket(self.label, self.value + random.uniform(0, t * max_coeff))

    def coeff_sort(self):
        return ket(self.label, self.value)

    def ket_sort(self):
        return ket(self.label, self.value)

    #  def find_max_coeff(self):                                 # where are these used? find-topic?
    #    return self.value
    #
    #  def find_min_coeff(self):
    #    return self.value

    def number_find_max_coeff(self):
        return ket("number: " + str(self.value))

    def number_find_min_coeff(self):
        return ket("number: " + str(self.value))

    # 24/2/2015:
    # implements discrim-drop[t] SP
    # ie: if discrim is > t return |>, else return value.
    # don't know how I want this to work!
    #  def discrimination_drop(self,t):
    #    return ket(self.label,self.value)

    # sigmoids apply to the values of kets, and leave ket labels alone.
    def apply_sigmoid(self, sigmoid, t1=None, t2=None):
        r = ket(self.label, self.value)
        if t1 is None:
            r.value = sigmoid(r.value)
        elif t2 is None:
            r.value = sigmoid(r.value, t1)
        else:
            r.value = sigmoid(r.value, t1, t2)
        return r

    # do we need a superposition version of this? Probably...
    # implements: similar[op] |x>
    def old_similar(self, context, op):  # should I use .apply_op(context,op,True)?
        f = self.apply_op(context, op)  # use apply_op or context.recall() directly?
        print("f:", f.display())  # in light of active=True thing, apply_op() seems the right answer.
        #    return context.pattern_recognition(f,op) # yeah, but what about in pat_rec?
        return context.pattern_recognition(f, op).delete_ket(self)  # we delete self, ie |x>, from the result, since it is always a 100% match anyway.

    # 23/2/2015:
    # implements: similar[op1,op2] |x>
    def similar(self, context, *ops):
        try:
            op1, op2 = ops
        except:
            op1 = ops[0]
            op2 = ops[0]
        f = self.apply_op(context, op1)
        return context.pattern_recognition(f, op2).delete_ket(self)  # we delete self, ie |x>, from the result, since it is always a 100% match anyway.

    # 23/2/2015:
    # implements: self-similar[op1,op2] |x>
    # ie don't delete |x>
    def self_similar(self, context, *ops):
        try:
            op1, op2 = ops
        except:
            op1 = ops[0]
            op2 = ops[0]
        f = self.apply_op(context, op1)
        return context.pattern_recognition(f, op2)

    # 14/1/2016: we need to test it though.
    # implements: similar-input[op] |x>                                  # I don't think this makes much sense, in light of: similar-input[op] some |superposition>
    #  def similar_input(self,context,op):
    #    return context.pattern_recognition(self,op).delete_ket(self)    # we delete self, ie |x>, from the result, since it is always a 100% match anyway.

    # 14/1/2016:
    # implements: self-similar-input[op] |x>
    # ie don't delete |x>
    def similar_input(self, context, op):
        return context.pattern_recognition(self, op)

    # implements: find-topic[op] |x>
    def find_topic(self, context, op):
        return context.map_to_topic(self, op)

    # 2/4/2015: intn-find-topic[op] |a b c>
    # I don't think this thing is all that useful.
    # currently we don't have a superposition version of this. Not sure it is needed.
    #
    def intn_find_topic(self, context, op):
        words = self.label.lower().split()
        logger.debug("words: " + words)
        if len(words) == 0:
            return ket("", 0)
        results = [context.map_to_topic(ket(x), op) for x in words]
        logger.debug("len results: " + str(len(results)))
        if len(results) == 0:  # this should never be true!
            return ket("", 0)
        r = results[0]
        for sp in results:
            logger.debug("sp: " + str(sp))
            r = intersection(r, sp)
        return r.normalize(100).coeff_sort()

    def count(self):  # duplicates len(x), but keep it anyway, because of its brother count_sum().
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

    def sdrop(self):
        return self.drop()

    def drop_below(self, t):
        if self.value >= t:
            return ket(self.label, self.value)
        else:
            return ket()

    def drop_above(self, t):
        if self.value <= t:
            return ket(self.label, self.value)
        else:
            return ket()

    def drop_zero(self):  # don't know where we use this.
        if abs(x.value) > 0.0001:
            return ket(self.label, self.value)
        else:
            return ket("", 0)

    def is_not_empty(self):
        if self.label == "":
            return ket("no")
        return ket("yes")

    def activate(self, context=None, op=None, self_label=None):
        return ket(self.label, self.value)  # not sure if we need this:
        # return self                       # or if this will suffice.

    def to_ket(self):
        return self

    def to_sp(self):
        return self



# a superposition is a linear combination of kets
# where kets are string, float pairs
class superposition(object):
    def __init__(self, first='', value=1):
        #    self.dict = {}                 # faster and cheaper than OrderedDict() if you don't need to preserve order
        self.dict = OrderedDict()
        if first is not '':
            if type(first) in [str]:  # this is ugly! Mixing and matching string vs superposition? Maybe we should keep a ket class?? Also, ket is quicker to type!
                self.dict[first] = value               # r1 = superposition('fred')
            elif type(first) in [ket, superposition]:  # r2 = superposition('fred',3.2)
                for key, value in first.items():       # r4 = superposition(ket('fred'))
                    if key != '':                      # r5 = superposition(another-sp)
                        self.dict[key] = value

    def old_str(self):
        if len(self.dict) == 0:
            return '|>'
        list_of_kets = []
        for key, value in self.dict.items():
            if value == 1:
                s = "|%s>" % key
            else:
                s = "%s|%s>" % (float_to_int(value), key)
            list_of_kets.append(s)
        return " + ".join(list_of_kets)

    def __str__(self):
        if len(self.dict) == 0:
            return '|>'
        s = ''
        for key, value in self.dict.items():
            sign = '+'
            if value < 0:
                sign = '-'
            if abs(value) == 1:
                s += " %s |%s>" % (sign, key)
            else:
                s += " %s %s|%s>" % (sign, float_to_int(abs(value)), key)
        if s.startswith(' + '):
            s = s[3:]
        return s

    def __iter__(self):
        for key, value in self.dict.items():
            yield ket(key, value)

    def items(self):
        for key, value in self.dict.items():
            yield key, value

    def __len__(self):
        return len(self.dict)

    def slen(self):
        return ket('number: 1')

    def __getattr__(self, name):
        if name == 'label':
            if len(self.dict) == 0:
                return ""
            for key, value in self.dict.items():  # NB. For a sp with more than 1 element, sp.label and sp.value returns label and value of the first element only.
                return key
        if name == 'value':
            if len(self.dict) == 0:
                return 1  # hrmm... what is the value of |>? Currently set to 1.
            for key, value in self.dict.items():
                return value
        else:
            raise AttributeError

    def __truediv__(self, divisor):
        if type(divisor) in [int, float]:
            r = superposition()
            for key, value in self.dict.items():
                r.dict[key] = value / divisor
            return r
        else:
            return NotImplemented

    def __add__(self, sp):
        if type(sp) in [ket, superposition]:
            r = copy.deepcopy(self)
            for key, value in sp.items():
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
            for key, value in sp.items():
                r.add(key, - value)
            return r
        else:
            return NotImplemented

    def add(self, s, value=1):  # what about adding a superposition? r.add(some-sp). Or r.add_sp(some-sp)? Yeah, and r.add_sp(some-ket)
        if s == '':             # |x> + 3.72|> == |x>
            return
        if s in self.dict:
            self.dict[s] += float(value)
        else:
            self.dict[s] = float(value)

    def sub(self, s, value=1):
        if s == '':
            return
        if s in self.dict:
            self.dict[s] -= float(value)
        else:
            self.dict[s] = - float(value)

    def add_sp(self, sp):  # handles r.add_sp(some-ket) and r.add_sp(some-sp). Breaks if sp is a stored_rule or a memoizing_rule. How fix?
        for key, value in sp.items():
            self.add(key, value)

    def sub_sp(self, sp):
        for key, value in sp.items():
            self.sub(key, value)

    def max_add(self, str, value=1):
        if str == '':
            return
        if str in self.dict:
            self.dict[str] = max(self.dict[str], float(value))
        else:
            self.dict[str] = float(value)

    def max_add_sp(self, sp):
        for key, value in sp.items():
            self.max_add(key, value)

    def seq_add(self, x):  # this probably doesn't work the way you want either. y = sp1.seq_add(sp2) works. sp1.seq_add(sp2) does not.
        r = sequence(self) + x
        return r

    def merge_sp(self, x, space=''):  # |a> + 2.1|b> + 3|c> _ 7.9|d> + |e> + |f> == |a> + 2.1|b> + |cd> + |e> + |f>
        if len(self) == 0:
            for key, value in x.items():
                self.add(key, value)
            return
        head = superposition()  # is there a better way to do this??
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
        #    result = head + ket(tail.label + space + x_head.label, tail.value) + x_tail
        result = head + ket(tail.label + space + x_head.label, x_head.value * tail.value) + x_tail
        self.dict = result.dict

    #  def clean_add(self,one):           # I don't know where this is used. Maybe remove since it duplicates add_sp().
    #    for key,value in one.items():
    #      self.add(key,value)

    def old_display(self):
        list_of_pairs = []
        for key, value in self.dict.items():
            if value == 1.0:
                s = "%s" % key
            else:
                s = "%s %s" % (float_to_int(value), key)
            list_of_pairs.append(s)
        return ",\t".join(list_of_pairs)

    def display(self, exact=False):
        if len(self.dict) == 0:
            return '|>'
        return " + ".join(x.display(exact) for x in self)  # 1) get ket class to do the display. 2) need something better if we mix + - _ .

    def readable_display(self):
        if len(self.dict) == 0:
            return ""
        return ", ".join(x.readable_display() for x in self)

    def pair(self):  # if the dict is longer than 1 elt, this returns a random pair
        for key, value in self.dict.items():  # presuming not using an OrderedDict
            return key, value

    def pick(self, n):  # randomly pick and return n elements from the superposition
        r = superposition()
        for key in random.sample(list(self.dict), n):
            value = self.dict[key]
            r.add(key, value)
        return r

    def pick_elt(self):
        if len(self) == 0:
            return ket()
        key = random.choice(list(self.dict))
        value = self.dict[key]
        return ket(key, value)

    def weighted_pick_elt(self):  # quick test in the console, looks to be roughly right.
        if len(self.drop()) == 0:
            return ket()
        # total = sum(x.value for x in self)
        total = sum(x.value for x in self.drop())
        r = random.uniform(0, total)
        upto = 0
        # for x in self:
        for x in self.drop():
            w = x.value
            if upto + w > r:
                return x
            upto += w
        assert False, "Shouldn't get here in weighted-pick-elt"

    def get_value(self, str):  # maybe convert to  __getitem__
        if str in self.dict:
            return self.dict[str]
        else:
            return 0

    #  def the_value(self):                         # if the dict is longer than 1 elt, this returns a random value
    #    for key,value in self.dict.items():
    #      return value
    #    return 0

    def rescale(self, t=1):
        if len(self.dict) == 0:
            return superposition()
        the_max = max(value for key, value in self.dict.items())
        result = superposition()
        if the_max > 0:
            for key, value in self.dict.items():
                result.dict[key] = t * self.dict[key] / the_max
        return result

    def normalize(self, t=1):
        if len(self.dict) == 0:
            return superposition()
        the_sum = sum(value for key, value in self.dict.items())
        result = superposition()
        if the_sum > 0:
            for key, value in self.dict.items():
                result.dict[key] = t * self.dict[key] / the_sum
        return result

    def softmax(self):
        if len(self) == 0:
            return ket()
        r = superposition()
        the_sum = sum(math.exp(value) for (key, value) in self.dict.items())
        for key, value in self.dict.items():
            r.add(key, math.exp(value) / the_sum)
        return r

    def multiply(self, t):
        r = superposition()
        for key, value in self.dict.items():
            r.add(key, value * t)
        return r
        return result

    # add noise to the ket/sp in range [0,t]
    def absolute_noise(self, t):
        r = superposition()
        for key, value in self.dict.items():
            r.add(key, value + random.uniform(0, t))
        return r

    # add noise to ket/sp in range [0,t*max_coeff]
    def relative_noise(self, t):
        max_coeff = self.find_max_coeff()
        r = superposition()
        for key, value in self.dict.items():
            r.add(key, value + random.uniform(0, t * max_coeff))
        return r

    def coeff_sort(self):
        r = superposition()
        for key, value in sorted(self.dict.items(), key=lambda x: x[1], reverse=True):  # which order? 3|a> + 2|b> + |c> or |c> + 2|b> + 3|c>?
            r.add(key, value)
        return r

    def ket_sort(self):
        r = superposition()
        for key, value in natural_sorted(self.dict.items(), key=lambda x: x[0].lower()):
            r.add(key, value)
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

    def select_top(self, k):
        r = superposition()
        for i, (key, value) in enumerate(self.dict.items()):
            r.add(key, value)
            if i + 1 >= k:
                break
        return r

    # NB: we use: 1 <= k <= len, not 0 <= k < len to access ket objects.
    # NB: though we still use -1 for the last element, -2 for the second last element, etc.
    def select_elt(self, k):
        if k >= 1 and k <= len(self.dict):
            label, value = list(self.dict.items())[k - 1]  # is there a better way to do this! Mapping entire sp to list, just to keep 1 element!!
            return ket(label, value)                       # perhaps, https://stackoverflow.com/questions/10058140/accessing-items-in-a-ordereddict
        elif k < 0:                                        # import itertools
            label, value = list(self.dict.items())[k]      # next(itertools.islice(d.values(), 0, 1))
            return ket(label, value)                       # next(itertools.islice(d.values(), 1, 2))
        else:
            return ket("", 0)

    def select_range(self, a, b):
        a = max(1, a) - 1
        b = min(b, len(self.dict))
        r = superposition()
        for label, value in list(self.dict.items())[a:b]:
            r.add(label, value)
        return r

    def top(self, k):
        if k == 0:
            return ket()
        value = self.coeff_sort().select_range(k, k).value
        return self.drop_below(value)

    def delete_elt(self, k):
        r = superposition()
        for i, (key, value) in enumerate(self.items()):
            if i != k - 1:
                r.add(key, value)
        return r

    def delete_elt_v2(self, k):
        r = copy.deepcopy(self)
        label, value = list(self.dict.items())[k - 1]
        r.add(label, -value)  # return r.drop() ??
        return r

    def delete_elt_v3(self, k):
        label, value = list(self.dict.items())[k - 1]
        r = copy.deepcopy(self)
        del r.dict[label]
        return r

    def find_index(self, one):
        label = one.label if type(one) is ket else one
        for k, (key, value) in enumerate(self.dict.items()):
            if key == label:
                return k + 1
        return 0

    def find_value(self, one):
        label = one.label if type(one) is ket else one
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

    def delete_ket(self, one):  # do we need a delete_sp() too?
        label = one.label if type(one) is ket else one
        r = copy.deepcopy(self)
        del r.dict[label]
        return r

    def drop(self):
        r = superposition()
        for key, value in self.dict.items():
            if value > 0:
                r.add(key, value)
        return r

    def sdrop(self):
        return self.drop()

    def drop_below(self, t):
        r = superposition()
        for key, value in self.dict.items():
            if value >= t:
                r.add(key, value)
        return r

    def drop_above(self, t):
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

    def product(self):  # need to put these in ket now.
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

    def apply_naked_fn(self, fn, *args):
        return fn(*args)

    def apply_fn(self, fn, *args):
        if len(self) == 0:
            return superposition() + ket().apply_fn(fn, *args)  # need to verify this doesn't break anything
        r = superposition()
        for x in self:
            r += fn(x, *args)   # should this be: r.add_sp(...)? Also, what happens if fn(...) returns a sequence?
        return r                # or maybe r.add_seq(...)?

    def apply_sp_fn(self, fn, *args):
        return fn(self, *args)

    def apply_seq_fn(self, fn, *args):  # need to test this!
        return fn(self, *args)

    def apply_op(self, context, op):  # bugs out when rule is a sequence, which is now most of the time, once parser is finished.
        r = context.seq_fn_recall(op, [ket(), self], True)  # op (*) has higher precedence than op |*>
        if len(r) == 0:
            r = sequence([])
            if len(self) == 0:
                rule = context.recall(op, '', True)  # op|> can return something other than |>. At least for now.
                r.add_seq(rule)
            else:
                for x in self:
                    rule = context.recall(op, x, True)  # should this be apply_op() instead? Nah, don't think so.
                    r.add_seq(rule)
        return r

    def apply_sigmoid(self, sigmoid, t1=None, t2=None):  # use *args notation. Fix!
        r = superposition()
        if t1 == None:
            for key, value in self.dict.items():
                value = sigmoid(value)
                r.add(key, value)
        elif t2 == None:
            for key, value in self.dict.items():
                value = sigmoid(value, t1)
                r.add(key, value)
        else:
            for key, value in self.dict.items():
                value = sigmoid(value, t1, t2)
                r.add(key, value)
        return r

    def is_not_empty(self):
        if len(self) == 0:
            return ket('no')
        return ket('yes')

    def activate(self, context=None, op=None, self_label=None):
        return self

    def to_ket(self):  # returns the first ket in the superposition
        for key, value in self.items():
            return ket(key, value)

    def to_sp(self):
        return self


# sequence class. Has methods we need to chomp out that are not relevant here. TODO.
class sequence(object):
    def __init__(self, data=[]):
        #  def __init__(self, name='', data = []):
        #    self.name = name
        # print('sequence data: %s' % data)
        if type(data) in [list]:
            self.data = data  # copy.deepcopy(data)??
        if type(data) in [sequence]:
            self.data = copy.deepcopy(data.data)
        if type(data) in [ket]:
            # self.data = [ket() + data]  # cast ket to superposition
            self.data = [superposition(data)]
        if type(data) in [superposition]:
            self.data = [data]
        if type(data) in [str]:
            self.data = [superposition(data)]

    def __len__(self):
        if len(self.data) == 0:
            return 0
        if len(self.data) == 1 and self.data[0].label == '':
            return 0
        return len(self.data)

    def slen(self):
        return ket('number: ' + str(len(self)))

    def __iter__(self):
        for x in self.data:
            yield x

    def __str__(self):
        if len(self) == 0:
            return '|>'
        return ' . '.join(str(x) for x in self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __add__(self, seq):  # tidy later!
        if type(seq) in [sequence]:
            r = copy.deepcopy(self)
            r.data += seq.data
            return r
        #    if type(seq) in [ket, superposition]:
        #      r = copy.deepcopy(self)
        #      r.data.append(seq)
        if type(seq) in [ket]:
            r = copy.deepcopy(self)
            r.data.append(ket() + seq)  # cast ket to superposition. Sequences of kets seems to bug out all over the place!
            return r
        if type(seq) in [superposition]:
            r = copy.deepcopy(self)  # do we need the deepcopy? How test?
            r.data.append(seq)
            return r
        if type(seq) in [list]:  # this looks broken.
            r = copy.deepcopy(self)
            r.data += seq
            return r
        else:
            return NotImplemented

    def tail_add_seq(self, seq):  # (|a> . |b> + |c>) + (|x> . |y>) == |a> . |b> + |c> + |x> . |y>  I think. I need more thinking time....
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

    def tail_sub_seq(self, seq):  # (|a> . |b> + |c>) - (|x> . |y>) == |a> . |b> + |c> - |x> . |y>  I think. I need more thinking time....
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
            self.data = [superposition()]  # is this right? should it be self.data = []?
        # my_print('self', str(self))
        # my_print('seq', str(seq))
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
        # my_print('one', [str(x) for x in one])
        # my_print('two', [str(x) for x in two])
        self.data = []
        for k in range(max_len):
            self.data.append(one[k] + two[k])

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
        # my_print('one', [str(x) for x in one])
        # my_print('two', [str(x) for x in two])
        self.data = []
        for k in range(max_len):
            self.data.append(one[k] - two[k])

    def merge_seq(self, seq, space=''):  # (|a> . |b> + |c>) _ (|x> . |y>) == |a> . |b> + |cx> . |y>  I think. I need more thinking time....
        if len(seq) == 0:
            return
        if len(self.data) == 0:
            self.data = [superposition()]
        if type(seq) in [ket, superposition]:
            self.data[-1].merge_sp(seq, space)
        if type(seq) in [sequence]:
            head, *tail = seq.data
            self.data[-1].merge_sp(head, space)
            self.data += tail

    def distribute_merge_seq(self, seq, space=''):  # |a> _ (|x> + |y>) == |ax> + |ay>             # this function feels like an ugly hack! Ditto the above add_seq/sub_seq/merge_seq!
        if len(seq) == 0:                           # |a> _ (|x> . |y>) == |ax> . |ay>             # maybe I should implement sp.distribute_merge_sp(x)??
            return                                  # |a> _ (|x> - |y>) == |ax> - |ay>
        # print('distribute: self: %s' % self)
        # print('distribute: seq:  %s' % seq)
        # print('distribute: type(self): %s' % type(self))
        # print('distribute: type(seq):  %s' % type(self))

        if len(self.data) == 0:
            self.data = [superposition()]
        if type(seq) in [ket, superposition]:
            tail = self.data[-1]
            r = superposition()
            for x in seq:
                # print('x: %s' % x)
                r2 = superposition(tail)
                r2.merge_sp(x, space)
                r.add_sp(r2)
            self.data[-1] = r
        if type(seq) in [sequence]:
            head = self.data[:-1]
            tail = self.data[-1]
            # print('head: %s' % str(head))
            # print('tail: %s' % str(tail))
            self.data = head
            for sp in seq.data:
                r = superposition()
                if len(sp) == 0:
                    r2 = superposition(tail)
                    r2.merge_sp(ket(), space)
                    r.add_sp(r2)
                else:
                    for x in sp:
                        # print('x: %s' % str(x))
                        r2 = superposition(tail)
                        r2.merge_sp(x, space)
                        # print('r2: %s' % str(r2))
                        r.add_sp(r2)
                self.data.append(r)

    def old_display(self):  # print out a sequence class
        for k, x in enumerate(self.data):
            if type(x) in [superposition]:
                print("seq |%s: %s> => %s" % (self.name, str(k), x.coeff_sort()))  # not super happy with this.
            else:
                print("seq |%s: %s> => %s" % (self.name, str(k), x))

    def long_display(self):  # print out a sequence class
        for k, x in enumerate(self.data):
            if type(x) in [superposition] and False:  # switched this branch off for now. I currently prefer not to change the order.
                print("seq |%s> => %s" % (k, x.coeff_sort()))
            else:
                print("seq |%s> => %s" % (k, x))

    def display_minimalist(self):
        for x in self.data:
            if type(x) in [superposition]:
                print(x.coeff_sort())  # not super happy with this.
            else:
                print(x)

    def display(self, exact=False):
        if len(self.data) == 0:
            return '|>'
        return " . ".join(x.display(exact) for x in self)  # 1) get ket class to do the display. 2) need something better if we mix + - _ .

    def readable_display(self):
        if len(self.data) == 0:
            return ""
        return " . ".join(x.readable_display() for x in self)

    #  def add(self, seq):
    #    self.data.append(copy.deepcopy(seq))

    def similar_index(self, sp):  # do we use this anywhere?
        r = superposition()
        for k, elt in enumerate(self.data):
            similarity = simm(elt, sp)
            if similarity > 0:
                r.add(str(k), similarity)
        return r.coeff_sort()

    def ngrams(self, p):  # do we use this anywhere?
        seq = sequence(self.name)
        for i in range(min(len(self.data) + 1, p) - 1):
            seq.data = self.data[0:i + 1]
            yield seq
        for i in range(len(self.data) - p + 1):
            seq.data = self.data[i:i + p]
            yield seq

    def pure_ngrams(self, p):  # do we use this anywhere?
        seq = sequence(self.name)
        for i in range(len(self.data) - p + 1):
            seq.data = self.data[i:i + p]
            yield seq

    def encode(self, encode_dict):  # do we use this anywhere?
        seq = sequence(self.name, [])
        for x in self.data:
            sp = full_encoder(encode_dict, x)
            seq.add(sp)
        return seq

    def noise(self, t):  # do we use this anywhere?
        seq = sequence(self.name, [])
        for x in self.data:
            try:
                value = x + np.random.normal(0, t)  # enable adding noise to superpositions??
            except:
                value = x
            seq.add(value)
        return seq

    def smooth(self, k):  # hrmm... maybe if type superposition, apply coeff_sort()?
        try:
            arr = [self.data[0]] + self.data + [self.data[-1]]
            for _ in range(k):
                new_arr = arr[:]
                for i in range(len(self.data)):
                    new_arr[i + 1] = arr[i] / 4 + arr[i + 1] / 2 + arr[i + 2] / 4
                arr = new_arr
            seq = sequence(self.name, [])
            seq.data = arr[1:-1]
            return seq
        except:
            return self

    def delta(self, dx=1):  # how do we handle sequences of 2tuples?
        try:
            arr = self.data + [self.data[-1]]  # how do we want to handle boundaries?
            new_arr = arr  # do we need [:]?
            # for i in range(len(self.data)):
            for i in range(len(self.data) - 1):  # how do we want to handle boudaries?
                new_arr[i] = (arr[i + 1] - arr[i]) / dx
            seq = sequence(self.name, [])
            # seq.data = new_arr[:-1]
            seq.data = new_arr[:-2]
            return seq
        except Exception as e:
            # print("delta exception:", e)
            return self

    def seq2sp(self):  # needs more thinking. Also, only works for sequences of superpositions.
        r = superposition()  # don't even know if useful yet.
        for x in self.data:
            # r += x
            r.add_sp(x)
        return r

    def multiply(self, t):  # is there a better way than writing all these identical wrappers?
        seq = sequence([])
        for x in self.data:
            seq.data.append(x.multiply(t))
        return seq

    def apply_fn(self, *args):
        if len(self) == 0:
            return sequence([]) + ket().apply_fn(*args)
        # print('apply_fn seq: %s' % self)
        seq = sequence([])
        for x in self.data:
            # print('apply_fn x: %s' % x)
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

    def apply_seq_fn(self, fn, *args):
        return fn(self, *args)

    def apply_op(self, context, op):
        # logger.debug('inside seq apply_op')
        # logger.debug('seq: %s' % str(self))
        # logger.debug('op: %s' % op)
        # seq = sequence([])
        # if op != 'supported-ops':
        seq = context.seq_fn_recall(op, [ket(), self], active=True)
        if len(seq) == 0:
            if len(self) == 0:
                seq = sequence([]) + ket().apply_op(context, op)  # do we want this?
            else:
                seq = sequence([])
                for x in self.data:
                    # print('type(x): %s' % type(x))
                    # print('x: %s' % str(x))
                    y = x.apply_op(context, op)
                    # print('type(y): %s' % type(y))
                    # print('y: %s' % str(y))
                    if len(y) == 0:                          # keep |> terms in our sequences.
                        seq.data.append(superposition())     # use sdrop if you want otherwise.
                    elif type(y) in [ket, superposition]:
                        seq.data.append(y)
                    elif type(y) in [sequence]:
                        seq.data += y.data
        return seq

    def apply_sigmoid(self, sigmoid, *args):
        if len(self) == 0:
            seq = sequence([]) + ket().apply_sigmoid(sigmoid, *args)  # do we need/want this?
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

    def drop(self):  # may want to filter out |>.  eg: drop (|a> . 0|b> . |c>).
        seq = sequence([])  # option 1) |a> . |> . |c>              # perhaps call this drop
        for x in self.data:  # option 2) |a> . |c>                   # and call this sdrop?
            seq.data.append(x.drop())
        return seq

    def drop_below(self, t):
        seq = sequence([])
        for x in self.data:
            seq.data.append(x.drop_below(t))
        return seq

    def drop_above(self, t):
        seq = sequence([])
        for x in self.data:
            seq.data.append(x.drop_above(t))
        return seq

    def sdrop(self):
        seq = sequence([])
        for sp in self.data:
            r = sp.drop()
            if len(r) > 0:
                seq.data.append(r)
        return seq

    def pick_elt(self):
        seq = sequence([])
        for x in self.data:
            seq.data.append(x.pick_elt())
        return seq

    def spick_elt(self):
        if len(self) == 0:
            return sequence([])
        r = random.choice(self.data)
        return sequence(r)

    def weighted_pick_elt(self):
        seq = sequence([])
        for x in self.data:
            seq.data.append(x.weighted_pick_elt())
        return seq

    def pick(self, n):
        seq = sequence([])
        for x in self.data:
            seq.data.append(x.pick(n))
        return seq

    def normalize(self, t=1):
        seq = sequence([])
        for x in self.data:
            seq.data.append(x.normalize(t))
        return seq

    def rescale(self, t=1):
        seq = sequence([])
        for x in self.data:
            seq.data.append(x.rescale(t))
        return seq

    def softmax(self, t=1):
        seq = sequence([])
        for x in self.data:
            seq.data.append(x.softmax())
        return seq

    def absolute_noise(self, t):
        seq = sequence([])
        for x in self.data:
            seq.data.append(x.absolute_noise(t))
        return seq

    def relative_noise(self, t):
        seq = sequence([])
        for x in self.data:
            seq.data.append(x.relative_noise(t))
        return seq

    def coeff_sort(self):
        seq = sequence([])
        for x in self.data:
            seq.data.append(x.coeff_sort())
        return seq

    def ket_sort(self):
        seq = sequence([])
        for x in self.data:
            seq.data.append(x.ket_sort())
        return seq

    def shuffle(self):
        seq = sequence([])
        for x in self.data:
            seq.data.append(x.shuffle())
        return seq

    def sselect_range(self, a, b):  # tweak so we can do: sselect[1,-2]
        # a = max(1, a) - 1
        if a >= 0:
            a -= 1
        b = min(b, len(self.data))
        seq = sequence([])
        seq.data = self.data[a:b]
        return seq

    def top(self, k):
        seq = sequence([])
        for x in self.data:
            seq.data.append(x.top(k))
        return seq

    def reverse(self):
        seq = sequence([])
        for x in self.data:
            seq.data.append(x.reverse())
        return seq

    def sreverse(self):
        seq = sequence([])
        seq.data = list(reversed(self.data))
        return seq

    def is_not_empty(self):
        if len(self) == 0:
            return ket("no")
        return ket("yes")

    def snumber_count(self):
        result = len(self)
        return ket("number: " + str(result))

    def number_count(self):
        seq = sequence([])
        for x in self.data:
            seq.data.append(x.number_count())
        return seq

    def number_count_sum(self):
        seq = sequence([])
        for x in self.data:
            seq.data.append(x.number_count_sum())
        return seq

    def snumber_count_sum(self):
        result = 0
        for x in self.data:
            result += x.count_sum()
        return ket('number: ' + str(result))  # float_to_int() ?


    def activate(self, context=None, op=None, self_label=None):
        return self

    def similar_input(self, context, op):
        return context.pattern_recognition(self, op)

    def to_ket(self):
        if len(self) == 0:
            return ket()
        for sp in self.data:
            return sp.to_ket()

    def to_sp(self):
        if len(self) == 0:
            return ket()
        # return self.data[0]
        r = superposition()
        for sp in self.data:
            r.add_sp(sp)
        return r


# code for the yet to be added stored function rules:
# We have a stored learn rule:
# op |x> #=> foo |y> + bah |z> + some-action
# This stores the rule: "foo |y> + bah |z> + some-action"
# without processing it at learn time.
# Then it activates later when we do: op |x>  (where |x> is self_object)
# However, we don't want it to activate when we do a dump rule
# Going to take some work to implement, but let's start with a class:
# Baring any bugs, I think it is working!
class stored_rule(object):
    def __init__(self, rule):  # rule should be a string.
        self.rule = rule
        logger.debug("in stored_rule class: just stored: " + rule)

    def type(self):  # not 100% we need this, but no harm in putting it in anyway.
        return "stored rule"

    def display(self, exact=False):  # we don't need exact, but we do need to handle display with 1 parameter.
        return self.rule

    def readable_display(self):
        return "# " + self.rule

    def __str__(self):
        return self.display()

    def __len__(self):  # not sure what to return. so 1 sounds good for now.
        return 1

        # where currently self_object is a string. Breaks even with ket, let alone sp.

    # eventually I want support for all three cases.
    def activate(self, context, op, self_object=None):
        try:
            # return extract_compound_superposition(context,self.rule,self_label)[0] # how does return work in try/except?
            # return extract_compound_sequence(context, self.rule, self_label)
            return process_stored_rule(context, self.rule, self_object)
        except Exception as e:  # works fine.
            logger.warning("FYI: except in stored_rule\nReason: %s" % e)
            return superposition()

    def multiply(self, value):
        return self  # will probably do a better job of multiplication later. Is it even used?

    # 14/1/2016:
    def add(self, value):
        return self  # will probably do a better job of addition later. Is it even used?

    def add_sp(self, sp):  # just for now. Tweak later.
        if type(sp) in [stored_rule]:
            self.rule += ' + ' + sp.rule
        if type(sp) in [ket, superposition]:
            self.rule += ' + ' + str(sp)

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
    def __init__(self, rule):  # rule should be a string.
        self.rule = rule
        logger.debug("in memoizing_rule class: just stored: " + rule)

    def type(self):  # not 100% we need this, but no harm in putting it in anyway.
        return "memoizing stored rule"

    def display(self, exact=False):  # we don't need exact, but we do need to handle display with 1 parameter.
        return self.rule

    def readable_display(self):
        return "! " + self.rule

    def __str__(self):
        return self.display()

    def __len__(self):  # not sure what to return. so 1 sounds good for now.
        return 1

        # where currently self_object is a string. Breaks even with ket, let alone sp.

    # eventually I want support for all three cases.
    def activate(self, context, op, self_label):
        try:
            # resulting_rule = extract_compound_superposition(context,self.rule,self_label)[0] # how does return work in try/except?
            resulting_rule = extract_compound_sequence(context, self.rule, self_label)
            context.learn(op, self_label, resulting_rule)
            return resulting_rule
        except Exception as e:
            logger.warning("FYI: except in memoizing_rule\nReason: %s" % e)
            return superposition()

    def multiply(self, value):
        return self  # will probably do a better job of multiplication later.

    # 14/1/2016:
    def add(self, value):
        return self  # will probably do a better job of addition later.


def label_descent(x):  # can we optimize this at all? Does it matter?
    logger.info("ket: " + x)
    result = [x]
    if x == "*":
        return result
    if x.endswith(": *"):
        x = x[:-3]
    while True:
        try:
            x, null = x.rsplit(": ", 1)
            result.append(x + ": *")
        except:
            result.append("*")
            return result


class NewContext(object):
    def __init__(self, name):
        self.name = name
        self.ket_rules_dict = OrderedDict()
        self.sp_rules_dict = OrderedDict()
        self.supported_operators_dict = OrderedDict()
        self.learn('', 'context', 'context: ' + self.name)

    def set(self, name):  # not 100% sure this is the best way, or correct.
        self.name = name  # BTW, it is intended to erase what is currently defined for the current context.
        self.ket_rules_dict = OrderedDict()
        self.sp_rules_dict = OrderedDict()
        self.supported_operators_dict = OrderedDict()
        self.learn('', 'context', 'context: ' + self.name)

    def reset(self, name):
        self.set(name)

    def context_name(self):
        return self.name

    # op is a string
    # label is a string or a ket
    # rule can be anything
    # add_learn is either True or False
    #
    def learn(self, op, label, rule, add_learn=False, seq_learn=False ):
        # some prelims:
        if op == "supported-ops":  # never learn "supported-ops", it is auto-generated and managed
            return
        if type(label) is ket:  # label is string. if ket, convert back to string
            label = label.label
        if type(rule) is str:  # rule is assumed to be ket, superposition, or stored rule (maybe fast sp too).
            rule = ket(rule)  # if string, cast to ket

        if type(rule) is list:  # if list, cast to superposition  # do we even use this branch?
            r = superposition()
            for x in rule:
                if type(x) in [int, float]:
                    r.add("number: " + str(x))
                elif type(x) is str:
                    r.add(x)
            rule = r

        if len(rule) == 0:  # do not learn rules that are |>
            return

        self.supported_operators_dict[op] = True  # learn supported operators in this context

        if label not in self.ket_rules_dict:
            self.ket_rules_dict[label] = OrderedDict()
            self.ket_rules_dict[label]["supported-ops"] = superposition()
        self.ket_rules_dict[label]["supported-ops"].max_add("op: " + op)
        if add_learn:
            if op not in self.ket_rules_dict[label]:
                self.ket_rules_dict[label][op] = sequence()  # this breaks add_learn for stored_rules, and memoizing_rules. Do we want to fix it?
            self.ket_rules_dict[label][op].tail_add_seq(rule)  # maybe change to something else in the future.
        elif seq_learn:
            if op not in self.ket_rules_dict[label]:
                self.ket_rules_dict[label][op] = sequence()
            self.ket_rules_dict[label][op] += rule
        else:
            self.ket_rules_dict[label][op] = rule

    def add_learn(self, op, label, rule):
        return self.learn(op, label, rule, add_learn=True)  # corresponds to "op |x> +=> |y>"

    def seq_learn(self, op, label, rule):
        return self.learn(op, label, rule, add_learn=False, seq_learn=True)  # corresponds to "op |x> .=> |y>"

    # op is a string, or a ket in form |op: some-operator>
    # label is a string or a ket
    #
    def recall(self, op, label, active=False):
        # some prelims:
        if type(op) is ket:
            op = op.label[4:]  # map |op: age> to "age"
        if type(label) is ket:
            coeff = label.value
            ket_label = label.label
        else:
            coeff = 1
            ket_label = label
        #    coeff = 1                                  # use this to switch off the multiply(coeff) feature

        if op == 'supported-ops':
            if ket_label in self.ket_rules_dict:
                if op in self.ket_rules_dict[ket_label]:
                    return self.ket_rules_dict[ket_label][op]
            else:
                return ket()

        match = False
        for trial_label in label_descent(ket_label):
            if trial_label in self.ket_rules_dict:
                if op in self.ket_rules_dict[trial_label]:
                    rule = self.ket_rules_dict[trial_label][op]
                    match = True
                    break
        if not match:
            logger.info("%s |%s> not found" % (op, ket_label))
            rule = ket()

        if active and type(rule) in [stored_rule, memoizing_rule]:
            rule = rule.activate(self, op, ket(ket_label, coeff))
        else:
            rule = rule.multiply(coeff)
        return rule

    # op is a string
    # label is a string or a ket
    # rule can be string (which is cast to ket), ket, superposition, sequence, stored_rule, memoizing_rule
    # add_learn is either True or False
    #
    def seq_fn_learn(self, op, label, rule, add_learn=False):  # op (*) => |y>. Note, seq_fn rules have higher precedence than ket rules.
        # some prelims:                                        # also, op (*,*) and op (*,*,*)
        if op == "supported-ops":  # never learn "supported-ops", it is auto-generated and managed
            return
        if type(label) is ket:  # label is string. if ket, convert back to string
            label = label.label
        if type(rule) is str:  # rule is assumed to be ket, superposition, or stored rule (maybe fast sp too).
            rule = ket(rule)  # if string, cast to ket
        if len(rule) == 0:  # do not learn rules that are |>
            return

        if label not in self.sp_rules_dict:
            self.sp_rules_dict[label] = OrderedDict()
            self.sp_rules_dict[label]["supported-ops"] = superposition()
        self.sp_rules_dict[label]["supported-ops"].max_add("op: " + op)
        if not add_learn:
            self.sp_rules_dict[label][op] = rule
        else:
            if op not in self.sp_rules_dict[label]:
                self.sp_rules_dict[label][op] = superposition()
            self.sp_rules_dict[label][op].clean_add(rule)

    def seq_fn_add_learn(self, op, label, rule):          # corresponds to "op (*) +=> |y>"
        return self.seq_fn_learn(op, label, rule, True)  # is it even used anywhere? Does it even make sense?

    # op is a string, or a ket in form |op: some-operator>
    # seq_list is a list of sequences
    #
    def seq_fn_recall(self, op, seq_list, active=False):  # work in progress ...
        # some prelims:
        if type(op) is ket:
            op = op.label[4:]  # map |op: age> to "age"
        if op == 'supported-ops':
            return ket()

        if type(seq_list) is str:
            ket_label = seq_list  # should this be: ket_label = '*'? Would that break dump?
        elif type(seq_list) is list:
            if len(seq_list) == 2:  # first element in seq_list is input-seq
                ket_label = '*'
            elif len(seq_list) == 3:
                ket_label = '*,*'
            elif len(seq_list) == 4:
                ket_label = '*,*,*'
            elif len(seq_list) == 5:
                ket_label = '*,*,*,*'

        match = False  # If/when I implement op(*,*) et al, I need a tidy way to handle stored rules and |_self1> vs |_self2> etc! No idea how to do that currently.
        if ket_label in self.sp_rules_dict:
            if op in self.sp_rules_dict[ket_label]:
                rule = self.sp_rules_dict[ket_label][op]
                match = True

        if not match:
            logger.debug("%s (*) not found" % (op))  # tweak later! Probably want to switch this off completely once testing is done.
            rule = ket()

        if active:
            #      rule = rule.activate(self,op,sp)        # how handle op (*) #=> foo |_self> ??  op (|a> + |b>) returns foo (|a> + |b>)
            #    return rule.multiply(coeff)              # I'm not sure multiply(coeff) makes sense for seq_fn_recall().
            if type(rule) in [memoizing_rule, stored_rule]:
                try:
                    # logger.info('rule: %s' % rule)
                    # logger.info('seq: %s' % [str(x) for x in seq_list])
                    # resulting_rule = extract_compound_sequence(self, rule.rule , seq_list)
                    resulting_rule = rule.activate(self, op, seq_list)
                    # logger.info('resulting_rule: %s' % resulting_rule)
                except Exception as e:
                    resulting_rule = ket()
                    logger.warning("seq_fn_recall: except while processing stored_rule: %s" % e)
                # if type(rule) is memoizing_rule:
                #  self.seq_fn_learn(op,sp,resulting_rule)
                rule = resulting_rule
        return rule

    # op is a string, or a ket in form |op: some-operator>
    # label is a string or a ket
    #
    def dump_rule(self, op, label, exact=False):
        # some prelims:
        if type(op) is ket:
            op = op.label[4:]
        ket_name = label if type(label) is ket else ket(
            label)  # maybe tidy this. It is in dump, so no need to optimize really.

        rule = self.recall(op, label)
        rule_string = " => "
        if type(rule) == stored_rule:
            rule_string = " #=> "
        if type(rule) == memoizing_rule:
            rule_string = " !=> "

        star_new_line = ''
        if ket_name.label == '*':
            star_new_line = '\n'

        return op + " " + ket_name.display() + rule_string + rule.display(exact) + star_new_line

    # previously called dump_all_rules()
    def dump_ket_rules(self, label, exact=False):
        # some prelims:
        if type(label) is ket:
            ket_label = label.label
        else:
            ket_label = label

        if ket_label not in self.ket_rules_dict:
            return ""

        return "\n".join(self.dump_rule(op, label, exact) for op in self.ket_rules_dict[ket_label] if
                         exact or (op != "supported-ops"))

    def dump_sp_rule(self, op, label, exact=False):
        # some prelims:
        if type(op) is ket:
            op = op.label[4:]
        sp_name = label

        rule = self.seq_fn_recall(op, label)
        rule_string = " => "
        if type(rule) == stored_rule:
            rule_string = " #=> "
        if type(rule) == memoizing_rule:
            rule_string = " !=> "

        return op + " (" + sp_name + ")" + rule_string + rule.display(exact) + '\n'

    def dump_sp_rules(self, label, exact=False):
        if label not in self.sp_rules_dict:
            return ""
        return "\n".join(
            self.dump_sp_rule(op, label, exact) for op in self.sp_rules_dict[label] if exact or (op != "supported-ops"))

    # instead of dumping all the rules for a known ket, dump all the rules for all kets in the given superposition:
    # sp should be a ket, or superposition
    #
    def dump_multiple_ket_rules(self, seq, exact=False):  # Used in the console.
        if type(seq) is str:
            seq = ket(seq)
        return "\n\n".join(self.dump_ket_rules(x, exact) for x in seq.to_sp())

    # dump everything we know about the current context:
    def dump_universe(self, exact=False, show_context_header=True):  # I think this is right, but need to test it.
        if show_context_header:
            context_string = "|context> => |context: " + self.name + ">"
            sep = "\n----------------------------------------\n"
        else:
            context_string = ""
            sep = ""
        #    return sep + context_string + "\n\n" + "\n\n".join(self.dump_ket_rules(x,exact) for x in self.ket_rules_dict ) + sep
        result_string = ""
        if len(self.ket_rules_dict) > 0:
            # result_string += "\n\n" + "\n\n".join(self.dump_ket_rules(x,exact) for x in self.ket_rules_dict )
            result_string += "\n\n".join(self.dump_ket_rules(x, exact) for x in self.ket_rules_dict)
        if len(self.sp_rules_dict) > 0:
            result_string += "\n\n" + "\n\n".join(self.dump_sp_rules(x, exact) for x in self.sp_rules_dict)
        # return sep + context_string + result_string + sep
        return sep + result_string + sep

    # not 100% sure we want this, but I'll add it for now:
    # See, new_context() only has 1 context, so dump_multiverse() doesn't make a whole lot of sense.
    # context.multi_save(filename) is one reason I decided to add it.
    def dump_multiverse(self, exact=False):
        return self.dump_universe(exact)

        # create inverse for a single learn rule:

    # not sure we want this factored out. But leave as is for now.
    def create_single_learn_rule_inverse(self, op, label):
        # some prelims:
        if type(op) is ket:
            op = op.label[4:]
        if op.startswith("inverse-"):  # don't take the inverse of an inverse.
            return
        if type(label) is ket:
            label = label.label

        if label not in self.ket_rules_dict:
            return
        if op not in self.ket_rules_dict[label]:
            return

        rule = self.ket_rules_dict[label][op]
        if type(rule) is sequence:
            for sp in rule:
                for x in sp:
                    if x.label != "":
                        self.add_learn("inverse-" + op, x, label)
        if type(rule) in [ket, superposition]:  # don't learn inverse for stored_rules.
            for x in rule:
                if x.label != "":
                    self.add_learn("inverse-" + op, x, label)  # do we want ket(label)?
                    # also, NB: the add_learn. ie, slow with current superposition class.
                    # will be faster with fast_superposition class (which I will swap in eventually!)

    # create inverse for a single known ket:
    def create_ket_rules_inverse(self, label):
        if type(label) is ket:
            label = label.label
        if label not in self.ket_rules_dict:
            return

        for op in self.ket_rules_dict[label]:
            self.create_single_learn_rule_inverse(op, label)

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
                if type(rule) in [ket, superposition, fast_superposition]:  # don't learn inverse for stored_rules.
                    for x in rule:
                        if x.label != "":
                            self.add_learn("inverse-" + op, x, label)

    def create_inverse_op(self, op):
        if type(op) is ket:
            op = op.label[4:]
        for label in self.ket_rules_dict:
            if op in self.ket_rules_dict[label]:
                rule = self.ket_rules_dict[label][op]
                if type(rule) is sequence:
                    for sp in rule:
                        for x in sp:
                            if x.label != "":
                                self.add_learn("inverse-" + op, x, label)
                elif type(rule) in [ket, superposition]:  # don't learn inverse for stored_rules.
                    for x in rule:
                        if x.label != "":
                            self.add_learn("inverse-" + op, x, label)

    # do we need unlearn stuff?
    # unlearn rule, unlearn everything to do with a ket, and so on??
    # might not be that hard ...

    # what I'm calling pattern recognition.
    # just simm applied to relevant kets
    def pattern_recognition(self, pattern, op, t=0):  # this function should be quite easy to parallelize in the future.
        if type(op) is ket:
            op = op.label[4:]
        result = superposition()  # later swap out superposition to fast_superposition
        for label in self.ket_rules_dict:  # though when I do so I will probably rename fast_sp to plain superposition.
            if op in self.ket_rules_dict[label]:
                #        candidate_pattern = self.recall(op,label,True)                 # do we need active=True here? probably. OK. On a trial basis :)
                candidate_pattern = self.ket_rules_dict[label][op]  # currently is an exception if any patterns are stored rules! Fixed.
                if type(candidate_pattern) in [stored_rule, memoizing_rule]:
                    candidate_pattern = candidate_pattern.activate(self, op, label)  # do we really want to activate memoizing rules just by running similar-input[op]??
                #        value = silent_simm(pattern,candidate_pattern)
                #        value = fast_simm(pattern,candidate_pattern)                    # see if this speeds things up!
                value = aligned_simm_value(pattern, candidate_pattern)
                if value > t:  # "value >= t" instead?
                    result.add(label, value)
        return result.coeff_sort()

    # essentially identical in structure to pattern_recognition.
    # I wonder if they should be merged into one more generic function?? Not for now, at least.
    def map_to_topic(self, e, op, t=0):
        if type(op) is ket:
            op = op.label[4:]
        result = superposition()  # later swap out superposition to fast_superposition
        for label in self.ket_rules_dict:
            if op in self.ket_rules_dict[label]:
                #        frequency_list = self.recall(op,label,True)                    # do we need active=True here? probably. OK. On a trial basis :)
                frequency_list = self.ket_rules_dict[label][op]  # this cut runtime in half!
                if type(frequency_list) in [stored_rule, memoizing_rule]:
                    frequency_list = frequency_list.activate(self, op, label)  # do we really want to activate memoizing rules just by running find-topic[op]??
                value = normed_frequency_class_value(e, frequency_list)
                if value > t:  # "value >= t" instead?
                    #result.data.append(ket(label, value))  # "result += ket(label,value)" when swap in fast_superposition
                    result.add(label, value)
        return result.normalize(100).coeff_sort()


    # given an operator, return superposition of kets that support that operator:
    # slightly weird we have this here, and then a wrapper around it in the functions code, and this latter is what the processor uses.
    #
    # 22/2/2015 tweak: relevant_kets(self,"*") returns all known kets.
    def relevant_kets(self, op):
        result = superposition()
        if op == "*":
            for label in self.ket_rules_dict:
                result.add(label)
        else:
            for label in self.ket_rules_dict:
                if op in self.ket_rules_dict[label]:
                    result.add(label)  # "result += ket(label)" when swap in fast_sp
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
    def starts_with(self, e):
        label = e.label
        #    if len(label) == 0:
        #      return ket("",0)
        #    if label[-1] != "*":
        #      return e
        #    label = label.rstrip("*").rstrip(": ")
        result = superposition()
        for trial_label in self.ket_rules_dict:
            if trial_label.startswith(label):
                result.add(trial_label)
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
    def pretty_print_ket(self, one):  # one is a ket
        label = one.label if type(one) == ket else one
        head = "  " + label + "\n"
        frame = ""
        op_list = list(self.ket_rules_dict[label])
        if len(op_list) != 0:
            max_len = max(len(op) for op in op_list)
            sep = ": "
            frame = "\n".join(
                "  " + op.rjust(max_len) + sep + self.recall(op, label).readable_display() for op in op_list) + "\n"
        return head + frame

    def display_seq(self, seq):  # seq is a ket, superposition, or sequence
        return "\n".join(self.pretty_print_ket(x) for x in seq.to_sp())

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
            count_label = - 1  # we subtract 1 because we don't want to count the supported-ops term.
            for op in self.ket_rules_dict[label]:
                count_label += 1
                rule = self.recall(op, label)  # do we need "active=True" here? Probably not.
                if type(rule) in [ket, superposition, fast_superposition]:
                    result += rule.apply_sigmoid(clean)  # this will auto-speed up once we swap in fast_superpositions.
            result += ket(label, count_label)
        return result.coeff_sort()


    def save(self, filename, exact_dump=True):  # we need to test this. Looks right.
        try:
            file = open(filename, 'w')
            file.write(self.dump_universe(exact_dump))
            file.close()
        except:
            logger.info("failed to save: " + filename)

    def append_save(self, filename, exact_dump=True):  # we need to test this. Looks right.
        try:
            file = open(filename, 'a')
            file.write(self.dump_universe(exact_dump, False))
            file.close()
        except:
            logger.info("failed to append save: " + filename)

    def multi_save(self, filename, exact_dump=True):  # we need to test this. I think it is working.
        try:
            file = open(filename, 'w')
            file.write(self.dump_multiverse(exact_dump))  # though here in new_context() dump_multiverse() is identical to dump_universe().
            file.close()  # Maybe just set multi_save() as a wrapper around ordinary save, to make it clearer?
        except:
            logger.info("failed to multi save: " + filename)

    def old_load(self, filename):  # BUG: doesn't set the context properly. Not 100% sure why, yet. I think it is related to C.set("changed context")
        try:  # cool! I implemented new_context().set and seems to work now.
            with open(filename, 'r') as f:
                for line in f:
                    if line.startswith("exit sw"):  # use "exit sw" as the code to stop processing a .sw file.
                        return  # maybe move try/except to around parse_rule_line() instead of entire file?
                    # parse_rule_line(self,line)             # this is broken! bug found when loading fragment-document.sw fragments
                    process_sw_file(self, line)  # this is broken! bug found when loading fragment-document.sw fragments
        except Exception as e:
            logger.info("failed to load: %s\nReason: %s" % (filename, e))

    def load(self, filename):
        try:
            with open(filename, 'r') as f:
                text = f.read()
                # logger.info('load text: %s' % text)
                process_sw_file(self, text)
        except Exception as e:
            logger.info("failed to load: %s\nReason: %s" % (filename, e))

    # 3/12/2015: new feature context.print_universe() and context.print_multiverse()
    def print_universe(self, exact_dump=False):
        print(self.dump_universe(exact_dump))

    def print_multiverse(self, exact_dump=False):
        print(self.dump_multiverse(exact_dump))


class ContextList(object):
    def __init__(self, name):
        self.name = name
        c = NewContext(name)
        self.data = [c]
        self.index = 0

    def reset(self, name):  # maybe use __init__ instead?
        self.name = name
        c = NewContext(name)
        self.data = [c]
        self.index = 0

    def set(self, name):  # maybe write a set_index, where you specify index number, instead of context name
        previous_context_name = self.context_name()
        match = False
        for k, context in enumerate(self.data):
            if context.name == name:
                self.index = k
                match = True
                break
        if not match:
            c = NewContext(name)
            self.data.append(c)
            self.index = len(self.data) - 1
        self.data[self.index].learn('previous', 'context', 'context: ' + previous_context_name)

    def show_context_list(self):  # maybe include a count of the number of kets known to that context
        text = "context list:\n"
        for k, context in enumerate(self.data):
            pre = "* " if k == self.index else "  "
            text += pre + context.name + " (" + str(len(context.ket_rules_dict)) + ")\n"
        return text

    # new 12/2/2015:
    # assumes k is an integer:
    def set_index(self, k):
        previous_context_name = self.context_name()
        if k < 0 or k >= len(self.data):
            return False
        self.index = k
        self.data[self.index].learn('previous', 'context', 'context: ' + previous_context_name)
        return True

    def show_context_list_index(self):
        text = "context list:\n"
        for k, context in enumerate(self.data):
            pre = "* " if k == self.index else "  "
            text += " " + str(k) + ") " + pre + context.name + " (" + str(len(context.ket_rules_dict)) + ")\n"
        return text

    def context_name(self):
        return self.data[self.index].context_name()

    def learn(self, op, label, rule, add_learn=False):
        self.data[self.index].learn(op, label, rule, add_learn)

    def add_learn(self, op, label, rule):
        self.data[self.index].add_learn(op, label, rule)

    def seq_learn(self, op, label, rule):
        self.data[self.index].seq_learn(op, label, rule)

    def recall(self, op, label, active=False):
        return self.data[self.index].recall(op, label, active)

    def seq_fn_learn(self, op, label, rule, add_learn=False):
        self.data[self.index].seq_fn_learn(op, label, rule, add_learn)

    def sp_add_learn(self, op, label, rule):
        self.data[self.index].sp_add_learn(op, label, rule)

    def seq_fn_recall(self, op, label, active=False):
        return self.data[self.index].seq_fn_recall(op, label, active)

    def dump_ket_rules(self, label, exact=False):
        return self.data[self.index].dump_ket_rules(label, exact)

    def dump_multiple_ket_rules(self, label, exact=False):  # is this really a label here, or a sp?
        return self.data[self.index].dump_multiple_ket_rules(label, exact)

    def display_seq(self, seq):
        return self.data[self.index].display_seq(seq)

    def display_all(self):
        return self.data[self.index].display_all()

    def to_freq_list(self):
        return self.data[self.index].to_freq_list()  # later rewrite so it returns results from all context's.

    # make the all context-to-freq it's own function.
    def multiverse_to_freq_list(self):
        result = superposition()
        for context in self.data:
            result += context.to_freq_list()
        return result

    def dump_universe(self, exact=False):
        return self.data[self.index].dump_universe(exact)

    def create_universe_inverse(self):
        self.data[self.index].create_universe_inverse()

    def create_multiverse_inverse(self):
        for context in self.data:
            context.create_universe_inverse()

    def create_inverse_op(self, op):
        self.data[self.index].create_inverse_op(op)

    def pattern_recognition(self, pattern, op, t=0):
        return self.data[self.index].pattern_recognition(pattern, op, t)

    # currently unimplemented. It was dropped from the recent new_context() class work. Maybe re-instate it?
    #  def verbose_pattern_recognition(self,pattern,op="pattern"):
    #    return self.data[self.index].verbose_pattern_recognition(pattern,op)

    def map_to_topic(self, e, op, t=0):
        return self.data[self.index].map_to_topic(e, op, t)

    def relevant_kets(self, op):
        return self.data[self.index].relevant_kets(op)

    # 9/2/2016
    def supported_operators(self):
        return self.data[self.index].supported_operators()

    #  def list_kets(self,e):
    #    return self.data[self.index].list_kets(e)
    # renames to starts-with
    def starts_with(self, e):
        return self.data[self.index].starts_with(e)

    def global_recall(self, op, label):  # where do we even use this?
        result = superposition()  # does it need active=True too?
        for context in self.data:
            result += context.recall(op, label)
        return result

    def dump_multiverse(self, exact=False):
        result = ""
        for context in self.data:
            result += context.dump_universe(exact)
        return result

    def save(self, filename, exact_dump=True):
        return self.data[self.index].save(filename, exact_dump)

    def append_save(self, filename, exact_dump=True):
        return self.data[self.index].append_save(filename, exact_dump)

    def multi_save(self, filename, exact_dump=True):  # we need to test this. I think it is working.
        try:
            file = open(filename, 'w')
            file.write(self.dump_multiverse(exact_dump))
            file.close()
        except:
            logger.info("failed to multi save: " + filename)

    def line_load(self, filename):  # BUG: doesn't set the context properly. Not 100% sure why, yet. I think it is related to C.set("changed context")
        try:  # Well, here in context_list() it works just fine! C.load("sw-examples/fib-play.sw"); print(C.dump_multiverse())
            with open(filename, 'r') as f:
                for line in f:
                    if line.startswith("exit sw"):  # use "exit sw" as the code to stop processing a .sw file.
                        return
                    process_sw_file(self, line)  # later maybe process entire file at once. Not sure which method is faster.
        except Exception as e:
            logger.info("ContextList failed to line_load: " + filename)
            logger.info('reason: %s' % e)

    def load(self, filename):
        try:
            with open(filename, 'r') as f:
                text = f.read()
                process_sw_file(self, text)
        except Exception as e:
            logger.info("ContextList failed to load: %s\nreason: %s" % (filename, e))

    # 3/12/2015: new feature context.print_universe() and context.print_multiverse()
    def print_universe(self, exact_dump=False):
        print(self.data[self.index].dump_universe(exact_dump))

    def print_multiverse(self, exact_dump=False):
        print(self.dump_multiverse(exact_dump))


from parsley import makeGrammar
from string import ascii_letters
# from semantic_db.processor_tables import *
from semantic_db.functions import *
from semantic_db.sigmoids import *
from semantic_db.usage_tables import *

def valid_op(op):  # do we still need this now we have a better parser?
    if not op[0].isalpha() and not op[0] == '!':
        return False
    return all(c in ascii_letters + '0123456789-+!?.' for c in op)


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
op_char = anything:x ?(x.isalpha() or x.isdigit() or x in '-+!?.:')
simple_op = op_start_char:first <op_char*>:rest -> first + rest
filtered_char = anything:x ?(x not in '[]|><') -> x
filtered_parameter_string = '"' ( ~'"' filtered_char)*:c '"' -> ''.join(c)
#parameters = (fraction | simple_op | filtered_parameter_string | '\"\"' | '*'):p -> str(p)
parameters = (fraction | simple_op | filtered_parameter_string | '\"\"' | '*'):p -> p

compound_op = simple_op:the_op '[' parameters:first (',' ws parameters)*:rest ']' -> ['c_op', the_op] + [first] + rest
#function_op = simple_op:the_op '(' ws literal_sequence:first (',' ws literal_sequence)*:rest ws ')' -> ['f_op', the_op] + [first] + rest
function_op = simple_op:the_op '(' ws full_compound_sequence:first (',' ws full_compound_sequence)*:rest ws ')' -> ['f_op', the_op] + [first] + rest
# not sure if putting ws in here before the '(' breaks anything? Perhaps more complex operator sequences? Yup, breaks: 'op8 (op7) op6 |fish>'
# so, can we easily fix it?
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

symbol_single_compound_sequence = ~'+=>' ~'.=>' ws op_symbol:symbol ws single_compound_sequence:seq -> (symbol, seq)
full_compound_sequence = ws (op_symbol | -> '+'):symbol single_compound_sequence:first ws symbol_single_compound_sequence*:rest ws -> [(symbol, first)] + rest

compiled_compound_sequence = full_compound_sequence:seq -> compile_compound_sequence(context, seq)

new_line = ('\r\n' | '\r' | '\n')
#char = :c ?(is_not_newline(c)) -> c
char = ~new_line anything
line = <char*>:s -> s
#line = <~new_line anything>*:s -> "".join(s)
multiline = '  ' line:first new_line (~new_line multiline)*:rest -> '\\n  ' + first + ''.join(rest)    
comment = ( '-'+ line | ws new_line)
#object = (naked_ket | '(*)' | '(*,*)' | '(*,*,*)' | full_compound_sequence ):obj -> obj
object = (naked_ket | '(*)' | '(*,*)' | '(*,*,*)' | '(*,*,*,*)' | full_compound_sequence ):obj -> obj
single_stored_rule = ws (simple_op | -> ''):prefix_op ws object:obj ws ('#=>' | '!=>'):rule_type ws line:s -> learn_stored_rule(context, prefix_op, obj, rule_type, s)
stored_rule = multi_stored_rule
multi_stored_rule = ws (simple_op | -> ''):prefix_op ws object:obj ws ('#=>' | '!=>'):rule_type ws (ws new_line multiline | line):s -> learn_stored_rule(context, prefix_op, obj, rule_type, s)
#memoizing_rule = ws (simple_op | -> ''):prefix_op ws object:obj ws '!=>' ws line:s -> learn_memoizing_rule(context, prefix_op, obj, s)
#learn_rule =  ws (simple_op | -> ''):prefix_op ws object:obj ws ('=>' | '+=>'):rule ws compiled_compound_sequence:seq -> learn_standard_rule(context, prefix_op, obj, rule, seq)
learn_rule =  ws (simple_op | -> ''):prefix_op ws object:obj ws ('=>' | '+=>' | '.=>'):rule_type ws full_compound_sequence:parsed_seq -> learn_standard_rule(context, prefix_op, obj, rule_type, parsed_seq)
recall_rule = ws (simple_op | "\'\'" ):prefix_op ws object:obj -> recall_rule(context, prefix_op, obj)

sw_file = (comment | learn_rule | multi_stored_rule )*
#sw_file = (comment | compiled_compound_sequence | learn_rule | multi_stored_rule )*
process_rule_line = (learn_rule | stored_rule | compiled_compound_sequence | new_line | comment)
stored_rule_line = (learn_rule | stored_rule | full_compound_sequence ):seq -> seq
"""


def float_int(x):
    if x.is_integer():
        return int(x)
    return x


def ket_calculate(start, pairs):
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


def process_operators(context, ops, seq, self_object=None):
    if len(ops) == 0:
        return seq
    # python_code = ''
    for op in reversed(ops):
        if type(op) is list:  # found either a compound-op, a function-op or bracket-ops
            my_print('op[0]', op[0])
            if op[0] is 'c_op':
                my_print('compound_op')
                # the_op = op[1]
                # parameters = ','.join(op[2:])
                the_op, *parameters = op[1:]
                if the_op not in compound_table:
                    logger.debug(the_op + " not in compound_table")
                    seq = sequence([])
                else:
                    # python_code = compound_table[the_op].format(parameters) # probably risk of injection attack here. Also, this is the place to change compound function invoke method.
                    # seq = eval('seq' + python_code)
                    method_name, str_fn_name, use_context = compound_table[the_op]  # heh, so we succesfully removed eval, but at what cost! Doing this for every invoke will hurt!
                    full_params = parameters  # can we preprocess and produce a compiled_compound_table?
                    if use_context is 'context':  #
                        full_params = [context] + full_params
                    if str_fn_name is not '':
                        fn_name = globals()[str_fn_name]  # Is this use of globals a security risk too? Quite possibly :(
                        full_params = [fn_name] + full_params
                    # print('method_name: %s' % str(method_name))
                    # print('use_context: %s' % use_context)
                    # print('str_fn_name: %s' % str_fn_name)
                    # print('full_params: %s' % str(full_params))

                    method = getattr(seq, method_name)
                    seq = method(*full_params)

            elif op[0] is 'f_op':
                my_print('function_op')
                null, fnk, *data = op
                my_print('fnk', fnk)
                my_print('data', data)
                # print('f_op seq: %s' % seq)

                # python_code = ''
                our_fn = ''
                seq_list = [compile_compound_sequence(context, x, self_object) for x in data]
                # my_print('str_seq_list', [str(x) for x in seq_list])

                if len(data) == 1:  # 1-parameter function:
                    if fnk in whitelist_table_1:
                        # python_code = "%s(*seq_list)" % whitelist_table_1[fnk]
                        our_fn = globals()[whitelist_table_1[fnk]]
                    elif False:  # is this branch still correct? How test?
                        # the_seq = compile_compound_sequence(context, data[0], self_object)
                        the_seq = seq_list[0]
                        seq = process_operators(context, [fnk], the_seq, self_object)
                elif len(data) == 2:  # 2-parameter function:  # should this be elif len(data) ... ?
                    if fnk in whitelist_table_2:  # still not sure if I want whitelist_table and context_whitelist_table separate, or pass context to everything.
                        # python_code = "%s(*seq_list)" % whitelist_table_2[fnk]
                        our_fn = globals()[whitelist_table_2[fnk]]
                    elif fnk in context_whitelist_table_2:
                        # python_code = "%s(context, *seq_list)" % context_whitelist_table_2[fnk]
                        seq_list = [context] + seq_list
                        our_fn = globals()[context_whitelist_table_2[fnk]]
                elif len(data) == 3:  # 3-parameter function:
                    if fnk in whitelist_table_3:
                        # python_code = "%s(*seq_list)" % whitelist_table_3[fnk]
                        our_fn = globals()[whitelist_table_3[fnk]]
                    elif fnk in context_whitelist_table_3:
                        # python_code = "%s(context, *seq_list)" % context_whitelist_table_3[fnk]
                        seq_list = [context] + seq_list
                        our_fn = globals()[context_whitelist_table_3[fnk]]
                elif len(data) == 4:  # 4-parameter function:
                    if fnk in whitelist_table_4:
                        # python_code = "%s(*seq_list)" % whitelist_table_4[fnk]
                        our_fn = globals()[whitelist_table_4[fnk]]
                if our_fn is not '':
                    # print('our_fn: %s' % str(our_fn))
                    seq = our_fn(seq, *seq_list)
                else:
                    seq = context.seq_fn_recall(fnk, [seq] + seq_list, active=True)
                # seq_list = [compile_compound_sequence(context, x, self_object) for x in data]
                # my_print('str_seq_list', [str(x) for x in seq_list])
                # if len(python_code) > 0:
                #  my_print("whitelist_table: python code", python_code)
                #  seq = eval(python_code)                                                       # can we implement this without using eval??
                # else:
                #  seq = context.seq_fn_recall(fnk, seq_list, True)
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
                else:  # finish this branch!
                    for sp in seq:  # haven't handled sequences yet. eg, (op3 _ op2) (|x> . |y> + |z>)
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
                                    new_seq.merge_seq(the_seq)  # do we need distributed_merge_seq here too? I suspect yes.
                                elif symbol == '__':
                                    new_seq.merge_seq(the_seq, ' ')
                                elif symbol == '.':
                                    new_seq += the_seq
                                my_print('new_seq', str(new_seq))
                            r.add_seq(new_seq)
                        seq = r
        elif type(op) is tuple:  # powered op found.
            tuple_op, power = op
            my_print('tuple_op', tuple_op)
            my_print('power', power)
            for _ in range(power):  # is there a better way to implement this?
                seq = process_operators(context, [tuple_op], seq, self_object)
        elif type(op) in [int, float]:
            seq = seq.multiply(op)
        elif op == '-':
            seq = seq.multiply(-1)  # is this branch still used anywhere?
        elif op == "\"\"":
            seq = seq.apply_op(context, "")
        elif op in built_in_table:
            method = getattr(seq, built_in_table[op])
            seq = method()
        elif op in sigmoid_table:
            our_fn = globals()[sigmoid_table[op]]
            seq = seq.apply_sigmoid(our_fn)
        elif op in fn_table:  # left out code for fn_table2 for now.
            our_fn = globals()[fn_table[op]]
            seq = seq.apply_fn(our_fn)
        elif op in sp_fn_table:
            our_fn = globals()[sp_fn_table[op]]
            seq = seq.apply_sp_fn(our_fn)
        elif op in seq_fn_table:
            our_fn = globals()[seq_fn_table[op]]
            seq = seq.apply_seq_fn(our_fn)
        elif op in ket_context_table:
            our_fn = globals()[ket_context_table[op]]
            seq = seq.apply_fn(our_fn, context)
        elif op in sp_context_table:                  # I don't think this is used anywhere at the moment.
            our_fn = globals()[sp_context_table[op]]
            seq = seq.apply_sp_fn(our_fn, context)
        else:  # literal op found. Also means literal ops have lower priority than all other operator types. Be aware!
            logger.debug('literal op found: %s' % op)
            seq = seq.apply_op(context, op)
        #    else:
    #      python_code = process_single_op(op)
    #      if len(python_code) > 0:
    #        seq = eval('seq' + python_code)
    return seq


def compile_compound_sequence(context, compound_sequence, self_object=None):
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
        if type(object) is str:  # found a ket
            if object == '_self' and type(self_object) in [str, ket, superposition, sequence]:
                the_seq = sequence(self_object)
            elif object.startswith('_self') and type(self_object) is list:  # this branch needs to handle |_self> too.
                try:
                    position = int(object[5:])
                except:
                    position = 1
                try:
                    the_seq = sequence(self_object[position])
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
        # my_print('really final the_seq', str(the_seq))

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
            # print('__ seq: %s' % seq)
            # print('__ the_seq: %s' % the_seq)
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
    if one in ['(*)', '(*,*)', '(*,*,*)', '(*,*,*,*)']:  # seq_fn_learn rule found. Tidy later!
        one = one[1:-1]
        if rule_type == '#=>':
            context.seq_fn_learn(op, one, stored_rule(s))
        elif rule_type == '!=>':
            context.seq_fn_learn(op, one, memoizing_rule(s))
        return
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

    if op == 'supported-ops':  # don't learn supported-ops lines.
        return

    if one in ['(*)', '(*,*)', '(*,*,*)', '(*,*,*,*)']:  # seq_fn_learn rule found. Tidy later!
        one = one[1:-1]
        # seq = compile_compound_sequence(context, parsed_seq, one)
        seq = compile_compound_sequence(context, parsed_seq)  # I don't currently know how to handle rules like: foo (*) => |_self>
        my_print('sp seq', str(seq))
        if rule_type == '=>':
            context.seq_fn_learn(op, one, seq)
            return

    if type(one) is str:
        seq = compile_compound_sequence(context, parsed_seq, [ket(), one])
        my_print('seq', str(seq))

        if op == '' and one == 'context' and rule_type == '=>':
            name = seq.to_sp().label
            if name.startswith('context: '):
                context.set(name[9:])
        elif rule_type == '=>':
            context.learn(op, one, seq)
            return seq
        elif rule_type == '+=>':
            context.add_learn(op, one, seq)
            return seq
        elif rule_type == '.=>':
            context.seq_learn(op, one, seq)
            return seq
    elif type(one) is list:  # indirect learn rule found
        indirect_object = compile_compound_sequence(context, one)
        my_print('indirect learn object', str(indirect_object))
        seq = sequence([])
        for sp in indirect_object:
            for one in sp:
                seq = compile_compound_sequence(context, parsed_seq, [ket(), one])
                if rule_type == '=>':
                    context.learn(op, one, seq)
                elif rule_type == '+=>':
                    context.add_learn(op, one, seq)
                elif rule_type == '.=>':
                    context.seq_learn(op, one, seq)
        return seq


def recall_rule(context, op, one):
    return context.recall(op, one)


#  return ket(one).apply_op(context, op)

def extract_compound_sequence(context, unparsed_seq, self_object=None):  # need to make context explicit somewhere ... rather than a global....
    parsed_seq = op_grammar(unparsed_seq).full_compound_sequence()
    my_print('parsed_seq', parsed_seq)
    my_print('self_object', self_object)
    seq = compile_compound_sequence(context, parsed_seq, self_object)
    return seq


def process_sw_file(context, sw_text):
    op_grammar(sw_text).sw_file()


def process_input_line(context, line, x):
    try:
        return op_grammar(line).process_rule_line()
    except Exception as e:
        logger.info('failed to process line: %s\nReason: %s' % (line, e))
        return ket()


def process_stored_rule(context, unparsed_rule, self_object=None):
    if self_object is not None and '|__self' in unparsed_rule:
        if type(self_object) is list:
            str_self_object = [str(x) for x in self_object]
            unparsed_rule = unparsed_rule.replace('|__self>', ' (%s) ' % str_self_object[1])  # I hate this bit of code!! Please kill it!
            for k, x in enumerate(str_self_object):  # we need a cleaner way to handle |__self> and |__self3> rules!
                pattern = '|__self%s>' % str(k)
                unparsed_rule = unparsed_rule.replace(pattern, ' (%s) ' % x)  # I hate this bit of code!! Please kill it!
        else:
            if type(self_object) is str:
                str_self_object = '|' + self_object + '>'
            else:
                str_self_object = str(self_object)
            unparsed_rule = unparsed_rule.replace('|__self>', ' (%s) ' % str_self_object)  # I hate this bit of code!! Please kill it!
    # print('self_object: %s' % str(self_object))
    # print('unparsed stored rule: %s' % unparsed_rule)
    seq = sequence([])
    for line in unparsed_rule.splitlines():
        line = line.strip()
        # print('line: %s' % line)
        if line != '' and not line.startswith('--'):
            if line == '|>':
                seq = ket()
            else:
                parsed_seq = op_grammar(line).stored_rule_line()
                # print('parsed_seq: %s' % parsed_seq)
                if type(parsed_seq) in [ket, superposition, sequence]:
                    seq = parsed_seq
                elif type(parsed_seq) is list:
                    seq = compile_compound_sequence(context, parsed_seq, self_object)
    return seq


def is_not_newline(c):
    return c not in ['\r', '\n']


context = ContextList('global context')
# context = ''

bindings_dictionary = {
    'ket_calculate': ket_calculate,
    'compile_compound_sequence': compile_compound_sequence,
    'float_int': float_int,
    'learn_stored_rule': learn_stored_rule,
    #  'learn_memoizing_rule'           : learn_memoizing_rule,
    'learn_standard_rule': learn_standard_rule,
    'recall_rule': recall_rule,
    'context': context,
    'is_not_newline': is_not_newline,
}

op_grammar = makeGrammar(our_grammar, bindings_dictionary)


# copied from here:
# http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
def human_readable_size(num):
    for x in ['B ', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            if x == 'B ':
                return "%3.0f %s" % (num, x)
            else:
                return "%3.1f %s" % (num, x)
        num /= 1024.0


import time


# find the stats of a .sw file:
# Needs improving!
# works fine, though is hinting at getting slow for large sw files. Yeah. It is now very slow on my large sw collection.
def extract_sw_stats(file):
    try:
        stats = []
        context = ""
        count = 0
        with open(file, 'r') as f:
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
        print("failed to load:", file)
        return ""
