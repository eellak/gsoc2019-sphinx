from helper import get_sentences
import argparse
import spacy
import pickle
import os
import logging
from nltk.util import ngrams
from helper import get_pos_doc, get_pos_sentence

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
        Tool for extracting POS tagging from a given corpus
    ''')
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input', help="Input directory that contains the email data (one sentence per line)", required=True)

    required.add_argument(
        '--n', help="Size of ngrams to consider", nargs='+', type=int, required=True)

    required.add_argument(
        '--output', help="Output pickle file that holds the pos tagging of the corpus", required=True)

    args = parser.parse_args()
    input = args.input
    n = args.n
    output = args.output

    if not input.endswith('/'):
        input = input + '/'

    logging.info('Reading emails corpus...')
    sentences = get_sentences(input)

    logging.info('Getting POS tagging of emails corpus...')
    pos_corpus = get_pos_sentence(sentences, n)

    # Pickling pos
    with open(output + '.pkl', "wb") as fp:
        pickle.dump(pos_corpus, fp)
