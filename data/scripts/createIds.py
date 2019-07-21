# A python script that creates 'fileids' file
# for a certain dataset. This file contains the id
# of each file in the dataset in the form dataset_{id}.

import sys
import argparse

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool for creating fileid file.
    ''')

    required = parser.add_argument_group('required arguments')

    required.add_argument(
        '--name', help="Basename of the sound files", required=True)

    required.add_argument(
        '--total', help="Total number of files", required=True, type=int)

    args = parser.parse_args()
    name = args.name
    total = args.total

    total_str = str(total - 1)

    with open("fileids", 'w') as f:
        for i in range(total):
            i_zeroed = str(i).rjust(len(total_str), '0')
            f.write(name + '_' + str(i_zeroed) + '\n')
