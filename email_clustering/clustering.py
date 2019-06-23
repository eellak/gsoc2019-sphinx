import os
from kmeans import get_metrics, run_kmeans, save_clusters
from helper import get_emails, get_spacy, get_tfidf, find_knee, silhouette_analysis, cluster2text, closest_cluster, closest_point
import argparse
import sys
import pickle

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool for clustering email
    ''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--input', help="Input directory", required=True)
    required.add_argument(
        '--output', help="Ouput directory", required=True)

    optional.add_argument(
        '--vector_type', help="Vector representation to be used", choices=['spacy', 'tf-idf'], default='spacy')

    optional.add_argument(
        '--n_clusters', help="Number of clusters to be used (if not set, automatically choose one)", type=int, default=-1)

    optional.add_argument(
        '--plot', help="Plot sum of squared errors and silhouette scores (only if n_clusters is not defined)", type=bool, default=False)

    optional.add_argument(
        '--method', help="Method for choosing optimal number of clusters", choices=['elbow', 'silhouette'], default='silhouette')

    optional.add_argument(
        '--min_cl', help="Minimum number of clusters (only if n_clusters is not defined)", type=int, default=2)

    optional.add_argument(
        '--max_cl', help="Maximum number of clusters (only if n_clusters is not defined)", type=int)

    optional.add_argument(
        '--samples', help="If set, a file that contains a representative email for each cluster is saved", action='store_true')

    args = parser.parse_args()
    input = args.input
    output = args.output
    vector_type = args.vector_type
    plot = args.plot
    n_clusters = args.n_clusters
    method = args.method
    min_cl = args.min_cl
    max_cl = args.max_cl
    samples = args.samples

    if not input.endswith('/'):
        input = input + '/'
    if not output.endswith('/'):
        output = output + '/'
    # Get emails
    emails = get_emails(input)

    # Max number of clusters is always n_samples-1 if not specified
    if max_cl is None:
        max_cl = len(emails) - 1
    # Min number of clusters is greater than 1.
    if min_cl < 2:
        sys.exit('Minimum number of clusters should be greater than 1.')
    if max_cl > len(emails) - 1:
        sys.exit(
            'Maximum number of clusters should be less than n_samples.')
    if min_cl > max_cl:
        sys.exit('Minumum number of clusters should be less than maximum')
    # Get vector representation of emails.
    if vector_type == 'spacy':
        X = get_spacy(emails)
    else:
        X = get_tfidf(emails)

    if n_clusters == -1:
        # Get metrics in different number of clusters (range [min_cl, max_cl]).
        sse, silhouette = get_metrics(X, plot, min_cl, max_cl)
        if method == 'elbow':
            n_clusters = find_knee(sse, min_cl)
        else:
            n_clusters = silhouette_analysis(silhouette, min_cl)
    # Run k-means with given number of clusters.
    labels, centers = run_kmeans(X, n_clusters)

    # Save clusters in given folders.
    save_clusters(emails, labels, output)

    # Save in each cluster a file that contains all the emails of it.
    # It will be used in the language model.
    cluster2text(output, n_clusters)

    # Save centers in a pickle, in order to classify
    # other emails.
    with open(output + 'centers.pickle', 'wb') as f:
        pickle.dump(centers, f)

    if samples:
        with open(os.path.join(output + 'samples'), 'w') as w:
            for i in range(n_clusters):
                w.write('Cluster ' + str(i) + '\n')
                w.write(emails[closest_point(centers[i], X)])
                w.write('\n')
