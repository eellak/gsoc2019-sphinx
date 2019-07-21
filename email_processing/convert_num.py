#!/usr/bin/python
# -*- coding: utf-8 -*-

from num2words import num2words
import re
from collections import OrderedDict

# Define an ordered dictionary that matches English
# to the corresponging Greek characters.
rep = OrderedDict([('one thousand', u'χίλια'),
                   ('one hundred', u'εκατό'),
                   ('one million', u'ένα εκατομμύριο'),
                   ('one billion', u'ένα δισεκατομμύριο'),
                   ('one trillion', u'ένα τρισεκατομμύριο'),
                   ('two hundred', u'διακόσια'),
                   ('three hundred', u'τριακόσια'),
                   ('four hundred', u'τετρακόσια'),
                   ('five hundred', u'πεντακόσια'),
                   ('six hundred', u'εξακόσια'),
                   ('seven hundred', u'εφτακόσια'),
                   ('eight hundred', u'οχτακόσια'),
                   ('nine hundred', u'εννιακόσια'),
                   ('ten', u'δέκα'),
                   ('eleven', u'έντεκα'),
                   ('twelve', u'δώδεκα'),
                   ('thirteen', u'δέκα τρία'),
                   ('fourteen', u'δέκα τέσσερα'),
                   ('fifteen', u'δέκα πέντε'),
                   ('sixteen', u'δέκα έξι'),
                   ('seventeen', u'δέκα εφτά'),
                   ('eighteen', u'δέκα οκτώ'),
                   ('nineteen', u'δέκα εννιά'),
                   ('twenty', u'είκοσι'),
                   ('thirty', u'τριάντα'),
                   ('forty', u'σαράντα'),
                   ('fifty', u'πενήντα'),
                   ('sixty', u'εξήντα'),
                   ('seventy', u'εβδομήντα'),
                   ('eighty', u'ογδόντα'),
                   ('ninety', u'ενενήντα'),
                   ('zero', u'μηδέν'),
                   ('one', u'ένα'),
                   ('two', u'δύο'),
                   ('three', u'τρία'),
                   ('four', u'τέσσερα'),
                   ('five', u'πέντε'),
                   ('six', u'έξι'),
                   ('seven', u'εφτά'),
                   ('eight', u'οκτώ'),
                   ('nine', u'εννιά'),
                   ('hundred', u'εκατοντάδες'),
                   ('thousand', u'χιλιάδες'),
                   ('million', u'εκατομμύρια'),
                   ('billion', u'δισεκατομμύρια'),
                   ('trillion', u'τρισεκατομμύρια'),
                   ('point', u'κόμμα'),
                   ('-', ' ')])


def converter(num):
    '''Converts a number to Greek text.

        Args:
            num: A string representing a number.
        Returns:
            gr_text: A string representing the number in Greek text.

        '''
    en_txt = num2words(num)
    en_txt = en_txt.replace(' and ', ' ').replace(',', '')
    en_txt = en_txt.split()
    pairs = []

    if len(en_txt) > 1:
        for i in range(0, len(en_txt) // 2):
            pairs.append(en_txt[2 * i] + ' ' + en_txt[2 * i + 1])

    if len(en_txt) % 2 == 1:
        pairs.append(en_txt[-1])

    gr_txt = ""
    for p in pairs:
        for i, j in rep.items():
            p = p.replace(i, j)
        gr_txt += p + ' '

    if len(pairs) > 1:
        gr_txt = gr_txt.replace('εκατό', 'εκατόν')

    return gr_txt
