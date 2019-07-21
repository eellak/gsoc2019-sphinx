#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import sys

categories_name = ['Αθλητισμός', 'Ελλάδα', 'Επιστήμη', 'Κόσμος',
                   'Οικονομία', 'Περιβάλλον', 'Πολιτική', 'Τέχνες', 'Υγεία', 'Άλλα']


def build_specific():
    '''Create the language model for each topic by using the srilm toolkit.

    '''
    for category in categories_name:
        if subprocess.call(['ngram-count -kndiscount -interpolate -text ./categories/' + category + ' -wbdiscount1 -wbdiscount2 -wbdiscount3 -lm ./categories/' + category + '.lm'], shell=True):
            sys.exit('Error in subprocess')


def build_generic():
    '''Create the general language model by using the srilm toolkit.

    '''
    if subprocess.call(['ngram-count -kndiscount -interpolate -text All -wbdiscount1 -wbdiscount2 -wbdiscount3 -lm All.lm'], shell=True):
        sys.exit('Error in subprocess')


if __name__ == '__main__':
    build_specific()
    build_generic()
    print('Language models created')
