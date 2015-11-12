#!/usr/bin/env python3

#######################################################################
# Convert raw tld data into sw file
# source: http://http-analyze.org/tld.php
#
# Author: Garry Morrison
# Date: 2015-03-03
# Update:
# Copyright: GPLv3
#
# Usage:
#
#######################################################################


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

C = context_list("top level domains")

filename = "tld-data.txt"

C.learn("tld","*",stored_rule("top-level-domain |_self>"))
with open(filename,'r') as f:
  for line in f:
    try:
      tld,country = line.split('\t')
      tld = tld.strip()
      country = country.strip()

      C.learn("top-level-domain",country,tld)
      C.learn("country",tld,country)
    except:
      continue

sw_file = "sw-examples/top-level-domains.sw"
save_sw(C,sw_file)

