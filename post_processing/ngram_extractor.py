import argparse
import pickle
import sys
from nltk.util import ngrams
from helper import get_ngrams, get_sentences

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
        Tool for extracting ngrams from a given email corpus
    ''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input', help="Input sentence", required=True)

    required.add_argument(
        '--n', help="Size of ngrams", nargs='+', type=int)

    required.add_argument(
        '--output', help="Output file",)

    args = parser.parse_args()
    input = args.input
    n = args.n
    output = args.output

    sentences = get_sentences(input)

    corpus = get_ngrams(sentences, n)

    # Pickling ngrams
    with open(output + '.pkl', "wb") as fp:
        pickle.dump(corpus, fp)
