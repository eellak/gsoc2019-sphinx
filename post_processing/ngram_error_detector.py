import argparse
import sys
import os
import arpa
from nltk.util import ngrams
from helper import get_hypothesis
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
        Not ready yet
    ''')
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input', help="Input file that contains one sentence per line", required=True)

    required.add_argument(
        '--lm', help="Input language model", required=True)

    required.add_argument(
        '--n', help="Size of n-gram", required=True, type=int)

    required.add_argument(
        '--threshold', help="Threshold for error detection (%100)", required=True, type=float)

    args = parser.parse_args()
    input = args.input
    lm = args.lm
    n = args.n
    threshold = args.threshold / 100

    sentences = get_hypothesis(input, True)

    # Reading input language model.
    models = arpa.loadf(lm)
    # ARPA files may contain several models.
    lm = models[0]

    for sent in sentences:
        print(sent)
        n_grams = ngrams(sent.split(), n)
        for n_gram in list(n_grams):
            prop = lm.p(n_gram)
            if prop < threshold:
                print(n_gram)
                print(prop)
