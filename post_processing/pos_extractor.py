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
        Tool for extracting POS tagging of the sentences of the emails
    ''')
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input', help="Input directory that contains the email data (one sentence per line)", required=True)
    required.add_argument(
        '--output', help="Output pickle file that holds the pos tagging of the corpus", required=True)

    optional.add_argument(
        '--size', help="Size of the words sequence to consider. If not set, all the sentence is taken.", type=int)

    args = parser.parse_args()
    input = args.input
    output = args.output
    size = args.size

    if not input.endswith('/'):
        input = input + '/'

    logging.info('Reading emails corpus...')
    sentences = get_sentences(input)

    logging.info('Getting POS tagging of emails corpus...')
    pos_corpus = get_pos_sentence(sentences, size)

    # Pickling pos
    with open(output + '.pkl', "wb") as fp:
        pickle.dump(pos_corpus, fp)
