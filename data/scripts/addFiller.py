# A python script that adds <s> at the start
# of each text and </s> at the end.

import sys
import os
import argparse

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool for adding the filler symbol (<s> and </s>) in a transcription.
    ''')

    required = parser.add_argument_group('required arguments')

    required.add_argument(
        '--input', help="Input transcription", required=True)
    required.add_argument(
        '--output', help="Output transcription containing the fillers", required=True)

    args = parser.parse_args()
    input = args.input
    output = args.output
    if not os.path.isfile(input):
        sys.exit("Wrong arguments")

    with open(output, 'w') as w, open(input, 'r') as r:
        for line in r:
            words = line.split(' ')
            # Last word is the file id according to Sphinx format.
            w.write(
                '<s> ' + ' '.join(words[:len(words) - 1]) + ' </s> ' + words[-1])
