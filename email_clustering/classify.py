import os
import argparse
from helper import closest_cluster, get_spacy, get_emails_from_transcription, get_trained_vec, get_trained_doc
import pickle

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool for classify new emails in clusters from k-means
    ''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input', help="Input transriptions (one per line)", required=True)
    required.add_argument(
        '--centers', help="Pickle file that contains the centers", required=True)
    required.add_argument(
        '--ids', help="Ids of the transcriptions", required=True)
    required.add_argument(
        '--metric', help="Metric to be used for finding closest cluster", choices=['euclidean', 'cosine'], default='euclidean', required=True)
    optional.add_argument(
        '--vector_type', help="Vector representation to be used", choices=['spacy', 'cbow', 'skipgram', 'word2vec', 'doc2vec'], default='spacy')
    optional.add_argument(
        '--vector_path', help="If cbow, fasttext or word2vec is selected, give the path of the trained embeddings")
    optional.add_argument(
        '--has_id', help="If set, each email contains his id in the end", action='store_true')
    optional.add_argument(
        '--save', help="If set, save labels in pickle format", action='store_true')

    args = parser.parse_args()
    input = args.input
    centers_path = args.centers
    ids_path = args.ids
    has_id = args.has_id
    save = args.save
    metric = args.metric
    vector_type = args.vector_type
    vector_path = args.vector_path

    # Read centers
    with open(centers_path, 'rb') as f:
        centers = pickle.load(f)

    ids = []
    with open(ids_path, 'r') as r:
        for line in r:
            ids.append(line.strip('\n'))

    # Get emails to classify
    emails = get_emails_from_transcription(input, has_id)
    # Represent them as vectors
    if vector_type == "spacy":
        vectors = get_spacy(emails)
    elif vector_type == 'doc2vec':
        vectors = get_trained_doc(emails, vector_path)
    elif vector_type == 'cbow':
        vectors = get_trained_vec(emails, vector_path, 'cbow')
    elif vector_type == 'skipgram':
        vectors = get_trained_vec(emails, vector_path, 'skipgram')
    else:
        vectors = get_trained_vec(emails, vector_path, 'word2vec')

    labels = {}
    for i, vec in enumerate(vectors):
        cluster = closest_cluster(centers, vec, metric)
        labels[ids[i]] = cluster

    # Save labels in pickle format
    if save:
        with open('labels.pickle', 'wb') as f:
            pickle.dump(labels, f)
