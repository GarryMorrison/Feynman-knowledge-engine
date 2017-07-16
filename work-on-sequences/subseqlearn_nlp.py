#!c:/Python34/python.exe

#######################################################################
# try to apply subseqlearn to natural language
# the hope is it auto finds words.
# just testing an idea, not guaranteed to work
# doesn't look like it will work ...
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 2017-07-13
# Update:
# Copyright: GPLv3
#
# Usage: ./subseqlearn_nlp.py
#
#######################################################################

import sys
from subseqlearn import *


sentence = """Dogs (Canis lupus familiaris) are domesticated mammals, not natural wild animals. They were originally bred from wolves. They have been bred by humans for a long time, and were the first animals ever to be domesticated.
Today, some dogs are used as pets, others are used to help humans do their work. They are a popular pet because they are usually playful, friendly, loyal and listen to humans. Thirty million dogs in the United States are registered as pets.[1] 
Dogs eat both meat and vegetables, often mixed together and sold in stores as dog food. Dogs often have jobs, including as police dogs, army dogs, assistance dogs, fire dogs, messenger dogs, hunting dogs, herding dogs, or rescue dogs.
They are sometimes called "canines" from the Latin word for dog - canis. Sometimes people also use "dog" to describe other canids, such as wolves. A baby dog is called a pup or puppy. A dog is called a puppy until it is about one year old.
Dogs are sometimes referred to as "man's best friend" because they are kept as domestic pets and are usually loyal and like being around humans.
All dogs are descended from wolves, by domestication and artificial selection. This is known because DNA genome analysis has been done to discover this.[3][4] They have been bred by humans. The earliest known fossil of a domestic dog is from 
31,700 years ago in Belgium.[5] Dogs have lived with people for at least 30,000 years. In 2013, a study was published that showed that the skull and teeth of a canid, dated to 33,000 years ago, had characteristics closer to a dog than to a 
wolf, and the authors conclude that "this specimen may represent a dog in the very early stages of domestication, i.e. an “incipient” dog." The researchers go on to suggest that it was, however, a line that did not lead to modern dogs.[6] 
Genetically, this material is closer to that of a modern dog than to that of a wolf.[7] Other signs of domestication are that sometimes, dogs were buried together with humans.[8] Evidence of this is a tomb in Bonn, where a man of about 50 
years of age, a woman of about 25 years of age, the remains of a dog, plus other artifacts were found. Radiocarbon dating showed that the human bones were between 13.300 and 14.000 years old.
Dogs are often called "man's best friend" because they fit in with human life. Man refers to humankind and not just guys (Old English). Dogs can serve people in many ways. For example, there are guard dogs, hunting dogs, herding dogs, guide 
dogs for blind people, and police dogs. There are also dogs that are trained to smell for diseases in the human body or to find bombs or illegal drugs. These dogs sometimes help police in airports or other areas. Sniffer dogs (usually 
beagles) are sometimes trained for this job. Dogs have even been sent by Russians into outer space, a few years before any human being. The first dog sent up was named Laika, but she died within a few hours.There are at least 800 breeds 
(kinds) of dogs. Dogs whose parents were the same breed will also be that breed: these dogs are called purebred or pure pedigree dogs. Dogs with parents from different breeds no longer belong to one breed: they are called mutts, mixed-breed 
dogs, hybrids, or mongrels. Some of the most popular breeds are sheepdogs, collies, poodles and retrievers. It is becoming popular to breed together two different breeds of dogs and call the new dog's breed a name that is a mixture of the 
parents' breeds' two names. A puppy with a poodle and a pomeranian as parents might be called a Pomapoo. These kinds of dogs, instead of being called mutts, are known as designer dog breeds. These dogs are normally used for prize shows and 
designer shows. They can be guide dogs.Dogs have four legs and make a "bark," "woof," or "arf" sound. Dogs often chase cats, and most dogs will fetch a ball or stick.
Dogs can smell and hear better than humans, but cannot see well in color because they are color blind. Due to the anatomy of the eye, dogs can see better in dim light than humans. They also have a wider field of vision.
Like wolves, wild dogs travel in groups called packs. Packs of dogs are ordered by rank, and dogs with low rank will submit to other dogs with higher rank. The highest ranked dog is called the alpha male. A dog in a group helps and cares for 
others. Domesticated dogs often view their owner as the alpha male."""


source_file = 'text/WP-Adelaide.txt'
source_file = 'text/WP-Australia.txt'
source_file = 'text/ebook-Asimov_Isaac_-_I_Robot.txt'
#source_file = 'text/ebook-Tom_Sawyer_74.txt'


with open(source_file, 'r') as f:
  sentence = f.read()
#print(sentence)
#sys.exit(0)


def save_sp(dest_file, op, ket_name, sp):
  s = "%s |%s> => %s" % (op, ket_name, sp)
  with open(dest_file, 'w') as f:
    f.write(s)


def merged_string_to_fragments(s, name):
  merged_sentence = s.replace(' ', '').replace('\n', '')
  #print(merged_sentence)
  #return

  seq_sentence = sequence('sentence', list(merged_sentence))
  #seq_sentence = sequence('sentence', s.replace('\n', ' ').split(' '))
  #seq_sentence.display()

  encode_dict = {}
  encoded_sentence = seq_sentence.encode(encode_dict)

  partition_points = learn_subsequences(encoded_sentence)
  subsequences = fragment_positive_sequence(seq_sentence, partition_points)
  #subsequences = fragment_sequence(seq_sentence, partition_points)


  r = superposition()
  for seq in subsequences:
    s = "".join(seq)
    print(s)
    r.add(s)
  print(r.coeff_sort())
  save_sp('sw-examples/subseqlearn-nlp--%s--raw.sw' % name, 'subseq', name, r)

  # now count them:                                     # bah, seems to make things worse!
  r2 = superposition()
  for word,coeff in r:
    count = merged_sentence.count(word)
    r2.add(word, count)
  #print(r2.coeff_sort())
  save_sp('sw-examples/subseqlearn-nlp--%s.sw' % name, 'subseq', name, r2)


#merged_string_to_fragments(sentence, 'wp-australia-split')
merged_string_to_fragments(sentence, 'I-robot')

