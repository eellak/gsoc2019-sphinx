import argparse
import spacy
import pickle

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool for detecting error words in an email based on POS tagging of previous emails
    ''')
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input', help="Input email", required=True)
    required.add_argument(
        '--pos', help="Pos tags of emails in pickle format", required=True)

    args = parser.parse_args()
    input = args.input
    pos_path = args.pos

    nlp = spacy.load('el_core_news_sm')
    pos_tag = []
    for sentence in input.split('\n'):
        sentence_tag = []
        doc = nlp(sentence)
        for token in doc:
            sentence_tag.append((token.text, token.pos_))
        pos_tag.append(sentence_tag)

    with open(pos_path, 'rb') as f:
        pos_emails = pickle.load(f)
