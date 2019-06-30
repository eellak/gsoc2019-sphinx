from helper import get_emails
import argparse
import spacy
import pickle
import os


def get_pos(emails):
    pos_tagging = []
    nlp = spacy.load('el_core_news_sm')
    for email in emails:
        for sentence in email.split('\n'):
            sentence_tag = []
            doc = nlp(sentence)
            for token in doc:
                sentence_tag.append((token.text, token.pos_))
            if sentence_tag:
                pos_tagging.append(sentence_tag)
    return pos_tagging


if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool for extracting POS tagging of emails
    ''')
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input', help="Input directory that contains the email data", required=True)
    required.add_argument(
        '--output', help="Output pickle file that holds the pos tagging of the corpus", required=True)
    args = parser.parse_args()
    input = args.input
    output = args.output

    if not input.endswith('/'):
        input = input + '/'

    emails = get_emails(input)

    pos = get_pos(emails)
    # Pickling pos
    with open(output + '.pkl', "wb") as fp:
        pickle.dump(pos, fp)
