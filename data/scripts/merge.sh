#!/bin/bash

# A bash script that takes two language models
# as input and merges them usign SRILM.
# Usage: ./merge <language model 1> <language model 2>

# Check arguments
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
