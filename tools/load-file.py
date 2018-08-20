#!c:/Python34/python.exe

#######################################################################
# load a single sw/swc file
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 20/8/2018
# Update: 20/8/2018
# Copyright: GPLv3
#
# Usage: ./load-file.py file.sw
# the idea is to test the load time of a file
#
# example usage:
# $ python3 -m cProfile load-file.py sw-examples/names.sw
# $ time python3 load-file.py sw-examples/names.sw
#
#######################################################################

import sys
from semantic_db import *

# switch off debug and info by default
logger.setLevel(logging.WARNING)

if len(sys.argv) < 2:
    print('please specify a file')
    sys.exit(0)

filename = sys.argv[1]
print('loading %s' % filename)

# context is defined in the parser section
# and we can't redefine it here due to the one global context bug
# load entire file at once:
context.load(filename)

# load one line at a time:
# useful for large files.
# but breaks multi-line stored rules
# context.line_load(filename)

# optionally print out the knowledge:
# comment out for large sw files, so we can measure loading times, not loading + print times.
context.print_multiverse()

