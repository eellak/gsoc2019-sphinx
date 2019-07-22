from helper import get_sentences
import argparse
import spacy
import pickle
import os
import logging
from nltk.util import ngrams

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


def get_pos_doc(doc):
    tags_doc = []
    for tok in doc:
        tags_doc.append(tok.pos_)
    return " ".join(tags_doc)


def get_pos_sentence(sentences, size):
    tags_corpus = {}
    nlp = spacy.load('el_core_news_sm')
    if size is None:
        for sent in sentences:
            doc = nlp(sent)
            tags_corpus[sent] = get_pos_doc(doc)
    else:
        for sent in sentences:
            n_grams = ngrams(sent.split(), size)
            for n_gram in list(n_grams):
                n_gram_text = ' '.join(n_gram)
                doc = nlp(n_gram_text)
                if n_gram_text not in tags_corpus:
                    tags_corpus[n_gram_text] = get_pos_doc(doc)
    return tags_corpus


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
