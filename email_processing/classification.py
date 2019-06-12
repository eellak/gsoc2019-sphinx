import requests
import os
from extraction import connect, read_emails, mime2str


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


def save_texts(categories):
    '''Save the emails of each category in a txt file in order to build the
        topic-specific language model.

        Args:
            categories: A dictionary that has the category name in Greek as key and a
                list with the emails of this category as value.
    '''

    for category in categories:
        with open('./categories/' + category, 'w') as w:
            for email in categories[category]:
                w.write(email + '\n')


def save_texts_together(categories):
    '''Save all the emails in one file.

        Args:
            categories: A dictionary that has the category name in Greek as key and a
                list with the emails of this category as value.
    '''

    with open('All', 'w') as w:
        for category in categories:
            for email in categories[category]:
                w.write(email + '\n')


if __name__ == '__main__':
    emails = []
    for email in os.listdir('./texts'):
        with open('./texts/' + email, 'r') as f:
            emails.append(f.read())

    categories = classify_emails(emails)
    save_texts_together(categories)
    save_texts(categories)
