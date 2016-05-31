#!/bin/bash

# echo $1
# cd "/Users/udit/git/btp/object-detector/"
# python /Users/udit/git/btp/object-detector/3d.py

cd "/Users/udit/git/btp/object-detector"
while IFS='' read -r line || [[ -n "$line" ]]; do
	echo $line
    $line
done < "/Users/udit/git/btp/gui/args.txt"