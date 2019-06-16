from sklearn.feature_extraction.text import TfidfVectorizer
from helper import get_emails
from kmeans import get_optimal_clusters, run_kmeans, save_clusters
import os
import numpy as np
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


if __name__ == '__main__':
    # Get emails
    emails = get_emails('./texts/')

    # Get vector representation of emails.
    X_spacy = get_spacy(emails)
    # X_tfidf = get_tfidf(emails)

    # Find the optimal number of clusters
    # get_optimal_clusters(X_spacy)

    # Run k-means with the optimal number of clusters
    labels = run_kmeans(X_spacy, 3)

    # Save clusters in separate folders.
    save_clusters(emails, labels)
