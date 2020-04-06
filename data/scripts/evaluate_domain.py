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

    required.add_argument(
        '--mllr', help="True for mllr adaptation", action='store_true')

    required.add_argument(
        '--map', help="True for map adaptation", action='store_true')

    required.add_argument(
        '--specific', help="True for specific language model", action='store_true')

    args = parser.parse_args()
    input = args.input
    mllr = args.mllr
    map = args.map
    specific = args.specific

    lines = []
    accuracies = []
    total_accuracy = 0
    for cluster in sorted(os.listdir(input)):
        cluster_path = os.path.join(input, cluster)
        trans = os.path.join(cluster_path, 'transription')
        if not os.path.exists(trans):
            continue
        if mllr:
            hyp = os.path.join(cluster_path, 'mllr.hyp')
        elif map:
            hyp = os.path.join(cluster_path, 'map.hyp')
        else:
            if specific:
                hyp = os.path.join(cluster_path, 'specific.hyp')
            else:
                hyp = os.path.join(cluster_path, 'merged.hyp')
        command = 'word_align.pl ' + trans + ' ' + hyp + \
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
