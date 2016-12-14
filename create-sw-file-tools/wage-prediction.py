#!/usr/bin/env python3

#######################################################################
# revist the wage prediction pattern recognition example
# first attempt here: 
# https://github.com/GarryMorrison/Feynman-knowledge-engine/blob/master/create-sw-file-tools/play_with_adult_wage_example.py
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-12-11
# Update: 2016-12-14
# Copyright: GPLv3
#
# Usage: ./wage-prediction.py
#
#######################################################################


import sys
from collections import OrderedDict
import random

sample_data = "data/adult/30-sample.data"
train_data = "data/adult/adult.data"
test_data = "data/adult/adult.test"

weight_up = 1.5
weight_down = 0.5
weights = [1,1,1,1,1,1,1,1,1,1,1,1,1,1]
#weights = [0.01668548583984375, 0.0296630859375, 1.1444091796875e-05, 2.53125, 0.7119140625, 25.62890625, 2.1357421875, 0.0007821321487426758, 0.03167635202407837, 0.2109375, 0.10546875, 0.01318359375, 0.2373046875, 0.11865234375]
good_weights = [0.01668548583984375, 0.0296630859375, 1.1444091796875e-05, 2.53125, 0.7119140625, 25.62890625, 2.1357421875, 0.0017597973346710205, 0.021117568016052246, 0.2109375, 0.10546875, 0.01318359375, 0.2373046875, 0.11865234375]
sample_size = 100


# define our bare-bones superposition class:
class superposition(object):
  def __init__(self):
#    self.dict = {}
    self.dict = OrderedDict()

  def __str__(self):
    list_of_kets = []
    for key,value in self.dict.items():
      if value == 1:
        s = "|%s>" % key
      else:
        s = "%s|%s>" % (value,key)
      list_of_kets.append(s)
    return " + ".join(list_of_kets)

  def __iter__(self):
    for key,value in self.dict.items():
      yield key, value

  def __len__(self):
    return len(self.dict)

  def add(self,str,value=1):
    if str in self.dict:
      self.dict[str] += float(value)
    else:
      self.dict[str] = float(value)

  def pair(self):                               # if the dict is longer than 1 elt, this returns a random pair
    for key,value in self.dict.items():         # presuming not using an OrderedDict
      return key, value

  def get_value(self,str):
    if str in self.dict:
      return self.dict[str]
    else:
      return 0

  def rescale(self,t=1):
    if len(self.dict) == 0:
      return superposition()
    the_max = max(value for key,value in self.dict.items())
    result = superposition()
    if the_max > 0:
      for key,value in self:
        result.dict[key] = t*self.dict[key]/the_max
    return result

  def normalize(self,t=1):
    if len(self.dict) == 0:
      return superposition()
    the_sum = sum(value for key,value in self.dict.items())
    result = superposition()
    if the_sum > 0:
      for key,value in self:
        result.dict[key] = t*self.dict[key]/the_sum
    return result

  def coeff_sort(self):
    r = superposition()
    for key,value in sorted(self.dict.items(), key=lambda x: x[1], reverse=True):
      r.add(key,value)
    return r

  def select_top(self,k):
    r = superposition()
    for i,(key,value) in enumerate(self.dict.items()):
      r.add(key,value)
      if i + 1 >= k:
        break
    return r

  def reweight(self, weights):
    r = superposition()
    for k, (key, value) in enumerate(self.dict.items()):
      r.add(key, value * weights[k] )
    return r

# maybe we should convert these sw_dict functions to a class?
def print_sw_dict(dict,op):
  for label,sp in dict.items():
    print("%s |%s> => %s" % (op,label,sp))

def print_sorted_sw_dict(dict,op):
  for label,sp in dict.items():
    print("%s |%s> => %s" % (op,label,sp.coeff_sort()))

def reweight_dict(dict, weights):
  new_dict = {}
  for label, sp in dict.items():
    new_dict[label] = sp.reweight(weights)
  return new_dict

def sample_dict(dict, sample_size):
  new_dict = {}
  for label, sp in random.sample(dict.items(), sample_size):
    new_dict[label] = sp
  return new_dict
  

# probably can optimize this more yet.
#
def fast_simm(A,B):
  if len(A) == 0 or len(B) == 0:
    return 0
  if len(A) == 1 and len(B) == 1:
    a_label, a_value = A.pair()
    b_label, b_value = B.pair()

    if a_label != b_label:                    # put a.label == '' test in here too?
      return 0
    a = max(a_value,0)                        # just making sure they are >= 0.
    b = max(b_value,0)
    if a == 0 and b == 0:                     # prevent div by zero.
      return 0
    return min(a,b)/max(a,b)
