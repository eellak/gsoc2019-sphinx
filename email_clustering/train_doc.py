from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import argparse
from helper import get_sentences
import os
from multiprocessing import cpu_count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
        Tool for training doc2vec embeddings on email corpus
    ''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input', help="Input directory that contains the emails", required=True)
    required.add_argument(
        '--size', help="Dimensionality of vectors", required=True, type=int)
    required.add_argument(
        '--output', help="Output directory", required=True)

    args = parser.parse_args()
    input = args.input
    vec_size = args.size
    output = args.output

    if not input.endswith('/'):
        input = input + '/'
    if not output.endswith('/'):
        output = output + '/'
    if not os.path.exists(output):
        os.makedirs(output)

    sentences = get_sentences(input)

    tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[
                                  str(i)]) for i, _d in enumerate(sentences)]

    max_epochs = 100
    alpha = 0.025

    model = Doc2Vec(size=vec_size,
                    alpha=alpha,
                    min_alpha=0.00025,
                    min_count=1,
                    dm=1)

    model.build_vocab(tagged_data)

    for epoch in range(max_epochs):
        print('iteration {0}'.format(epoch))
        model.train(tagged_data,
                    total_examples=model.corpus_count,
                    epochs=model.iter)
        # decrease the learning rate
        model.alpha -= 0.0002
        # fix the learning rate, no decay
        model.min_alpha = model.alpha

    model.save("d2v.model")
    print("Model Saved")
