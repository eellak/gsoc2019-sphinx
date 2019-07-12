import argparse
import sys
import os
from rec_unlimited import record

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''
		Tool for recording a speech dataset for Sphinx (16 sample rate-mono) quickly.
	''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional_arguments')

    required.add_argument(
        '--output', help="Folder to save the files", required=True)
    required.add_argument(
        '--input', help="Folder that contains the input transcriptions", required=True)
    required.add_argument(
        '--name', help="Name of the dataset (name format should be name_{id})", required=True)
    required.add_argument(
        '--total', help="Total number of files", required=True)

    args = parser.parse_args()
    out = args.output
    inp = args.input
    name = args.name
    total = args.total

    if not out.endswith('/'):
        out = out + '/'
    if not inp.endswith('/'):
        inp = inp + '/'
    for text in sorted(os.listdir(inp)):
        while True:
            print("Type n to record next file, q to quit")
            ans = input()
            if ans == "n":
                break  # stops the loop
            if ans == "q":
                sys.exit("Exiting...")
        with open(os.path.join(inp, text), 'r') as f:
            print(f.read())
            print('Recording..')
            record(None, 16000, 1, os.path.join(
                out, text + '.wav'), None)