#  return intersection(A.normalize(),B.normalize()).count_sum()     # very slow version!

  # now calculate the superposition version of simm, while trying to be as fast as possible:
  try:
    merged = {}
    one_sum = 0
    one = {}
    for label,value in A:
      one[label] = value
      one_sum += value                     # assume all values in A are >= 0
      merged[label] = True                 # potentially we could use abs(elt.value)

    two_sum = 0
    two = {}
    for label,value in B:
      two[label] = value
      two_sum += value                     # assume all values in B are >= 0
      merged[label] = True

    # prevent div by zero:
    if one_sum == 0 or two_sum == 0:
      return 0

    merged_sum = 0
    for key in merged:
      if key in one and key in two:
        v1 = one[key]/one_sum
        v2 = two[key]/two_sum
        merged_sum += min(v1,v2)
    return merged_sum
  except Exception as e:
    print("fast_simm exception reason: %s" % e)

# I don't think we use this anywhere.
# pretty print a float:
def float_to_int(x,t=4):
  if float(x).is_integer():
    return str(int(x))
  return str(round(x,t))

# pretty print a table:
# table print tweaked from here: http://stackoverflow.com/questions/25403249/print-a-list-of-tuples-as-table
def print_table(table):
  max_length_column = []
  tuple_len = len(table[0])     # assume entire table has the same shape as the first row
  for i in range(tuple_len):
    max_length_column.append(max(len(e[i])+2 for e in table))
  for e in table:
    for i in range(tuple_len):
      print(e[i].ljust(max_length_column[i]), end='')
    print()


# return list version:
def pattern_recognition_list(dict,pattern,t=0):
  result = []
  for label,sp in dict.items():
    value = fast_simm(pattern,sp)       # if a clean superposition, then swap in faster_simm()
    if value > t:
      result.append((label,value))
  return result

# return superposition version:
def pattern_recognition_sp(dict,pattern,k):
  r = superposition()
  for label,sp in dict.items():
    value = fast_simm(pattern,sp)       # if a clean superposition, then swap in faster_simm()
    if value > 0:
      r.add(label,value)
  return r.coeff_sort().select_top(k)    # putting the select_top() statement here rather than later, doesn't seem to improve speed.

# return best-match version:
def pattern_recognition_best_match(dict, pattern):
  best_match = ""
  best_score = 0
  for label,sp in dict.items():
    if pattern.dict != sp.dict:
      similarity = fast_simm(pattern, sp)
      if similarity > best_score:
        best_match = label
        best_score = similarity
  return best_match, best_score


def learn_data(filename, node_name):
  data_dict = {}
  answer_dict = {}
  k = 0
  with open(filename, 'r') as f:
    for line in f:
      try:
        age,workclass,fnlwgt,education,education_num,marital_status,occupation,relationship,race,sex,capital_gain,capital_loss,hours_per_week,native_country,wage_class = line.strip().split(', ')
        k += 1
        r = superposition()
        r.add("age", age)                    # NB: age is a string, not a float. We auto-cast to float in the superposition class.
        r.add(workclass)
        r.add("fnlwgt", fnlwgt)
        r.add(education)
        r.add("education-num", education_num)
        r.add(marital_status)
        r.add(occupation)
        r.add(relationship)
        r.add(race)
        r.add(sex)
        r.add("capital-gain", capital_gain)
        r.add("capital-loss", capital_loss)
        r.add("hours-per-week", hours_per_week)
        r.add(native_country)

        # heh. adult.data uses "<=50K" and ">50K", while adult.test uses "<=50K." and ">50K."
        # tweak to fix that:
#        wage_class_sp = superposition()
#        wage_class = wage_class.rstrip('.')
#        if wage_class == "<=50K":
#          wage_class_sp.add("below-50K")
#        elif wage_class == ">50K":
#          wage_class_sp.add("above-50K")

        wage_class_str = ""
        wage_class = wage_class.rstrip('.')
        if wage_class == "<=50K":
          wage_class_str = "below-50K"
        elif wage_class == ">50K":
          wage_class_str = "above-50K"

        node = "%s %s" % (node_name, k)
        data_dict[node] = r
#        answer_dict[node] = wage_class_sp
        answer_dict[node] = wage_class_str

      except Exception as e:
        print("learn_data exception reason:", e)
  return data_dict, answer_dict


def first_find_score(data_dict, answer_dict):
  number_of_results = 10

  label, pattern = random.sample(data_dict.items(), 1)[0] 
  answer = answer_dict[label]
  print("label:",label)
  print("pattern:", pattern)
  print("answer:",answer)

  # find matching patterns:
  result = pattern_recognition_list(data_dict, pattern)

  # sort the results:
  sorted_result = sorted(result, key = lambda x: float(x[1]), reverse = True)[:number_of_results]

  # find discrimination:
  discrimination = sorted_result[0][1] - sorted_result[1][1]

  # find score:
  second_label = sorted_result[1][0]
  score = 0
  if str(answer) == str(answer_dict[second_label]):                     # do we really want answer_dict to return sp? Why not string? Fix later.
    score += 1

  print("discrimination:", discrimination)
  print("score:", score)
  result2 = pattern_recognition_best_match(data_dict, pattern) 
  print("compare:", result2)

  # format the results a little:
  return [(str(k+1), label , float_to_int(100*value), str(answer_dict[label]) ) for k,(label,value) in enumerate(sorted_result) ]



