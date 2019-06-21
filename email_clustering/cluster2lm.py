import subprocess
import os
import argparse

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool for converting text to language model using srilm toolkit
    ''')

    required = parser.add_argument_group('required arguments')
    required.add_argument(
        '--input', help="Input directory that contains the clusters", required=True)

    args = parser.parse_args()
    input = args.input
    for cluster in os.listdir(input):
        cluster_path = os.path.join(input, cluster)
        if subprocess.call(['ngram-count -kndiscount -interpolate -text ' + os.path.join(cluster_path, 'corpus') + ' -wbdiscount1 -wbdiscount2 -wbdiscount3 -lm ' + os.path.join(cluster_path, 'model.lm')], shell=True):
            sys.exit('Error in subprocess')
