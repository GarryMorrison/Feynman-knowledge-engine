#!/usr/bin/env python3

#######################################################################
# use sample adult data for testing pattern recognition
# url: https://archive.ics.uci.edu/ml/datasets/Adult
#
# Author: Garry Morrison
# Date: 2015-03-12
# Update:
# Copyright: GPLv3
#
# Usage:
#
# described here:
# http://write-up.semantic-db.org/94-harder-supervised-pattern-recognition-example.html
# http://write-up.semantic-db.org/95-some-wage-prediction-results.html
# http://write-up.semantic-db.org/119-the-full-wage-prediction-results.html
#
#######################################################################


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

C = context_list("adult wage pattern recognition")

short_sample = "data/adult/30-sample.data"
learning_data = "data/adult/adult.data"
test_data = "data/adult/adult.test"

def learn_data(C,filename,learning=True):
  k = 0
  with open(filename,'r') as f:
    for line in f:
      try:
        age,workclass,fnlwgt,education,education_num,marital_status,occupation,relationship,race,sex,capital_gain,capital_loss,hours_per_week,native_country,wage_class = line.strip().split(', ')
        k += 1
        r = ket("age",age) + ket(workclass) + ket("fnlwgt",fnlwgt) + ket(education) + ket("education-num",education_num) + ket(marital_status) + ket(occupation) 
        r += ket(relationship) + ket(race) + ket(sex) + ket("capital-gain",capital_gain) + ket("capital-loss",capital_loss) + ket("hours-per-week",hours_per_week) + ket(native_country)

        # heh. adult.data uses "<=50K" and ">50K", while adult.test uses "<=50K." and ">50K."
        # tweak to fix that:
        wage_class = wage_class.rstrip('.')
        if wage_class == "<=50K":
          ket_wage_class = ket("below-50K")
        elif wage_class == ">50K":
          ket_wage_class = ket("above-50K")
        else:
          ket_wage_class = ket("")
        
        if learning:                         # learn training data set:
          node = ket("node-" + str(k))
          C.learn("pattern",node,r)
          C.learn("M",node,ket_wage_class)
        else:
          node = ket("example-" + str(k))    # learn test cases:
          C.learn("input-pattern",node,r)    
          C.learn("answer",node,ket_wage_class)
      except:
        continue

# test cases to check my code is correct.
#learn_data(C,short_sample,True)
#learn_data(C,short_sample,False)

# the main event:
learn_data(C,learning_data,True)
learn_data(C,test_data,False)

# save the results:
sw_file = "sw-examples/adult-wage-pattern-recognition.sw"
save_sw(C,sw_file,False)

