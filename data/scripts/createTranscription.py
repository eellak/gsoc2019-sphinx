import argparse
import os

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument(
        '--input', help="Folder that contains the texts", required=True)
    required.add_argument(
        '--output', help="Path to save the output", required=True)
    required.add_argument(
        '--name', help="Name of the dataset", required=True)

    args = parser.parse_args()
    input = args.input
    output = args.output
    name = args.name

    with open(output, 'w') as w:
        for text in sorted(os.listdir(input)):
            id = text.split(name + '_')[-1]
            with open(os.path.join(input, text), 'r') as f:
                w.write(f.read().replace("\n", " "))
                w.write(' (' + name + '_' + str(id) + ')')
                w.write('\n')
