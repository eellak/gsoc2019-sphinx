#!/bin/bash

if [ ! -f "$1" ]; then
    echo "First .lm model does not exist"
    exit 0
fi

if [ ! -f "$2" ]; then
    echo "Second .lm model does not exist"
    exit 0
fi

# Merge .ml models usign srilm
ngram -lm $1 -mix-lm $2 -write-lm "merged.lm"