def find_score(data_dict, answer_dict):
  score_weights = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
#  score_weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
  count = 0
  simple_score = 0
  score = 0
  for label, pattern in data_dict.items():
    count += 1
    answer = answer_dict[label]

    # find matching patterns:
#    result = pattern_recognition_best_match(data_dict, pattern)
    result_list = pattern_recognition_list(data_dict, pattern)

    # sort the results:
    result = sorted(result_list, key = lambda x: float(x[1]), reverse = True)[1:10]
    result = [x[0] for x in result]

    if answer == answer_dict[result[0]]:
      simple_score += 1
    for k, result_label in enumerate(result):
#      print("k: %s answer: %s" % (k, answer_dict[result_label]) )
      if answer == answer_dict[result_label]:
        score += score_weights[k]
#        print("score_weight: %s" % score_weights[k] )
#    break
  print("%s / %s = %.3f" % (simple_score, count, 100 * simple_score / count) )
  return score


def find_weights(data_dict, answer_dict, weights, weight_up, weight_down, trials):
  print("weights:", weights)
  best_score = find_score(data_dict, answer_dict)
  sample_weights = weights[:]
  for i in range(trials):
    k = random.sample(range(len(weights)), 1)[0]
    w = random.sample([weight_up, weight_down], 1)[0]
    stored_weights = sample_weights[:]
    sample_weights[k] *= w
    print("%s:\tscore: %s\t k: %s\t w: %s\t weights: %s" % (i, 100*best_score, k, w, sample_weights))
    sample_data_dict = reweight_dict(data_dict, sample_weights)
    sample_score = find_score(sample_data_dict, answer_dict)
    if sample_score >= best_score:
      best_score = sample_score
    else:                                            # no improvement, so don't keep weights changes
      sample_weights = stored_weights
  return sample_weights


# test it works:
#data_dict, answer_dict = learn_data(sample_data, "sample")
#data_dict, answer_dict = learn_data(train_data, "train")
#data_dict, answer_dict = learn_data(test_data, "test")

#print_sw_dict(data_dict, "pattern")
#print_sw_dict(answer_dict, "answer")
#print("len data_dict:", len(data_dict))
#print("len answer_dict:", len(answer_dict))

#new_data_dict = reweight_dict(data_dict, weights)
#print_sw_dict(data_dict, "pattern")
#print_sw_dict(new_data_dict, "pattern")

#sample_data_dict = sample_dict(data_dict, 200)
#print_sw_dict(sample_data_dict, "pattern")
#sys.exit(0)

#result = first_find_score(data_dict, answer_dict)
#print_table(result)

#score1 = find_score(sample_data_dict, answer_dict)

#weights = [1,1,0.00001,1,1,1,1,1,1,1,1,1,1,1]
#new_data_dict = reweight_dict(sample_data_dict, weights)
#score2 = find_score(new_data_dict, answer_dict)

#weights = [0.75,1,0.000001,1,1,1,1,1,1,1,1,1,1,1]
#new_data_dict = reweight_dict(sample_data_dict, weights)
#print_sw_dict(new_data_dict, "pattern")
#score3 = find_score(new_data_dict, answer_dict)

#print("delta:", 100 * (score3 - score1) )

#result = first_find_score(new_data_dict, answer_dict)
#print_table(result)


#data_dict, answer_dict = learn_data(train_data, "train")
#sample_data_dict = sample_dict(data_dict, 200)
#print("score: %s" % find_score(sample_data_dict, answer_dict) )
#sys.exit(0)


# put it to work:
data_dict, answer_dict = learn_data(train_data, "train")
sample_data_dict = sample_dict(data_dict, 500)
new_weights = find_weights(sample_data_dict, answer_dict, weights, weight_up, weight_down, 300)

sample_data_dict = sample_dict(data_dict, 500)
new_weights = find_weights(sample_data_dict, answer_dict, new_weights, weight_up, weight_down, 200)

sample_data_dict = sample_dict(data_dict, 500)
new_weights = find_weights(sample_data_dict, answer_dict, new_weights, weight_up, weight_down, 200)



new_data_dict = reweight_dict(sample_data_dict, new_weights)

print("first result:")
find_score(sample_data_dict, answer_dict)

print("new_weights:", new_weights)
print("final result:")
find_score(new_data_dict, answer_dict)

result = first_find_score(new_data_dict, answer_dict)
print_table(result)

print("---------------")
sample_data_dict = sample_dict(data_dict, 10000)
print("first full result:")
find_score(sample_data_dict, answer_dict)

new_data_dict = reweight_dict(sample_data_dict, new_weights)
print("final full result:")
find_score(new_data_dict, answer_dict)

