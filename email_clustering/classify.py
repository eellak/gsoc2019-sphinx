import os
import argparse
from helper import closest_cluster, get_spacy, get_emails_from_transcription, get_trained_vec, get_trained_doc
import pickle
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool for classify new emails in precomputed clusters
    ''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input', help="Input transriptions (one per line)", required=True)
    required.add_argument(
        '--centers', help="Pickle file that contains the centers of the clusters", required=True)
    required.add_argument(
        '--ids', help="File that contains the ids of the transcriptions", required=True)

    optional.add_argument(
        '--metric', help="Metric to be used for finding closest cluster", choices=['euclidean', 'cosine'], default='cosine')
    optional.add_argument(
        '--vector_type', help="Vector representation to be used", choices=['spacy', 'cbow', 'skipgram', 'word2vec', 'doc2vec'], default='spacy')
    optional.add_argument(
        '--vector_path', help="If cbow, fasttext, word2vec or doc2vec is selected, specify the path of the trained embeddings")
    optional.add_argument(
        '--has_id', help="If set, each email contains his id in the end (Sphinx format)", action='store_true')
    optional.add_argument(
        '--save', help="If set, save labels in pickle format", action='store_true')
    optional.add_argument(
        '--output', help="If set, name of the pickle output", default='labels.pickle')

    args = parser.parse_args()
    input = args.input
    centers_path = args.centers
    ids_path = args.ids

    metric = args.metric
    vector_type = args.vector_type
    vector_path = args.vector_path
    has_id = args.has_id
    save = args.save
    output = args.output

    logging.info('Reading the centers of the computed clusters...')
    # Read centers
    with open(centers_path, 'rb') as f:
        centers = pickle.load(f)

    logging.info('Reading input emails...')
    # Read ids
    ids = []
    with open(ids_path, 'r') as r:
        for line in r:
            ids.append(line.strip('\n'))

    # Get emails to classify
    emails = get_emails_from_transcription(input, has_id)
    logging.info('Represent them as vectors...')
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

    logging.info(
        'Compute the cluster of each email based on the given metric...')
    # Compute closest cluster of each email based on given metric.
    labels = {}
    for i, vec in enumerate(vectors):
        cluster = closest_cluster(centers, vec, metric)
        labels[ids[i]] = cluster

    # Save labels in pickle format
    if save:
        with open(output, 'wb') as f:
            pickle.dump(labels, f)
