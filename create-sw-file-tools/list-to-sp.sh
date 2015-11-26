#!/bin/sh

if [ $# != 2 ] ; then
  echo -e "\nUsage: ./list-to-sp.sh pre-string file\n"
  echo -e "\nExample: ./list-to-sp.sh \"list-of |common English words> => \" 74550com.mon > common-English-words.sw"
  echo -e "\nData here: http://icon.shef.ac.uk/Moby/mwords.html"
  exit
fi

pre="$1"
data="$2"

echo -n "$pre"
sed 's/^/|/g' "$data" | sed 's/$/> + /g' | tr -d '\n' | sed 's/ + $//g'
