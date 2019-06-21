import os
import numpy as np
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from kneed import KneeLocator
import sys


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
        with open(os.path.join(cluster_path, 'corpus'), 'w') as w:
            for email in os.listdir(cluster_path):
                with open(os.path.join(cluster_path, email), 'r') as r:
                    w.write(r.read())
                    w.write('\n')
