from helper import get_sentences
import argparse
import spacy
import pickle
import os
import logging
from nltk.util import ngrams
from helper import get_vec

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
        Tool for extracting semantic vectors from a given email corpus
    ''')
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input', help="Input directory that contains the email data (one sentence per line)", required=True)

    required.add_argument(
        '--n', help="Size of ngrams", nargs='+', type=int, required=True)

    required.add_argument(
        '--output', help="Output pickle file that holds the vectors of the corpus", required=True)

    args = parser.parse_args()
    input = args.input
    n = args.n
    output = args.output

    if not input.endswith('/'):
        input = input + '/'

    logging.info('Reading emails corpus...')
    sentences = get_sentences(input)

    logging.info('Getting vectors of emails corpus...')
    vectors = get_vec(sentences, n)

    # Pickling pos
    with open(output + '.pkl', "wb") as fp:
        pickle.dump(vectors, fp)
