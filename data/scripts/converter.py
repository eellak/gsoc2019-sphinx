# Convert sound files to mono .wav
# with sample rate 16kHz.

import argparse
import os
import subprocess
import sys

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool for converting sound files in Sphinx format (mono wav files with 16kHz sample rate)
    ''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('--input', help="Input directory", required=True)
    optional.add_argument(
        '--output', help="Output direcory (default: Input directory)")

    args = parser.parse_args()
    input = args.input
    output = args.output

    if not input.endswith('/'):
        input = input + '/'

    if output is None:
        output = input

    if not os.path.exists(output):
        os.makedirs(output)

    for file in os.listdir(input):
        input_path = os.path.join(input, file)
        output_path = os.path.join(output, file)
        output_base = os.path.splitext(output_path)[0]
        if subprocess.call(['ffmpeg -i ' + input_path + ' -ar 16000 -ac 1 ' + output_base + '.wav'], shell=True):
            sys.exit('Error in subprocess')
