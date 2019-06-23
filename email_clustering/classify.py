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

    args = parser.parse_args()
    input = args.input
    centers_path = args.centers

    # Read centers
    with open(centers_path, 'rb') as f:
        centers = pickle.load(f)

    # Get emails to classify
    emails = get_emails_from_transcription(input)
    # Represent them as vectors
    vectors = get_spacy(emails)
    for vec in vectors:
        cluster = closest_cluster(centers, vec)
        print(cluster)
