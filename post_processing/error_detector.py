import argparse
import spacy
import pickle
from helper import closest_sentence, pos2str

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
    optional.add_argument(
        '--weight', help="Weight in computing the min distance", type=float, default=0.5)

    args = parser.parse_args()
    input = args.input
    pos_path = args.pos
    weight = args.weight

    # Get POS tag of input email
    nlp = spacy.load('el_core_news_sm')
    pos_input = []
    for sentence in input.split('\n'):
        sentence_tag = []
        doc = nlp(sentence)
        for token in doc:
            sentence_tag.append((token.text, token.pos_))
        pos_input.append(sentence_tag)

    # Retrieve POS tags of fethed emails.
    with open(pos_path, 'rb') as f:
        pos_emails = pickle.load(f)

    pos_input_str, input_str = pos2str(pos_input)

    pos_emails_str, emails_str = pos2str(pos_emails)

    print(closest_sentence(
        input_str[0], pos_input_str[0], emails_str, pos_emails_str, w=weight))
