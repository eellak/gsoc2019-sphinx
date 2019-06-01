# Replace all \xa0 charactes with space in a text file.

import sys

if len(sys.argv) != 2:
    sys.exit("Wrong number of parameters!")


file = sys.argv[1]
if not os.path.isfile(file):
    sys.exit("Wrong path")

with open(file, 'r') as r, open('transcription_formatted', 'w') as w:
    for line in r:
        w.write(line.replace(u'\xa0', u' '))
