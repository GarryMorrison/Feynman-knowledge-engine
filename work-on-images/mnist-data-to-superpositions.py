#!c:/Python34/python.exe

#######################################################################
# 
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2016-05-12
# Update:
# Copyright: GPLv3
#
# Usage: ./mnist-data-to-images.py how-many-to-process
#
#######################################################################

import os
import sys

from PIL import Image

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

context = context_list("raw mnist superpositions")

try:
  k = int(sys.argv[1])
except:
  print("\nUsage: ./mnist-data-to-images.py how-many-to-process")
  sys.exit(1)

# for now, assume they exist, without testing it:
source = "work-on-handwritten-digits/mnist_train_images.csv"
destination = "work-on-handwritten-digits/train-images/"
#source = "work-on-handwritten-digits/mnist_test_images.csv"
#destination = "work-on-handwritten-digits/test-images/"


count = 0
with open(source,'r') as f:
  for line in f:
    line = line.strip()
    if len(line) == 0:
      continue
    count += 1
    if count > k:
      break
    data = [ 255 - int(x) for x in line.split(',')]
    r = superposition()
    for i,pixel in enumerate(data):
      pixel_ket = ket(str(i+1),pixel)
      r.data.append(pixel_ket)
    context.learn("pixels","image: mnist-test-image-" + str(count),r)
context.print_universe()
context.save("sw-examples/raw-mnist-test-100-superpositions.sw")

