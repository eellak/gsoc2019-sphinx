# A python script that finds 'out of
# dictionary' words from given transcriptions.

# TODO: faster implementation using binary search
# since the dictionary is sorted.


import sys
import os


# Search for a specific word in the
# dictionary.
def searchDic(word, dict):
    with open(dict) as f:
        i = 1
        for line in f:
            if line.split(' ')[0] == word:
                return True
            i += 1
    return False


if len(sys.argv) != 3:
    sys.exit("Wrong number of parameters!")

# Read dictionary and transcription file.
dict = sys.argv[1]
file = sys.argv[2]
if not os.path.isfile(dict) or not os.path.isfile(file):
    sys.exit("Wrong arguments")

# Keep track of missing words, to avoid duplicates.
missing = []

with open(file, 'r') as f, open('missing-words.txt', 'w') as w:
    for line in f:
        # Some Greek texts have \xa0 (Unicode representing spaces)
        # so remove it, before splitting on spaces.
        line = line.replace(u'\xa0', u' ')
        words = line.split(' ')
        # Last word is the identifires of the transcription, so
        # don't care about it.
        print('Searching for transcription: ' + words[-1])
        for word in words[:len(words)-1]:
            if word:
                if (not searchDic(word, dict)) and (word not in missing):
                    w.write(word + '\n')
                    print(word)
                    missing.append(word)

print('OK')
