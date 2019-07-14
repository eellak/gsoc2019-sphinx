from gensim.models.fasttext import FastText
import argparse
from helper import get_sentences

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool for training different kind of embeddings on email corpus
    ''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input', help="Input directory that contains the emails", required=True)
    required.add_argument(
        '--size', help="Dimensionality of word vectors", required=True, type=int)

    args = parser.parse_args()
    input = args.input
    vec_size = args.size

    if not input.endswith('/'):
        input = input + '/'

    sentences = get_sentences(input)

    sent_token = []
    for sent in sentences:
        sent_token.append(sent.strip('\n').split(' '))

    model = FastText(sent_token, sg=1, hs=1, size=vec_size,
                     workers=4)

    model.save('test')
