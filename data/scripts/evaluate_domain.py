import os
import argparse
import subprocess


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool for evaluating a domain-specific language model (output of decode.py)
    ''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input', help="Folder that contains the clusters of the test set along with their hypothesis (output of decode.py)", required=True)

    args = parser.parse_args()
    input = args.input

    lines = []
    accuracies = []
    total_accuracy = 0
    for cluster in os.listdir(input):
        cluster_path = os.path.join(input, cluster)
        trans = os.path.join(cluster_path, 'transription')
        merged = os.path.join(cluster_path, 'merged.hyp')
        command = 'word_align.pl ' + trans + ' ' + merged + \
            ' | tail -2 | head -1 | cut -d " " -f11'
        result = subprocess.check_output(
            command, shell=True).decode('utf-8')
        accuracy = float(result.strip('\n')[:-1])
        accuracies.append(accuracy)
        line = file_len(os.path.join(cluster_path, 'fileids'))
        lines.append(line)
        total_accuracy += line * accuracy

    total_accuracy = total_accuracy / sum(lines)
    print(accuracies)
    print(lines)

    print(total_accuracy)
