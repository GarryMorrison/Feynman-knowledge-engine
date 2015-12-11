#!/usr/bin/env python3

# OK. So what is the idea behind this code?
# Well, it is motivated by the idea of neuron grid cells, eg in rats.
# So the idea is define a grid by defining relationships between grid elements.
# In this case N, NE, E, SE, S, SW, W, NW.
# Then adding knowledge specific to particular grid locations.
# In humans this might include say restaurants, service stations, your home, your work, etc.
# In the current file, this is just a sinle integer value. Defaults at zero.
# Each time you step on a cell you add 1 to it's value.
# Then randomly walk along the grid for n steps.
# First case was just a random pick-elt from SE, S, SW.
# In the future, there are a couple of tweaks we can make:
# 1) shapes other than rectangular grids. eg, the corridor layout of a hospital.
# 2) more inteligent walking. Instead of randomly picking, some more involed choices.
# eg, maybe ants heading roughly towards cells with more scent markers, but still in a rough say Southish direction.
# eg, maybe a robot trying to get from A to B.
# So, I guess robots are probably the long term goal for code like this!
#
# http://write-up.semantic-db.org/36-learning-a-grid.html
# http://write-up.semantic-db.org/37-walking-our-grid.html


import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *


C = context_list("walking a grid")


def ket_elt(j,i):
  return ket("grid: " + str(j) + " " + str(i))


# lets put the logic of handling boundaries here.
# makes it easier to swap to torus model too!
# Makes use of the fact that learn() ignores rules that are the empty ket |>.
# and makes create_grid() much cleaner!
def ket_elt_bd(j,i,I,J):
# finite universe model:
  if i <= 0 or j <= 0 or i > I or j > J:
    return ket("",0)
# torus model:
#  i = (i - 1)%I + 1
#  j = (j - 1)%J + 1
  return ket("grid: " + str(j) + " " + str(i))


# boundary handling machinery now in ket_elt_bd()
def create_grid(c,I,J):
  c.learn("dim-1","grid",str(I))
  c.learn("dim-2","grid",str(J))

  for j in range(1,J+1):
    for i in range(1,I+1):
      x = ket_elt(j,i)
# don't need this, since not doing train-of-thought walk:
# and it is seriously slow. Need to improve add_learn() one day!
#      c.add_learn("elements","grid",x)
      c.learn("cell-value",x,"0")
      c.learn("N",x,ket_elt_bd(j-1,i,I,J))
      c.learn("NE",x,ket_elt_bd(j-1,i+1,I,J))
      c.learn("E",x,ket_elt_bd(j,i+1,I,J))
      c.learn("SE",x,ket_elt_bd(j+1,i+1,I,J))
      c.learn("S",x,ket_elt_bd(j+1,i,I,J))
      c.learn("SW",x,ket_elt_bd(j+1,i-1,I,J))
      c.learn("W",x,ket_elt_bd(j,i-1,I,J))
      c.learn("NW",x,ket_elt_bd(j-1,i-1,I,J))


#create_grid(C,15,15)
#create_grid(C,5,5)         
create_grid(C,10,10)


#create_grid(C,3,3)
#create_grid(C,9,9)
#create_grid(C,40,40)
#create_grid(C,60,60)
#create_grid(C,45,45)
#create_grid(C,20,20)


# just sample test of setting grid values:
#C.learn("cell-value","grid: 3 5","13")
#C.learn("cell-value","grid: 7 2","8")
#C.learn("cell-value","grid: 1 5","s")   # yeah, doesn't have to be a number, here it is the string "s".
                                    # well, the walk-grid code assumes elements are strings of ints.

print(C.dump_universe())
sys.exit(0)


# returns a string that is the grid:
# apply_op polutes the output with x: grid: i j, hence string version.
def string_grid(c,grid):
  I = int(grid.apply_op(c,"dim-1").label)
  J = int(grid.apply_op(c,"dim-2").label)

  s = ""
  s += "I: " + str(I) + "\n"
  s += "J: " + str(J) + "\n"  

  for j in range(1,J+1):
    s += str(j).ljust(4)
    for i in range(1,I+1):
      x = ket_elt(j,i)
      value = x.apply_op(c,"cell-value").the_label()  
      if value == "0":                             
        value = "."
      s += value.rjust(3)
    s += "\n"
  return s


# define the grid ket:
grid = ket("grid")

# quick check on our grid:
#print(string_grid(C,grid))
#sys.exit(0)

# number of steps:
n = 20

# the seed/starting cell:
seed_cell = ket("grid: 10 10")


# define cell propagation rules:
C.learn("SW-S-SE","*",stored_rule("pick-elt (SW |_self> + S |_self> + SE |_self>)"))
C.learn("W-SW-S-SE-E","*",stored_rule("pick-elt (W |_self> + SW |_self> + S |_self> + SE |_self> + E |_self>)"))
C.learn("W-SW-S-SE-E-NE","*",stored_rule("pick-elt (W |_self> + SW |_self> + S |_self> + SE |_self> + E |_self> + NE |_self>)"))
C.learn("NW-W-SW-S-SE-E","*",stored_rule("pick-elt (NW |_self> + W |_self> + SW |_self> + S |_self> + SE |_self> + E |_self>)"))
C.learn("NW-W-SW-S-SE-E-NE","*",stored_rule("pick-elt (NW |_self> + W |_self> + SW |_self> + S |_self> + SE |_self> + E |_self> + NE |_self>)"))

def walk_grid(C,seed_cell,next,steps):
  cell = seed_cell
  for k in range(steps):
    value = cell.apply_op(C,"cell-value").the_label()
    try:
      next_value = str(int(value) + 1)
    except:
      next_value = "1"
    C.learn("cell-value",cell,next_value)            
    cell = cell.apply_op(C,next).ket()


#walk_grid(C,seed_cell,"W-SW-S-SE",n)

# NB: we had to redefine all the "value" to "cell-value" so it didn't conflict with the built in function called "value"
# Yeah, a pain!
# 
def new_walk_grid(C,seed_cell,next,steps):
  C.learn("next-value","*",stored_rule("arithmetic(cell-value |_self>,|+>,|1>)"))

  cell = seed_cell
  for k in range(steps):
    next_value = cell.apply_op(C,"next-value")
    C.learn("cell-value",cell,next_value)            
    cell = cell.apply_op(C,next).ket()

#new_walk_grid(C,seed_cell,"SW-S-SE",30)
#seed_cell = ket("grid: 2 10")
#new_walk_grid(C,seed_cell,"W-SW-S-SE-E",200)

C.learn("cell-value","grid: 3 5","13")
C.learn("cell-value","grid: 7 2","8")
C.learn("cell-value","grid: 1 5","H")
C.learn("cell-value","grid: 10 8","G")
C.learn("cell-value","grid: 10 9","R")
C.learn("cell-value","grid: 10 10","I")
C.learn("cell-value","grid: 10 11","D")
print(string_grid(C,grid))

sys.exit(0)

# In BKO swc something like this perhaps:
# BUG: we can't use "value" as the literal op, as it is already defined as a function operator!
# For testing in the console I went with "cell-value" instead.
# This is an issue I will come across more. ie, conflict between reserved names, vs names you define.
#
# next |*> #=> pick-elt (SW |_self> + S |_self> + SE |_self>)
# |cell> => |grid: 1 22>
# repeat[n][
#   cell-value "" |cell> => arithmetic(cell-value |_self>,|+>,|1>)
#   |cell> => next "" |cell>
# ]

