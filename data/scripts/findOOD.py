# A python script that finds 'out of
# dictionary' words from given transcriptions.

# TODO: faster implementation using binary search
# since the dictionary is sorted.


import sys
import os
import argparse


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


if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool that finds out of dictionary words from a given transcription
    ''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--dict', help="Path of dictionary", required=True)
    required.add_argument(
        '--input', help="Path of input transcription (should be in Sphinx format)", required=True)
    required.add_argument(
        '--output', help="Path of output file", required=True)
    optional.add_argument(
        '--print_missing', help="If True, prints missing words", action='store_true')

    args = parser.parse_args()
    input = args.input
    output = args.output
    dict = args.dict
    print_missing = args.print_missing

    if not os.path.isfile(dict) or not os.path.isfile(input):
        sys.exit("Wrong arguments")

    # Keep track of missing words, to avoid duplicates.
    missing = []

    with open(input, 'r') as f, open(output, 'w') as w:
        for line in f:
            # Some Greek texts have \xa0 (Unicode representing spaces)
            # so remove it, before splitting on spaces.
            line = line.replace(u'\xa0', u' ')
            words = line.split(' ')
            # Last word is the identity of the transcription, so
            # don't care about it.
            print('Searching for transcription: ' +
                  words[-1].strip('\n'))
            for word in words[:len(words) - 1]:
                if word:
                    if (not searchDic(word, dict)) and (word not in missing):
                        if print_missing:
                            print(word)
                        w.write(word + '\n')
                        missing.append(word)

    print('OK')
