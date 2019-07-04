import os
import numpy as np
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from kneed import KneeLocator
import sys
from stop_words import STOP_WORDS
import re


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""

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
    #results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results


def get_emails(dir):
    '''Get emails from a specific directory and return them as a list.

        Args:
            dir: Directory that contains the emails in text files.
        Returns:
            emails: A list that contains the emails in string format.

        '''
    if not os.path.exists(dir):
        sys.exit('Email folder does not exist')

    emails = []
    for email in os.listdir(dir):
        with open(dir + email, 'r') as f:
            emails.append(f.read())
    return emails


def get_sentences(dir):
    '''Get all the sentences of the emails from a specific directory and return them as a list.

        Args:
            dir: Directory that contains the emails in text files.
        Returns:
            emails: A list that contains the sentences of the emails in string format.

        '''
    if not os.path.exists(dir):
        sys.exit('Email folder does not exist')

    emails = []
    for email in os.listdir(dir):
        with open(dir + email, 'r') as f:
            # Each line represents a sentence.
            for line in f:
                emails.append(line)
    return emails


def get_spacy(emails):
    '''Represent emails as vectors using the spacy Greek model.

        Args:
            emails: A list that contains the emails in string format.
        Returns:
            X: A list that contains the vectors of the emails.

        '''
    nlp = spacy.load('el_core_news_md')
    X = []
    for email in emails:
        doc = nlp(email)
        X.append(doc.vector)
    return X


def get_tfidf(emails):
    '''Represent emails as vectors using the tf-idf.

        Args:
            emails: A list that contains the emails in string format.
        Returns:
            X: A list that contains the tf-idf of the emails.

        '''

    # Compute tf idf vectorizer of emails.
    tf = TfidfVectorizer()
    emails_fitted = tf.fit(emails)
    emails_transformed = emails_fitted.transform(emails)
    # Or fit_transform together
    return emails_transformed


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


def cluster2text(out, n_clusters):
    for i in range(n_clusters):
        cluster_path = './' + out + 'cluster_' + str(i)
        email_path = './' + out + 'cluster_' + str(i) + '/data'
        with open(os.path.join(cluster_path, 'corpus'), 'w') as w:
            for email in os.listdir(email_path):
                with open(os.path.join(email_path, email), 'r') as r:
                    w.write(r.read())
                    w.write('\n')


def closest_cluster(centers, point):
    '''Find the cluster that a point belongs.

        Args:
            centers: The coordinates of the centers of the clusters
            point: The coordinates of the point (vector representation of a text)
        Returns:
            min_cluster: Closest cluster to the point.

        '''
    min_distance = np.linalg.norm(centers[0] - point)
    min_cluster = 0
    for i in range(1, len(centers)):
        cur_distance = np.linalg.norm(centers[i] - point)
        if cur_distance < min_distance:
            min_distance = cur_distance
            min_cluster = i
    return min_cluster


def get_emails_from_transcription(file, has_id):
    emails = []
    with open(file, 'r') as f:
        for email in f:
            if has_id:
                # Remove id from each email.
                emails.append(re.sub(r'\([^)]*\)$', '', email))
            else:
                emails.append(email.strip(' '))
    return emails


def closest_point(center, X):
    '''Find the point of X that is closer in center.

        Args:
            center: The coordinates of the center
            point: The coordinates of the points (vector representation of emails)
        Returns:
            min_point: Index of the closest point to the cluster

        '''
    min_distance = np.linalg.norm(center - X[0])
    min_point = 0
    for i in range(1, len(X)):
        cur_distance = np.linalg.norm(center - X[i])
        if cur_distance < min_distance:
            min_distance = cur_distance
            min_point = i
    return min_point
