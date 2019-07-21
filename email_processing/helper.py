#!/usr/bin/python
# -*- coding: utf-8 -*-

from alphabet_detector import AlphabetDetector
import string
import re
import os
import sys
import nltk
from nltk.tokenize import sent_tokenize
from convert_num import converter

'''
    This sript contains some helper functions
    for processing emails from a user's account.
'''


def process_text(text):
    '''Clean a text in order to be used in a language model.

        Args:
            text: A string containing the text.
        Returns:
            out_clean: A string containing the clean text.

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
    # Remove useless lines.
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
                # Keep dot after non-Greek word.
                elif word.strip().endswith('.'):
                    out += '. '
        out += '\n'
    # Break line in sentences.
    out = out.replace('\r', '')
    # Set salutation as a separate sentence.
    lines = out.split('\n')
    if lines[0].strip('\n').strip().endswith(',') and (len(lines[1].strip('\n').strip()) == 0 or lines[1].isupper()):
        lines[0] = lines[0].strip('\n').strip()[:-1] + '.'
    out = '\n'.join(lines)

    sentences = sent_tokenize(out)
    table = str.maketrans(string.punctuation,
                          ' ' * len(string.punctuation))
    sentences = [sent.translate(table) for sent in sentences]
    out_clean = []
    for sent in sentences:
        # split into tokens by white space
        tokens = sent.split()
        # remove remaining tokens that are not alphabetic or numeric.
        toks = []
        for token in tokens:
            if token.isdigit():
                # Convert numeric tokens in Greek text.
                toks.append(converter(token))
            elif token.isalpha():
                toks.append(token)
        # make lower case
        toks = [word.lower() for word in toks]
        if toks:
            out_clean.append(' '.join(toks))
    return out_clean


def save_messages(body_messages, header_messages, out, info, sentence):
    '''Save messages in separate files and keeps an info file with the headers.

        Args:
            body_messages: A list of strings that contains the body of the messages.
            header_messages: A list of strings that contains the header of the messages.
            out: The directory to store the emails.
            info: If true, a file that contains the headers is saved too.
            sentence: If true, save each sentence in a separate file.

        '''
    # If output directory does not exist, create it.
    if not os.path.exists(out):
        os.makedirs(out)

    # Keep an info file that contains the sender, the
    # receiver and the subject of the message.
    if info:
        with open('./' + out + 'info', 'w') as w1:
            for i, msg in enumerate(body_messages):
                w1.write(
                    header_messages[i][0] + ' | ' + header_messages[i][1] + ' | ' + header_messages[i][2])
                w1.write('\n')

    if sentence:
        # Compute total number of sentences.
        total = 0
        for body in body_messages:
            for sent in body:
                total += 1
        total_str = str(total - 1)
        i = 0
        for msg in body_messages:
            for sent in msg:
                # Add leading zeros in order to have all names in the right order.
                i_zeroed = str(i).rjust(len(total_str), '0')
                with open('./' + out + 'data_' + i_zeroed, 'w') as w2:
                    w2.write(sent + '\n')
                i += 1
    else:
        total_str = str(len(body_messages) - 1)
        for i, msg in enumerate(body_messages):
            # Add leading zeros in order to have all names in the right order.
            i_zeroed = str(i).rjust(len(total_str), '0')
            with open('./' + out + 'data_' + i_zeroed, 'w') as w2:
                for sent in msg:
                    w2.write(sent + '\n')


def get_emails(dir):
    '''Get emails from a specific directory and return them as a list.

        Args:
            dir: Directory that contains the emails in text files.
        Returns:
            emails: A list that contains the emails in string format.

        '''
    # If input directory does not exist, exit with error.
    if not os.path.exists(dir):
        sys.exit('Email folder does not exist')

    emails = []
    for email in os.listdir(dir):
        with open(dir + email, 'r') as f:
            emails.append(f.read())
    return emails
