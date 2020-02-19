#!/bin/sh
awk '{printf "\"%s %s\" \"%s %s\" \"1968 Sep 22 %s\"\n", $10, $11, $12, $13, $1}' < data/1968-09-22.txt | while read line ; do
    eval ./eclipse-tell.py $line
    echo ""
done