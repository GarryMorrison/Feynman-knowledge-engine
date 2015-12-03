#!/bin/sh

if [ $# == 0 ] ; then
  echo -e "\nUsage: ./make-image.sh filename.dat\n"
  exit
fi

dest="tmp.plg"

for file in "$@"; do
  echo "file: $file"
  name=$(echo "$file" | sed 's/.dat//g')
  title=$(echo "$name" | sed 's/-/ /g')

echo "set style data histogram
set xrange [0:65536]
set title \"$title\"
set style fill solid
set term png
set output \"$name.png\"
plot \"$file\" 
" > $dest

/usr/bin/gnuplot "$dest"

done
