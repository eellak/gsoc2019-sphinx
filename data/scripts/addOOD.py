# A python script that adds 'out of dictionary'
# words in the dictionary usign Phonetisaurus.

import sys
import subprocess
import os

if len(sys.argv) != 3:
    sys.exit("Wrong number of parameters!")

# Read phonetisaurus trained model and dictionary to expand.
model = sys.argv[1]
dict = sys.argv[2]

if not os.path.isfile(model) and not os.path.isfile(dict):
    sys.exit("Wrong arguments")

print("Generating phonemes...")
if subprocess.call(['phonetisaurus-apply --model ' + model + ' --word_list missing-words.txt > missing-words-phonemes.txt'], shell=True):
    sys.exit('error in subprocess')

print("Copy generated phonemes to given dictionary...")
# Open file with the missing words and the generated phonemes.
with open('missing-words-phonemes.txt', 'r') as r, open(dict, 'a') as w:
    for line in r:
        w.write(line)

print('OK')
