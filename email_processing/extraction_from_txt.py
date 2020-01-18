#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from helper import process_text, save_messages
import urllib
import base64
import pickle
import os.path
import chardet
import argparse

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool for extracting sent messages directly from a txt file
    ''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--output', help="Output directory", required=True)
    required.add_argument(
        '--input', help="Input text file", required=True)
    optional.add_argument(
        '--sentence', help="If true, save each sentence of the messages in separate files.", action='store_true')

    args = parser.parse_args()
    out = args.output
    input_file = args.input
    sentence = args.sentence

    if not out.endswith('/'):
        out = out + '/'

    print('Reading messages...')
    # Get the sent messages.
    messages = []
    with open(input_file, 'r') as r:
        for line in r:
            messages.append(process_text(line))

    print('Saving messages...')
    # Save messages in txt files.
    if not os.path.exists(out):
        os.makedirs(out)

    if sentence:
        # Compute total number of sentences.
        total = 0
        for msg in messages:
            for sent in msg:
                total += 1
        total_str = str(total - 1)
        i = 0
        for msg in messages:
            for sent in msg:
                # Add leading zeros in order to have all names in the right order.
                i_zeroed = str(i).rjust(len(total_str), '0')
                with open('./' + out + 'data_' + i_zeroed, 'w') as w2:
                    w2.write(sent + '\n')
                i += 1
    else:
        total_str = str(len(messages) - 1)
        for i, msg in enumerate(messages):
            # Add leading zeros in order to have all names in the right order.
            i_zeroed = str(i).rjust(len(total_str), '0')
            with open('./' + out + 'data_' + i_zeroed, 'w') as w2:
                for sent in msg:
                    w2.write(sent + '\n')
    print(len(messages), 'messages have been saved successfully')
