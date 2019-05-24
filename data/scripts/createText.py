#!/bin/bash

# A script that reads test.transcriptions file and write each
# sentence in 'train-text.txt' file line by line.

# Open read file
r = open("../../test.transciptions", 'r')
# Open write file
w = open("train-text.txt", 'w')

for line in r:
    # Keep only the text of each transcription.
    # line = line.split("(paramythi_")[0] for paramythi dataset
    line = line.split("(radio_")[0]
    # Split the text to its sentences.
    sentences = line.split(".")
    # Write non-empty sentences.
    for sentence in sentences:
        if sentence.strip():
            w.write(sentence.strip() + '.' + '\n')

# Close all files
r.close()
w.close()
