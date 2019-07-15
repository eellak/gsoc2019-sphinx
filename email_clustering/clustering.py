import os
from kmeans import get_metrics, run_kmeans, save_clusters
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from helper import get_emails, get_spacy, get_tfidf, find_knee, silhouette_analysis, cluster2text, closest_cluster, closest_point
from helper import sort_coo, extract_topn_from_vector, get_sentences
import argparse
import sys
import pickle
from stop_words import STOP_WORDS
from helper import get_trained_vec

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
        '--vector_type', help="Vector representation to be used", choices=['spacy', 'tf-idf', 'cbow', 'skipgram', 'word2vec'], default='spacy')

    optional.add_argument(
        '--n_clusters', help="Number of clusters to be used (if not set, automatically choose one)", type=int, default=-1)

    optional.add_argument(
        '--plot', help="Plot sum of squared errors and silhouette scores (only if n_clusters is not defined)", action='store_true')

    optional.add_argument(
        '--method', help="Method for choosing optimal number of clusters", choices=['elbow', 'silhouette'], default='silhouette')

    optional.add_argument(
        '--min_cl', help="Minimum number of clusters (only if n_clusters is not defined)", type=int, default=2)

    optional.add_argument(
        '--max_cl', help="Maximum number of clusters (only if n_clusters is not defined)", type=int)

    optional.add_argument(
        '--samples', help="If set, a file that contains a representative email for each cluster is saved", action='store_true')

    optional.add_argument(
        '--keywords', help="If set, get some keywords for each cluster", action='store_true')

    optional.add_argument(
        '--sentence', help="If set, clustering is done using the sentences of the emails instead of the entire emails", action='store_true')

    optional.add_argument(
        '--vector_path', help="If cbow, fasttext or word2vec is selected, give the path of the trained embeddings")

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
    keywords = args.keywords
    sentence = args.sentence
    vector_path = args.vector_path

    if not input.endswith('/'):
        input = input + '/'
    if not output.endswith('/'):
        output = output + '/'

    if sentence:
        # Get sentences of emails
        emails = get_sentences(input)
    else:
        # Get emails
        emails = get_emails(input)

    # Max number of clusters is always n_samples/2 if not specified
    if max_cl is None:
        max_cl = len(emails) // 2
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
    elif vector_type == 'tf-idf':
        X = get_tfidf(emails)
    elif vector_type == 'cbow':
        X = get_trained_vec(emails, vector_path, 'cbow')
    elif vector_type == 'skipgram':
        X = get_trained_vec(emails, vector_path, 'skipgram')
    else:
        X = get_trained_vec(emails, vector_path, 'word2vec')

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
        # Save the closest email in each center.
        with open(os.path.join(output + 'samples'), 'w') as w:
            for i in range(n_clusters):
                w.write('Cluster ' + str(i) + '\n')
                w.write(emails[closest_point(centers[i], X)])
                w.write('\n')

    if keywords:
        # We want to keep some representative words for each cluster
        # in order to identify the topic it represents. So we take
        # the words with the heighest tf-idf metric in each cluster.
        cv = CountVectorizer(stop_words=STOP_WORDS)
        tfidf = TfidfTransformer(smooth_idf=True, use_idf=True)
        for i in range(n_clusters):
            emails_cluster = [emails[j]
                              for j in range(len(emails)) if labels[j] == i]
            word_count_vector = cv.fit_transform(emails_cluster)
            tfidf.fit(word_count_vector)
            feature_names = cv.get_feature_names()
            tf_idf_vector = tfidf.transform(
                cv.transform(emails_cluster))
            sorted_items = sort_coo(tf_idf_vector.tocoo())
            keywords = extract_topn_from_vector(
                feature_names, sorted_items, 10)
            print(keywords)
