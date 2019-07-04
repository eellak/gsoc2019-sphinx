# A python script that reads 'train/transcriptions' file and
# write each sentence in output file line by line.
# Necessary to build a language model from transciptions.

import sys
import argparse
import os

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool for creating email corpus from transcriptions (writes each sentence of input directory in output file line by line).
    ''')

    required = parser.add_argument_group('required arguments')

    required.add_argument(
        '--input', help="Folder the contains the transcriptions", required=True)

    required.add_argument(
        '--output', help="Output file", required=True)

    args = parser.parse_args()
    input = args.input
    output = args.output

    if not input.endswith('/'):
        input = input + '/'

    # Open read and write file
    with open(output, 'w') as w:
        for text in sorted(os.listdir(input)):
            with open(os.path.join(input, text), 'r') as f:
                for line in f:
                    w.write(line)
