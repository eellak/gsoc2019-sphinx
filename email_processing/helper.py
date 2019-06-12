from alphabet_detector import AlphabetDetector
import string
import re

'''
    This sript contains some helper functions
    for extracting emails from a user's account.
'''


def process_text(text):
    '''Clean a text in order to be used in a language model.

        Args:
            text: A string containing the text.
        Returns:
            out: A string containing the only lowercase alphabetic characters.

        '''
    out = ""
    # If a line starts with these, remove it.
    words_to_stop = ['---------- Forwarded message ---------',
                     '---------- Προωθημένο μήνυμα ----------']
    # Checks if a word is Greek
    ad = AlphabetDetector()
    # Regex that matches lines that contain the date of the message.
    date = re.compile('.*-.*-.*:.*')
    lines = text.split('\n')
    for i in range(len(lines)):
        # If line is in the form yyyy-mm-dd hh:mm, remove it.
        if date.match(lines[i]) is not None:
            continue
        elif any(w in lines[i] for w in words_to_stop):
            break
        # Lines with '--' are the signature and lines with '>'
        # represent previous conversations.
        elif lines[i].startswith('--') or lines[i].startswith('>'):
            break
        elif lines[i].startswith('Στις') and lines[i].strip().endswith('έγραψε:'):
            break
        elif lines[i].startswith('On') and lines[i].strip().endswith('wrote:'):
            break
        elif i < len(lines) - 1 and lines[i].startswith('Στις') and lines[i + 1].strip().endswith('έγραψε:'):
            break
        # Remove non-greek words.
        else:
            for word in lines[i].split(' '):
                if ad.only_alphabet_chars(word, "GREEK"):
                    out += word + ' '

    # Break line in sentences.
    out.replace("\r", "").replace(".", ".\n")
    # split into tokens by white space
    tokens = out.split()
    # remove punctuation from each token
    table = str.maketrans('', '', string.punctuation)
    tokens = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    tokens = [word for word in tokens if word.isalpha()]
    # make lower case
    tokens = [word.lower() for word in tokens]
    return ' '.join(tokens)


def save_messages(body_messages, header_messages):
    '''Save messages in separate files and keeps an info file with the headers.

        Args:
            body_messages: A list of strings that contains the body of the messages.
            header_messages: A list of strings that contains the header of the messages.

        '''
    # Keep an info file that contains the sender, the
    # receiver and the subject of the message.
    with open('info', 'w') as w1:
        for i, msg in enumerate(body_messages):
            with open('./texts/email_' + str(i), 'w') as w2:
                w1.write(
                    header_messages[i][0] + ' | ' + header_messages[i][1] + ' | ' + header_messages[i][2])
                w1.write('\n')
                w2.write(msg)
