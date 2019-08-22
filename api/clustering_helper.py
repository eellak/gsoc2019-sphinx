import os
import numpy as np
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
from stop_words import STOP_WORDS
import re
from gensim.models import Word2Vec
from gensim.models.fasttext import FastText
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import scipy
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from numpy import sqrt
from kneed import KneeLocator
from multiprocessing import cpu_count
import logging


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    ''' Get the feature names and tf-idf score of top n items'''

    # use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:

        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    # results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results


def get_spacy(emails, nlp):
    '''Represent emails as vectors using the spacy Greek model.

        Args:
            emails: A list that contains the emails in string format.
        Returns:
            X: A list that contains the vectors of the emails.

        '''
    X = []
    for email in emails:
        doc = nlp(email)
        X.append(doc.vector)
    return X


def cluster2text(out, n_clusters):
    for i in range(n_clusters):
        cluster_path = os.path.join(out, 'cluster_' + str(i))
        email_path = os.path.join(out, 'cluster_' + str(i) + '/data')
        with open(os.path.join(cluster_path, 'corpus'), 'w') as w:
            for email in os.listdir(email_path):
                with open(os.path.join(email_path, email), 'r') as r:
                    w.write(r.read())
                    w.write('\n')


def closest_cluster(centers, point, metric):
    '''Find the cluster that a point belongs.

        Args:
            centers: The coordinates of the centers of the clusters
            point: The coordinates of the point (vector representation of a text)
            metric: Metric to be used (euclidean or cosine)
        Returns:
            cluster: Closest cluster to the point.

        '''
    cluster_id = 0
    if metric == 'euclidean':
        distance = np.linalg.norm(centers[0] - point)
        for i in range(1, len(centers)):
            cur_distance = np.linalg.norm(centers[i] - point)
            if cur_distance < distance:
                distance = cur_distance
                cluster_id = i
    else:
        distance = cosine_similarity([centers[0]], [point])[0][0]
        for i in range(1, len(centers)):
            cur_distance = cosine_similarity(
                [centers[i]], [point])[0][0]
            if cur_distance > distance:
                distance = cur_distance
                cluster_id = i
    return cluster_id


def closest_point(center, X, metric):
    '''Find the point of X that is closer in center.

        Args:
            center: The coordinates of the center
            point: The coordinates of the points (vector representation of emails)
            metric: Metric to be used
        Returns:
            min_point: Index of the closest point to the cluster

        '''
    if metric == 'euclidean':
        distance = np.linalg.norm(center - X[0])
    else:
        distance = cosine_similarity([center], [X[0]])[0][0]
    min_point = 0
    total = len(X)
    for i in range(1, total):
        if metric == 'euclidean':
            cur_distance = np.linalg.norm(center - X[i])
            if cur_distance < distance:
                distance = cur_distance
                min_point = i
        else:
            cur_distance = cosine_similarity([center], [X[i]])[0][0]
            if cur_distance > distance:
                distance = cur_distance
                min_point = i
    return min_point


def get_metrics(X, min_cl, max_cl):
    '''Run k-means and keep sum of squared errors and silhouette coefficients
        for each number of clusters.

        Args:
            X: A list that contains the vectors of the emails.
            min_cl: Minimum number of clusters (at least 2).
            max_cl: Maximum number of clusters (up to n_samples-1)
        Returns:
            sse: A list that contains the sum of squared erros per cluster.
            silhouette: A list that contains the silhouette score per cluster.

        '''

    ks = range(min_cl, max_cl)
    sse = []
    silhouette = []
    for k in ks:
        clf = KMeans(n_clusters=k, n_jobs=cpu_count(),
                     n_init=10 * cpu_count())
        clf = clf.fit(X)
        sse.append(clf.inertia_)
        silhouette.append(silhouette_score(X, clf.labels_))
    return sse, silhouette


def run_kmeans(X, n_clusters):
    '''Run k-means algorithm for given number of clusters.

        Args:
            X: A list that contains the vectors.
            n_clusters: number of clusters
        Returns:
            labels: Label of each vector.

        '''
    # Run k-means usign n_clusters
    clf = KMeans(n_clusters=n_clusters, n_jobs=cpu_count(),
                 n_init=10 * cpu_count())
    labels = clf.fit_predict(X)
    return labels, clf.cluster_centers_


def find_knee(sse, min_cl):
    '''Find optimal number of clusters using the elbow method. More info here: https://github.com/arvkevi/kneed

        Args:
            sse: A list that contains the sum of squared errors.
            min_cl: Minimum number of clusters
        Returns:
            n_clusters: Optimal number of clusters

        '''
    k = range(min_cl, len(sse) + min_cl)
    kneedle = KneeLocator(list(k), sse, curve='convex',
                          direction='decreasing')
    n_clusters = kneedle.knee
    return n_clusters


def cluster2text(out, n_clusters):
    for i in range(n_clusters):
        cluster_path = os.path.join(out, 'cluster_' + str(i))
        email_path = os.path.join(out, 'cluster_' + str(i) + '/data')
        with open(os.path.join(cluster_path, 'corpus'), 'w') as w:
            for email in os.listdir(email_path):
                with open(os.path.join(email_path, email), 'r') as r:
                    w.write(r.read())
                    w.write('\n')


def silhouette_analysis(silhouette, min_cl):
    '''Find optimal number of clusters using the silhouette method.

        Args:
            sse: A list that contains the silhouette scores.
            min_cl: Minimum number of clusters
        Returns:
            n_clusters: Optimal number of clusters

        '''
    n_clusters = silhouette.index(max(silhouette))
    return n_clusters + min_cl


def save_clusters(emails, labels, path):
    # If output directory does not exist, create it.
    out = os.path.join('./data', path)
    if not os.path.exists(out):
        os.makedirs(out)

    total_str = str(len(emails) - 1)
    for i, email in enumerate(emails):
        # Add leading zeros in order to have all names in the right order.
        i_zeroed = str(i).rjust(len(total_str), '0')
        path = './' + out + '/cluster_' + \
            str(labels[i]) + '/data/data_' + i_zeroed
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(email)
