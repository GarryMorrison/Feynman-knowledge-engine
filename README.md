# The Feynman Knowledge Engine
a minimalist but extensible knowledge engine

Currently very pre-alpha

A series of blog posts that tries to explain my ideas:
http://write-up.semantic-db.org/

A blog post trying to summarize and give an interpretation of the BKO scheme:
http://write-up.semantic-db.org/166-an-interpretation-of-my-bko-scheme.html

A big collection of example sw files:
http://semantic-db.org/sw-examples/

Wikipedia to link-structure sw files:
http://semantic-db.org/wikipedia-sw/

My console history. Essentially a giant collection of examples:
https://github.com/GarryMorrison/Feynman-knowledge-engine/blob/master/sa-console-command-history.txt

Visualizing sw files, via the DOT language:
http://write-up.semantic-db.org/169-visualizing-sw-files.html

A definition of the if-then machine, a proposed approximation to a single neuron:
http://write-up.semantic-db.org/186-introducing-the-if-then-machine.html

<pre>
Installation instructions:
$ git clone git://github.com/python-parsley/parsley.git
$ cd parsley/
$ sudo python3 setup.py install

$ cd ..
$ git clone git://github.com/GarryMorrison/Feynman-knowledge-engine.git
$ cd Feynman-knowledge-engine/
$ chmod +x the_semantic_db_console.py

$ ./the_semantic_db_console.py
Welcome!

sa: h

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

</pre>

