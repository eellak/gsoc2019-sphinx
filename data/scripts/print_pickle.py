import pickle
import argparse

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Help script that prints the contents of a pickle file.
    ''')

    required = parser.add_argument_group('required arguments')

    required.add_argument(
        '--input', help="Path of the pickle file", required=True)

    args = parser.parse_args()
    input = args.input

    with open(input, 'rb') as f:
        x = pickle.load(f)

    print(x)
