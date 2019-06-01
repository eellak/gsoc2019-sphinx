# A python script that adds <s> at the start
# of each text and </s> at the end.

import sys
import os


if len(sys.argv) != 2:
    sys.exit("Wrong number of parameters!")

if not os.path.isfile(sys.argv[1]):
    sys.exit("Wrong arguments")

with open('transcriptions_filler', 'w') as w, open(sys.argv[1], 'r') as r:
    for line in r:
        words = line.split(' ')
        w.write('<s> ' + ' '.join(words[:len(words)-1]) + ' </s> ' + words[-1])
