#!/usr/bin/env python3

import sys

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

#C = context_list("geonames AU")
# is new_context() faster than context_list() ??
C = new_context("geonames US")

# NB: may need to filter down to ASCII chars.
#file = "data/ascii-just-adelaide.txt"
#file = "data/ascii-cities15000.txt"


#file = "data/short-play.txt" # yup. code seems to work!
#file = "data/AU.txt" # nope! Bugs out on non-ascii chars.

#file = "data/ascii-AU.txt" # tidied using clean-ascii.sh

#file = "data/ascii-cities15000.txt"
file = "data/ascii-US.txt"      # too big for RAM for now.
#file = "data/ascii-cities1000.txt"



with open(file,'r') as f:
  for line in f:
#    print("line:",line)
#    fields = len(line.split("\t"))
#    print("fields:",fields)
    
    id,name,asciiname,altname,lat,long,feat_class,feat_code,country,cc2,admin1,admin2,admin3,admin4,population,elevation,dem,tz,mod_date = line.split("\t")
#    print("id:        ",id)
#    print("name:      ",asciiname)
#    print("lat:       ",lat)
#    print("long:      ",long)
#    print("country:   ",country)
#    print("population:",population)
#    print("dem:       ",dem)
#    print("tz:        ",tz)

#    print()

    x = ket("id: " + id)    
#    C.learn("id",x,"geonameid: " + id)
    C.add_learn("id",asciiname,x)
    C.learn("name",x,asciiname)     
    C.learn("latitude",x,"latitude: " + lat) 
    C.learn("latitude-self",x,x.multiply(float(lat)))
    C.learn("longitude",x,"longitude: " + long)
    C.learn("longitude-self",x,x.multiply(float(long)))
    C.learn("country-code",x,"country-code: " + country)  

    if int(population) > 0:
      C.learn("population",x,"population: " + population)
      C.learn("population-self",x,x.multiply(int(population)))

    if elevation != '':
      C.learn("elevation",x,"m: " + elevation)

    if tz != '':  
      C.learn("tz",x,"time-zone: " + tz)


name = "sw-examples/improved-geonames-us.sw"
save_sw(C,name)

# first play with profiler:
#import cProfile
#cProfile.run('save_sw(C,name)')
#print(C.dump_universe())

