import argparse
import spacy
import pickle
from helper import closest_pos, closest_vec, closest_ngram
import sys
from nltk.util import ngrams
from helper import get_pos_doc

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
        Tool for correcting error words in an email
    ''')
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input_sent', help="Pickle file that holds the sentences", required=True)

    required.add_argument(
        '--errors', help="Pickle file that holds the errors of input sentences", required=True)

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

    args = parser.parse_args()
    input_sent = args.input_sent
    errors = args.errors
    method = args.method

    pos_path = args.pos
    vec_path = args.vec
    ngram_path = args.ngram
    weight = args.weight

    # Check input paths
    if method == 'pos' and pos_path is None:
        sys.exit('Give pos tagging pickle file')
    if method == 'semantic' and vec_path is None:
        sys.exit('Give vectors pickle file')
    if method == 'word' and ngram_path is None:
        sys.exit('Give ngrams pickle file')

    with open(input_sent, 'rb') as f:
        sentences = pickle.load(f)
    with open(errors, 'rb') as f:
        errors = pickle.load(f)

    if method == 'pos':
        # Load Greek spacy model.
        nlp = spacy.load('el_core_news_sm')
        # Load pos tags of corpus
        with open(pos_path, 'rb') as f:
            pos_corpus = pickle.load(f)

        for i, sent in enumerate(sentences):
            words = sent.split()
            for j, word in enumerate(words):
                if errors[i][j] == 0:
                    continue
                window = " ".join([words[j - 1], words[j]])
                print(window)
                doc = get_pos_doc(nlp(window))
                print(closest_pos(window, doc, pos_corpus, w=weight))
    elif method == 'semantic':
        # Load Greek spacy model.
        nlp = spacy.load('el_core_news_md')
        # Load pos tags of corpus
        with open(vec_path, 'rb') as f:
            vec_corpus = pickle.load(f)

        for i, sent in enumerate(sentences):
            words = sent.split()
            for j, word in enumerate(words):
                if errors[i][j] == 0:
                    continue
                window = " ".join([words[j - 1], words[j]])
                print(window)
                doc = nlp(window).vector
                print(closest_vec(window, doc, vec_corpus, w=weight))
    else:
        # Load pos tags of corpus
        with open(ngram_path, 'rb') as f:
            ngram_corpus = pickle.load(f)

        for i, sent in enumerate(sentences):
            words = sent.split()
            for j, word in enumerate(words):
                if errors[i][j] == 0:
                    continue
                window = " ".join([words[j - 1], words[j]])
                print(window)
                print(closest_ngram(window, ngram_corpus))
