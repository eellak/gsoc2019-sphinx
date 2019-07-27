import argparse
import spacy
import pickle
from helper import closest_pos, closest_vec, closest_ngram
import sys
from nltk.util import ngrams
from helper import get_pos_doc, get_hypothesis
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
        Tool for correcting error words in an email
    ''')
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input_sent', help="Input file that contains the asr output (one sentence per line)", required=True)

    required.add_argument(
        '--input_errors', help="Pickle file that holds the errors of input sentences", required=True)

    required.add_argument(
        '--method', help="Method to be used for finding errors", choices=['pos', 'semantic', 'word'], required=True)

    optional.add_argument(
        '--pos', help="Pos tags of emails in pickle format if pos method is chosen")
    optional.add_argument(
        '--vec', help="Vectors of emails in pickle format if semantic method is chosen")
    optional.add_argument(
        '--ngram', help="Ngrams of emails in pickle format if word method is chosen")

    optional.add_argument(
        '--weight', help="Weight in computing the min distance", type=float, default=0.5)

    optional.add_argument(
        '--save', help="Save corrected ASR output", action='store_true')
    optional.add_argument(
        '--output', help="If save is true, this is the path to the output file")

    args = parser.parse_args()
    input_sent = args.input_sent
    errors = args.input_errors
    method = args.method

    pos_path = args.pos
    vec_path = args.vec
    ngram_path = args.ngram
    weight = args.weight
    save = args.save
    output = args.output

    # Check input paths
    if method == 'pos' and pos_path is None:
        sys.exit('Give pos tagging pickle file')
    if method == 'semantic' and vec_path is None:
        sys.exit('Give vectors pickle file')
    if method == 'word' and ngram_path is None:
        sys.exit('Give ngrams pickle file')
    if save and output is None:
        sys.exit('Give output file')

    sentences = get_hypothesis(input_sent, True)
    with open(errors, 'rb') as f:
        errors = pickle.load(f)

    corrected_input = []
    if method == 'pos':
        # Load Greek spacy model.
        nlp = spacy.load('el_core_news_sm')
        # Load pos tags of corpus
        with open(pos_path, 'rb') as f:
            pos_corpus = pickle.load(f)

        for i, sent in enumerate(sentences):
            print(sent)
            words = sent.split()
            corrected_words = words.copy()
            for j, word in enumerate(words):
                if errors[i][j] == 0:
                    continue
                window = " ".join([words[j - 1], words[j]])
                doc = get_pos_doc(nlp(window))
                print(window)
                min_sent, word_dist, pos_dist = closest_pos(
                    window, doc, pos_corpus, w=weight)
                print(min_sent)
                corrected_words[j] = " ".join(min_sent[0].split()[1:])
            corrected_input.append(" ".join(corrected_words))

    elif method == 'semantic':
        # Load Greek spacy model.
        nlp = spacy.load('el_core_news_md')
        # Load pos tags of corpus
        with open(vec_path, 'rb') as f:
            vec_corpus = pickle.load(f)

        for i, sent in enumerate(sentences):
            print(sent)
            words = sent.split()
            corrected_words = words.copy()
            for j, word in enumerate(words):
                if errors[i][j] == 0:
                    continue
                window = " ".join([words[j - 1], words[j]])
                print(window)
                doc = nlp(window).vector
                min_sent, word_dist, pos_dist = closest_vec(
                    window, doc, vec_corpus, w=weight)
                print(min_sent)
                corrected_words[j] = " ".join(min_sent[0].split()[1:])
            corrected_input.append(" ".join(corrected_words))
    else:
        # Load pos tags of corpus
        with open(ngram_path, 'rb') as f:
            ngram_corpus = pickle.load(f)

        for i, sent in enumerate(sentences):
            print(sent)
            words = sent.split()
            corrected_words = words.copy()
            for j, word in enumerate(words):
                if errors[i][j] == 0:
                    continue
                window = " ".join([words[j - 1], words[j]])
                print(window)
                min_sent, distance = closest_ngram(
                    window, ngram_corpus)
                print(min_sent)
                corrected_words[j] = " ".join(min_sent[0].split()[1:])
            corrected_input.append(" ".join(corrected_words))

    p = re.compile(r'\([^)]*\)$')
    with open(output, 'w') as fw, open(input_sent, 'r') as fr:
        for i, line in enumerate(fr):
            m = p.search(line)
            idx = m.group(0).split()[0].split('(')[1]
            fw.write(corrected_input[i].strip('\n') + ' ' + '(' + idx + ')')
            fw.write('\n')
