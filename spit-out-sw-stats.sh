#!/bin/sh

if [ $# -lt 1 ] ; then
  echo -e "\nUsage: ./spit-out-sw-stats.sh file.sw\n"
  exit
fi

file="$1"

sha1sum "$file"

size=$(du -h "$file" | cut -f1)
op_count=$(grep -v "^supported-op" "$file" | grep "^[[:alpha:]]" | sed 's/ |.*$//g' | sort | uniq | wc -l)
learn_rule_count=$(grep -v "^supported-op" "$file" | grep -c "=> ")

echo "($size, $op_count op types and $learn_rule_count learn rules)"

for op in $(grep -v "^supported-op" "$file" | grep "^[[:alpha:]]" | sed 's/ |.*$//g' | sort | uniq); do
  learn_rule_count=$(grep "^$op " "$file" | grep -c "=> ")
  echo "$op: $learn_rule_count learn rules"
done

