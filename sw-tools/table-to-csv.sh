#!/bin/sh

if [ $# -lt 1 ] ; then
  echo -e "\nUsage: ./table-to-csv.sh saved-table.txt\n"
  exit
fi

table="$1"

#sed 's/^| //g' "$table" | sed 's/|/,/g' | grep -v "^+"

sed 's/^| /"/g' "$table" | sed 's/| /","/g' | grep -v "^+" | sed 's/ |$/"/g'
