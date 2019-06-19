import os
from kmeans import get_metrics, run_kmeans, save_clusters
from helper import get_emails, get_spacy, get_tfidf
import argparse

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool for clustering email
    ''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('--input', help="Input directory", required=True)
    required.add_argument('--output', help="Ouput directory", required=True)

    optional.add_argument(
        '--vector_type', help="Vector representation to be used", choices=['spacy', 'tf-idf'], default='spacy')

    optional.add_argument(
        '--n_clusters', help="Number of clusters to be used (if not set, automatically choose one)", type=int, default=-1)

    optional.add_argument(
        '--plot', help="Plot sum of squared errors and silhouette scores (only if n_clusters is not defined)", type=bool, default=False)

    args = parser.parse_args()
    input = args.input
    output = args.output
    vector_type = args.vector_type
    plot = args.plot
    n_clusters = args.n_clusters

    if not input.endswith('/'):
        input = input + '/'
    if not output.endswith('/'):
        output = output + '/'
    # Get emails
    emails = get_emails(input)

    # Get vector representation of emails.
    if vector_type == 'spacy':
        X = get_spacy(emails)
    else:
        X = get_tfidf(emails)

    if n_clusters == -1:
        # Find the optimal number of clusters

    else:
        # Run k-means with given number of clusters.
        labels = run_kmeans(X, n_clusters)

    # Save clusters in separate folders.
    save_clusters(emails, labels, output)
