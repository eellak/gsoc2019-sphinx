# A python script that adds 'out of dictionary'
# words in the dictionary usign Phonetisaurus.

import sys
import subprocess
import os
import argparse

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool that generates phonemes for out of dictionary words and adds them in the dictionary
    ''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--model', help="Phonetisaurus model", required=True)
    required.add_argument(
        '--input', help="Path of missing words file.", required=True)
    required.add_argument(
        '--dict', help="Path of the dictionary", required=True)

    args = parser.parse_args()
    model = args.model
    dict = args.dict
    input = args.input

    if not os.path.isfile(model) or not os.path.isfile(dict) or not os.path.isfile(input):
        sys.exit("Wrong arguments")

    print("Generating phonemes...")
    if subprocess.call(['phonetisaurus-apply --model ' + model + ' --word_list ' + input + ' > missing-words-phonemes.txt'], shell=True):
        sys.exit('error in subprocess')
    print("Copy generated phonemes to given dictionary...")
    # Open file with the missing words and the generated phonemes.
    with open('missing-phonemes', 'r') as r, open(dict, 'a') as w:
        for line in r:
            w.write(line.replace('\t', ' '))

    print('OK')
