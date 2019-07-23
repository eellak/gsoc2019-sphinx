import argparse
import sys
import os
import arpa
from nltk.util import ngrams
from helper import get_hypothesis
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
        Tool for detecting error words in ASR output
    ''')
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input', help="Input file that contains one sentence per line", required=True)

    required.add_argument(
        '--lm', help="Input language model", required=True)

    required.add_argument(
        '--n', help="Size of n-gram", required=True, type=int)

    required.add_argument(
        '--threshold', help="Threshold for error detection", required=True, type=float)

    args = parser.parse_args()
    input = args.input
    lm = args.lm
    n = args.n
    threshold = args.threshold / 100

    sentences = get_hypothesis(input, True)

    # Reading input language model.
    models = arpa.loadf(lm)
    # ARPA files may contain several models.
    lm = models[0]
    # For each sentence find words that have low propability
    # and keep a score of them.
    errors = []
    for sent in sentences:
        words = sent.split()
        scores = dict(zip(words, [0] * len(words)))
        n_grams = list(ngrams(words, n))
        for n_gram in n_grams:
            prop = lm.p(n_gram)
            if prop < threshold:
                for word in n_gram:
                    scores[word] += 1
        sent_errors = [0]
        for n_gram in n_grams:
            if scores[n_gram[1]] > 1:
                sent_errors.append(1)
            else:
                sent_errors.append(0)
        sent_errors.append(0)

        errors.append(sent_errors)

    print(sentences)
    print(errors)
