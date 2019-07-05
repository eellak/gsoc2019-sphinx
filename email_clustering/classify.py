import os
import argparse
from helper import closest_cluster, get_spacy, get_emails_from_transcription
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
        '--n_clusters', help="Number of clusters", required=True, type=int)
    optional.add_argument(
        '--has_id', help="If set, each email contains his id in the end", action='store_true')
    optional.add_argument(
        '--save', help="If set, save labels in pickle format", action='store_true')

    args = parser.parse_args()
    input = args.input
    centers_path = args.centers
    ids_path = args.ids
    n_clusters = args.n_clusters
    has_id = args.has_id
    save = args.save

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
    vectors = get_spacy(emails)

    labels = {k: [] for k in range(n_clusters)}
    for i, vec in enumerate(vectors):
        cluster = closest_cluster(centers, vec)
        labels[cluster].append(ids[i])

    # Save labels in pickle format
    if save:
        with open('labels.pickle', 'wb') as f:
            pickle.dump(labels, f)
