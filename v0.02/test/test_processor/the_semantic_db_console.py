#!c:/Python34/python.exe 

#######################################################################
# the semantic-db console
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2014
# Update: 24/9/2015
# Copyright: GPLv3
#
# Usage: ./the_semantic_db_console.py [--debug] 
#
#######################################################################

import sys
import glob
import os
import datetime
import time
import urllib.request
#import logging

from the_semantic_db_code import *
from the_semantic_db_functions import *
from the_semantic_db_processor import *

# if --debug, set logging level to DEBUG:
if len(sys.argv) == 2:
  if sys.argv[1] == "--debug":
    logger.setLevel(logging.DEBUG)
  elif sys.argv[1] == "--info":
    logger.setLevel(logging.INFO)
  

logger.debug('debug enabled')   

# starting .sw directory:
sw_file_dir = "sw-examples"
# check it exists, if not create it:
if not os.path.exists(sw_file_dir):
  print("Creating " + sw_file_dir + " directory.")
  os.makedirs(sw_file_dir)
  

print("Welcome!")

C = context_list("sw console")

help_string = """
  q, quit, exit                quit the agent.
  h, help                      print this message
  context                      print list of context's
  context string               set current context to string
  icontext                     interactive context
  reset                        reset back to completely empty console
                               Warning! you will lose all unsaved work!
  dump                         print current context
  dump exact                   print current context in exact mode
  dump multi                   print context list
  dump self                    print what we know about the default ket/sp
  dump ket/sp                  print what we know about the given ket/sp
  display                      (relatively) readable display of current context
  display ket/sp               (relatively) readable display about what we know for the ket/sp
  freq                         convert current context to frequency list
  mfreq                        convert context list to frequency list
  web-load http://file.sw      load a sw file from the web
  load file.sw                 load file.sw
  save file.sw                 save current context to file.sw
  save multi file.sw           save context list to file.sw
  files                        show the available .sw files
  cd                           change and create if necessary the .sw directory
  ls, dir, dirs                show the available directories
  create inverse               create inverse for current context
  create multi inverse         create inverse for all context in context list
  x = foo: bah                 set x (the default ket) to |foo: bah>
  id                           display the default ket/superposition
  s, store                     set x to the result of the last computation
  .                            repeat last computation
  i                            interactive history
  history                      show last 30 commands
  history n                    show last n commands
  save history                 save console history to file
  debug on                     switch verbose debug messages on
  debug off                    switch debug messages off
  info on                      switch info messages on
  info off                     switch info messages off
  -- comment                   ignore, this is just a comment line.
  if none of the above         process_input_line(C,line,x)
"""


x = ket("",0)
stored_line = ""
command_history = []
command_history_file = "sa-console-command-history.txt"  # file where we save the command history. Might be interesting.

# save history function:
def save_history(history,history_file):
    print("saving history ... ")
    try:
      f = open(history_file,'a')
      today = str(datetime.date.today())
      f.write(today + "\n")
      for line in history:
        f.write("  " + line + "\n")
      f.write("\n")
      f.close()
      print("Done.")
    except:
      print("failed!")    


# the interactive semantic agent:
while True:
  line = input("\nsa: ")

  if line == "i":
    n = 30
    if len(command_history) > 0:
      count = min(len(command_history),n)
      history = command_history[-count:]
      for k,line in enumerate(history):
        print(" " + str(k) + ")  " + line)
      selection = input("\nEnter your selection: ")
      try:
        selection = int(selection)
        line = history[selection]
        print("Your selection:",line,"\n")
      except:
        continue
    else:
      print("history is empty")    
      continue
  command_history.append(line)

# exit the agent:
  if line in ['q','quit','exit']:

    # save history before we go:
    save_history(command_history,command_history_file)
  
    print("\nBye!")
    break

  if line in ['h','help']:
    print(help_string)

  elif line == "context":
    print(C.show_context_list())

  elif line == "icontext":
    print(C.show_context_list_index())
    selection = input("Enter your selection: ")
    try:
      selection = int(selection)
      if C.set_index(selection):
        print(C.dump_universe())
    except:
      continue

