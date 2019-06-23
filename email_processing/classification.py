import requests
import os
from extraction import connect, read_emails, mime2str
from helper import get_emails
import argparse


def classify(text):
    '''Classify a given text using an already trained classifier
        (link https://github.com/eellak/gsoc2018-spacy).

        Args:
            text: A string that containes the text to be classified.
        Returns:
            The category of the text, if found.

        '''
    url = 'https://nlp.wordgames.gr/api/analyze'
    res = requests.post(url, json={'text': text})
    if res.status_code == 200:
        if 'category' in res.json():
            return res.json()['category'].strip()
        else:
            return 'Unable to find category'
    else:
        return 'Server Error'


def classify_emails(emails):
    '''Get the categories of emails.

        Args:
            emails: A list of emails in string format.
        Returns:
            categories: A dictionary that has the category name in Greek as key and a
                list with the emails of this category as value.
        '''

    categories = {'Αθλητισμός': [], 'Ελλάδα': [], 'Επιστήμη': [], 'Κόσμος': [],
                  'Οικονομία': [], 'Περιβάλλον': [], 'Πολιτική': [], 'Τέχνες': [], 'Υγεία': [], 'Άλλα': []}
    for email in emails:
        category = classify(email)
        if category in categories:
            categories[category].append(email)
        else:
            categories['Άλλα'].append(email)
    return categories


def save_texts(categories, output):
    '''Save the emails of each category in a txt file in order to build the
        topic-specific language model.

        Args:
            categories: A dictionary that has the category name in Greek as key and a
                list with the emails of this category as value.
    '''
    # If output directory does not exist, create it.
    if not os.path.exists(output):
        os.makedirs(output)

    for category in categories:
        with open('./' + output + category, 'w') as w:
            for email in categories[category]:
                w.write(email + '\n')

    with open('./' + output + 'General', 'w') as w:
        for category in categories:
            for email in categories[category]:
                w.write(email + '\n')


if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Classify emails in predefined categories. More info on the classifier here: https://github.com/eellak/nlpbuddy/wiki/Category-prediction
    ''')
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('--input', help="Input directory", required=True)
    required.add_argument('--output', help="Output directory", required=True)

    args = parser.parse_args()
    output = args.output
    input = args.input

    if not input.endswith('/'):
        input = input + '/'
    if not output.endswith('/'):
        output = output + '/'

    emails = get_emails('./' + input)
    categories = classify_emails(emails)

    save_texts(categories, output)
