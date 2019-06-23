import subprocess
import os
import argparse
import sys

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool for converting text to language model using srilm toolkit
    ''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument(
        '--input', help="Input directory that contains the clusters", required=True)
    optional.add_argument(
        '--mix', help="If set, create a merged lm with the given model")

    args = parser.parse_args()
    input = args.input
    mix = args.mix
    for cluster in os.listdir(input):
        cluster_path = os.path.join(input, cluster)
        if os.path.isdir(cluster_path):
            if subprocess.call(['ngram-count -kndiscount -interpolate -text ' + os.path.join(cluster_path, 'corpus') + ' -wbdiscount1 -wbdiscount2 -wbdiscount3 -lm ' + os.path.join(cluster_path, 'model.lm')], shell=True):
                sys.exit('Error in subprocess')
            if mix is not None:
                if subprocess.call(['ngram -lm ' + mix + ' -mix-lm ' + os.path.join(cluster_path, 'model.lm') + ' -lambda 0.5 -write-lm ' + os.path.join(cluster_path, 'merged.lm')], shell=True):
                    sys.exit('Error in subprocess')
