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


dict = sys.argv[1]
file = sys.argv[2]

w = open('missing-words.txt', 'w')

with open(file, 'r') as f:
    for line in f:
        words = line.split(' ')
        for word in words[:len(words)-1]:
            if not searchDic(word, dict):
                w.write(word + '\n')
                print(word)
w.close()
