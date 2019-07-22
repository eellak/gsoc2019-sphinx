from helper import get_sentences
import argparse
import spacy
import pickle
import os
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

def get_pos(sentences):
    pos_tagging = []
    nlp = spacy.load('el_core_news_sm')
    for sent in sentences:
        tags = []
        texts = []
        doc = nlp(sent)
        for token in doc:
            tags.append(token.pos_)
            texts.append(token.text)
        if tags:
            pos_tagging.append((" ".join(texts), " ".join(tags)))
    return pos_tagging


if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool for extracting POS tagging of the sentences of the emails
    ''')
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input', help="Input directory that contains the email data (one sentence per line)", required=True)
    required.add_argument(
        '--output', help="Output pickle file that holds the pos tagging of the corpus", required=True)

    args = parser.parse_args()
    input = args.input
    output = args.output

    if not input.endswith('/'):
        input = input + '/'

    logging.info('Reading emails corpus...')
    sentences = get_sentences(input)

    logging.info('Getting POS tagging of emails corpus...')
    pos = get_pos(sentences)
    
    # Pickling pos
    with open(output + '.pkl', "wb") as fp:
        pickle.dump(pos, fp)
