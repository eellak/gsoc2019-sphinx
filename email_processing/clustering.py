from sklearn.feature_extraction.text import TfidfVectorizer
from helper import get_emails
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os
import numpy as np
from sklearn.cluster import KMeans
import spacy


def get_spacy_vec(emails):
    nlp = spacy.load('el_core_news_md')
    X = []
    for email in emails:
        doc = nlp(email)
        X.append(doc.vector)
    return X


def get_tfidf(emails):
    # Compute tf idf vectorizer of emails.
    tf = TfidfVectorizer()
    # Or fit_transform together
    emails_fitted = tf.fit(emails)
    emails_transformed = emails_fitted.transform(emails)
    return emails_transformed


if __name__ == '__main__':
    # Get emails
    emails = get_emails('./texts/')

    X1 = get_spacy_vec(emails)
    X2 = get_tfidf(emails)

    n_clusters = 3
    clf = KMeans(n_clusters=n_clusters, max_iter=100,
                 init='k-means++', n_init=1)
    labels = clf.fit_predict(X2)
    print(labels)
