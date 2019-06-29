from helper import get_emails
import argparse
import spacy

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool for extracting POS tagging of emails
    ''')
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input', help="Input directory", required=True)

    args = parser.parse_args()
    input = args.input

    if not input.endswith('/'):
        input = input + '/'

    emails = get_emails(input)
    nlp = spacy.load('el_core_news_sm')

    for email in emails:
        for sentence in email.split('\n'):
            doc = nlp(sentence)
            print(sentence)
            for token in doc:
                print(token.pos_, end=' ')
            print()
