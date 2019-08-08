#!/usr/bin/python
# -*- coding: utf-8 -*-

from alphabet_detector import AlphabetDetector
import string
import re
import os
import sys
import nltk
from nltk.tokenize import sent_tokenize
import urllib
import base64
import pickle
import os.path
import email
from email.header import decode_header
from email.iterators import typed_subpart_iterator
import chardet
from bs4 import BeautifulSoup
import argparse
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


def get_header(header_text, default="ascii"):
    '''Decode the specified header.

        Args:
            header_text: string that contains a header from a MIME message.
            default: default encoding
        Returns:
            header: decoded header.

        '''
    headers = decode_header(header_text)
    header_sections = []
    for text, charset in headers:
        if charset is not None:
            header_sections.append(str(text, charset or default))
        elif isinstance(text, (bytes, bytearray)):
            header_sections.append(text.decode("utf-8"))
        else:
            header_sections.append(text)
    return u"".join(header_sections)


def get_charset(message, default="ascii"):
    '''Get the charset of a message object.

        Args:
            message: MIME object
            default: default encoding
        Returns:
            charset of message

        '''
    if message.get_content_charset():
        return message.get_content_charset()

    if message.get_charset():
        return message.get_charset()

    return default


def get_body(message):
    '''Get the body of a message object.

        Args:
            message: MIME object
        Returns:
            body_part: string containg the body of the message

        '''
    # Check if the message is multipart.
    if message.is_multipart():
        # Get the plain text version only
        text_parts = [part for part in typed_subpart_iterator(
            message, 'text', 'plain')]
        body = []
        for part in text_parts:
            charset = get_charset(part, get_charset(message))
            if charset == "utf-8":
                body.append(str(part.get_payload(decode=True),
                                charset,
                                "replace"))
            else:
                body.append(part.get_payload())
        body_part = u"\n".join(body).strip()
        return body_part

    else:
        # If it is not multipart, the payload will be a string
        # representing the message body.
        charset = get_charset(message)
        if charset == "utf-8":
            body = str(message.get_payload(decode=True),
                       get_charset(message),
                       "replace")
        else:
            body = message.get_payload()
        body_part = body.strip()
        return body_part


def mime2str(msg):
    '''Convert a mime message in string format.

        Args:
            msg: A mime message.
        Returns:
            body: The body of the message as a string.
            headers: A list that contains the sender, the receiver
                and the subject of the message.

        '''
    text = get_body(msg)
    if text:
        headers = [get_header(msg["from"]), get_header(
            msg["to"]), get_header(msg["subject"])]

        return text, headers

    # Else return empty string.
    return "", ""
