from sklearn.feature_extraction.text import TfidfVectorizer
from helper import get_emails
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import spacy


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


def get_optimal_clusters(X):
    '''Run k-means and search for the omptimal
        number of clusters by using the Elbow Criterion.

        Args:
            X: A list that contains the vectors of the emails.
        '''

    sse = []
    for k in range(1, len(X)):
        clf = KMeans(n_clusters=k)
        clf = clf.fit(X)
        sse.append(clf.inertia_)

    plt.plot(range(1, len(X)), sse, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_error')
    plt.title('Elbow Method For Optimal k')
    plt.show()


if __name__ == '__main__':
    # Get emails
    emails = get_emails('./texts/')

    # Get representation of emails.
    X_spacy = get_spacy(emails)
    # X_tfidf = get_tfidf(emails)

    # Find the optimal number of clusters
    get_optimal_clusters(X_spacy)
