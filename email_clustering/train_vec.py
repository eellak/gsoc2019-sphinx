from gensim.models.fasttext import FastText
from gensim.models import Word2Vec
import argparse
from helper import get_sentences
import os
from multiprocessing import cpu_count

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
        Tool for training different kind of embeddings on email corpus
    ''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input', help="Input directory that contains the emails", required=True)
    required.add_argument(
        '--size', help="Dimensionality of word vectors", required=True, type=int)
    required.add_argument('--type', help="Choose between FastText and Word2Vec",
                          choices=['fasttext', 'word2vec'], required=True)

    optional.add_argument(
        '--algorithm', help="Training algorithm to be used when choosing fasttext embeddings", choices=['skipgram', 'cbow'], default='skipgram')
    required.add_argument(
        '--output', help="Output directory", required=True)

    args = parser.parse_args()
    input = args.input
    vec_size = args.size
    type = args.type
    algorithm = args.algorithm
    output = args.output

    if not input.endswith('/'):
        input = input + '/'
    if not output.endswith('/'):
        output = output + '/'

    if not os.path.exists(output):
        os.makedirs(output)
    sentences = get_sentences(input)

    sent_token = []
    for sent in sentences:
        sent_token.append(sent.strip('\n').split(' '))

    if type == "fasttext":
        if algorithm == "skipgram":
            sg = 1
        else:
            sg = 0
        model = FastText(sent_token, sg=sg, hs=1, size=vec_size,
                         workers=cpu_count(), iter=100)
        model.save(os.path.join(output, algorithm + '.model'))
    else:
        model = Word2Vec(sent_token, size=vec_size,
                         window=3, workers=cpu_count(), iter=100)
        model.save(os.path.join(output, type + '.model'))
