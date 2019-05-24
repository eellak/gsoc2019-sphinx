#!/bin/bash

# A bash script that converts .mp3 files to .wav
# with sample rate 16kHz.
# Usage: ./converter <directory name>

# Check number of arguments
[ $# -eq 0 ] && { echo "Usage: $0 directory_name"; exit 1; }

# Check if argument is a directory
if [ ! -d "$1" ]; then
    echo "Give a right directory name"
    exit 0
fi

FILES=$1/*
for f in $FILES
do
    echo "Processing $f file..."
    dir="$(basename $f)"
    # Convert each file in .wav with 16kHz sample rate.
    ffmpeg -i $f -ar 16000 -ac 1 ${f%.*}.wav
done