# switch context:
  elif line.startswith("context "):
    name = line[8:]
    C.set(name)
    print(C.dump_universe())

  elif line == "reset":
    check = input("\n  Warning! This will erase all unsaved work! Are you sure? (y/n): ")
    if len(check) > 0 and check[0] == 'y':
      C = context_list("sw console")
      print("\n  Gone ... ")

  elif line == "dump":
    print(C.dump_universe())

  elif line == "dump exact":
    print(C.dump_universe(True))

  elif line == "dump multi":
    print(C.dump_multiverse())

  elif line == "dump self":
    print(C.dump_multiple_ket_rules(x))

  elif line.startswith("dump "):
    var = line[5:]
    print("var:",var,"\n")
    try:
      sp = extract_compound_superposition(C,var)[0]
      print(C.dump_multiple_ket_rules(sp))
    except:
      continue

  elif line == "display":
    print(C.display_all())

  elif line.startswith("display "):
    var = line[8:]
    print("var:",var,"\n")
    try:
      sp = extract_compound_superposition(C,var)[0]
      print(C.display_sp(sp))
    except:
      continue

  elif line == "freq":
    result = C.to_freq_list()
    print(result)

  elif line == "mfreq":
    print(C.multiverse_to_freq_list())

  elif line.startswith("web-load "):          # where put it? in sw_file_dir? What if file with that name already exists?
    url = line[9:]                            # how about timing the download and load? Cheat, and merge with "load file.sw"?
    start_time = time.time()
    try:
      # download url
      print("downloading sw file:",url)       # code to time the download? Probably, eventually.
      headers = { 'User-Agent' : 'semantic-agent/0.1' }
      req = urllib.request.Request(url,None,headers)      # does it handle https?
      f = urllib.request.urlopen(req)
      html = f.read()
      f.close()
    except:
      print("failed to download:",url)
      continue
         
    # find the sw file name:
    name = url.split("/")[-1]
    dest = sw_file_dir + "/" + name

    dont_save = False      
    # check if it exists:
    while os.path.exists(dest):
      # either rename or overwrite
      check = input("\n  File \"" + name + "\" already exists.\n  [O]verwrite, [R]ename or [D]on't save? (O,R,D): ")
      if len(check) > 0:
        if check[0] in ["o","O"]:                  # we are allowed to overwrite it
          break
        if check[0] in ["d","D"]:                  # don't save the file we just downloaded (yeah, waste if it was big)
          dont_save = True
          break
        elif check[0] in ["r","R"]:                # we have to choose a new name
          check = input("\n  New name: ")
          if len(check) > 0:
            name = check
            dest = sw_file_dir + "/" + name

    # check if we don't want to save:
    if dont_save:
      continue
                     
    # let's save it:
    print("\nsaving to:",name)                  # do we need a try/except here?
    f = open(dest,'wb')
    f.write(html)
    f.close()

    # now let's load it into memory:
    print("loading:",dest,"\n")
    load_sw(C,dest)
    end_time = time.time()
    delta_time = end_time - start_time
    print("\n  Time taken:",display_time(delta_time))
   

  elif line.startswith("load "):
    name = line[5:]
    name = sw_file_dir + "/" + name            # load and save files to the sw_file_dir.
    print("loading sw file:",name)

# time it!
    start_time = time.time()
    load_sw(C,name)
    end_time = time.time()
    delta_time = end_time - start_time
    print("\n  Time taken:",display_time(delta_time))
  
  elif line == "save history":
    # save history:
    save_history(command_history,command_history_file)
  
  elif line.startswith("save multi "):
    name = line[11:]
    name = sw_file_dir + "/" + name            # load and save files to the sw_file_dir.
    print("saving context list to:",name)
    save_sw_multi(C,name)

  elif line.startswith("save "):               # check for file existance first? Or just blow away what is already there?
    name = line[5:]
    name = sw_file_dir + "/" + name            # load and save files to the sw_file_dir.    
    print("saving current context to:",name)
    save_sw(C,name)

  elif line == "files":
    sep = "   "
    max_len = 0
    data = []
    for file in glob.glob(sw_file_dir + "/*.sw"):
      base = os.path.basename(file)
      max_len = max(max_len,len(base))
      data.append([base,extract_sw_stats(file)])
    print()
    for file,stats in data:
      print("  " + file.ljust(max_len) + sep + stats)

  elif line.startswith("cd "):
    sw_file_dir = line[3:]
  # check it exists, if not create it:
    if not os.path.exists(sw_file_dir):
      print("Creating " + sw_file_dir + " directory.")
      os.makedirs(sw_file_dir)

  elif line in ['ls','dir','dirs']:
    print("directory list:")
    for dir in [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith("__")]:
      prefix = "  "
      if dir == sw_file_dir:
        prefix = "* "
      sw_count = len(glob.glob(dir + "/*.sw"))
      print(prefix + dir + " (" + str(sw_count) + ")")


  elif line == "create inverse":
    C.create_universe_inverse()

  elif line == "create multi inverse":
    C.create_multiverse_inverse()


  elif line.startswith("x = "):
    var = line[4:]
    try:
      x = extract_compound_superposition(C,var)[0]
    except:  
      x = ket(var)

  elif line == "id":
    print(x)

  elif line in ['s','store']:   # set x to the result of the last computation.
    x = result
    print("stored:",x)
    
  elif line.startswith("--"):
    continue

  elif line.startswith("history"):
    try:
      n = int(line[8:])
    except:
      n = 30

    if len(command_history) > 0:
      count = min(len(command_history),n)
      for line in command_history[-count:]:
        print("  " + line)

  elif line == 'debug on':
    logger.setLevel(logging.DEBUG)
    
  elif line == 'debug off':
    logger.setLevel(logging.INFO)

  elif line == 'info on':
    logger.setLevel(logging.INFO)
    
  elif line == 'info off':
    logger.setLevel(logging.WARNING)

  else:
    if line == ".":
      line = stored_line
    stored_line = line

    start_time = time.time()    

    result = process_input_line(C,line,x)  # maybe handling of comment lines should be in here?
    print(result)

    end_time = time.time()
    delta_time = end_time - start_time
    print("\n  Time taken:",display_time(delta_time))   # display_time() is in the sdb_functions.py file



