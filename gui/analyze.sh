#!/bin/bash
cd "/Users/udit/git/btp/object-detector"
while IFS='' read -r line || [[ -n "$line" ]]; do
	echo $line
    $line
done < "/Users/udit/git/btp/gui/args.txt"