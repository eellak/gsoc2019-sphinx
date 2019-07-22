import argparse
import spacy
import pickle
from helper import closest_pos_sentence, closest_semantic_sentence
import sys
from nltk.util import ngrams
from helper import get_pos_doc

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
        Tool for detecting error words in an email based on POS tagging of an email corpus
    ''')
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input', help="Input sentence", required=True)
    required.add_argument(
        '--method', help="Method to be used for finding errors", choices=['pos', 'semantic'], required=True)

    optional.add_argument(
        '--pos', help="Pos tags of emails in pickle format if pos method is chosen")
    optional.add_argument(
        '--vec', help="Vectors of emails in pickle format if semantic method is chosen")
    optional.add_argument(
        '--weight', help="Weight in computing the min distance", type=float, default=0.5)
    optional.add_argument(
        '--size', help="Size of the words sequence to consider. If not set, all the sentence is taken.", type=int)

    args = parser.parse_args()
    input = args.input
    method = args.method

    pos_path = args.pos
    vec_path = args.vec
    weight = args.weight
    size = args.size

    # Check input paths
    if method == 'pos' and pos_path is None:
        sys.exit('Give pos tagging pickle file')
    if method == 'semantic' and vec_path is None:
        sys.exit('Give vectors pickle file')

    if method == 'pos':
        # Load Greek spacy model.
        nlp = spacy.load('el_core_news_sm')
        # Load pos tags of corpus
        with open(pos_path, 'rb') as f:
            pos_corpus = pickle.load(f)

        if size is None:
            doc = nlp(input)
            pos_input = get_pos_doc(doc)
            print(closest_pos_sentence(input, pos_input, pos_corpus, w=weight))
        else:
            n_grams = ngrams(input.split(), size)
            for n_gram in list(n_grams):
                n_gram_text = ' '.join(n_gram)
                doc = get_pos_doc(nlp(n_gram_text))
                print(closest_pos_sentence(
                    n_gram_text, doc, pos_corpus, w=weight))
    else:
        # Load Greek spacy model.
        nlp = spacy.load('el_core_news_md')
        # Load vectors of corpus
        with open(vec_path, 'rb') as f:
            vec_corpus = pickle.load(f)
        if size is None:
            vec_input = nlp(input).vector
            print(closest_semantic_sentence(
                input, vec_input, vec_corpus, w=weight))
        else:
            n_grams = ngrams(input.split(), size)
            for n_gram in list(n_grams):
                n_gram_text = ' '.join(n_gram)
                doc = nlp(n_gram_text).vector
                print(closest_semantic_sentence(n_gram_text, doc,
                                                vec_corpus, w=weight))
