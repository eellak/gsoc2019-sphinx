from sklearn.feature_extraction.text import TfidfVectorizer
from helper import get_emails
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os
import numpy as np
from sklearn.cluster import KMeans


if __name__ == '__main__':
    # Get emails
    emails = get_emails('./texts/')

    # Compute tf idf vectorizer of emails.
    tf = TfidfVectorizer()
    # Or fit_transform together
    emails_fitted = tf.fit(emails)
    emails_transformed = emails_fitted.transform(emails)
    idf = tf.idf_
    feature_names = np.array(tf.get_feature_names())
    sorted_by_idf = np.argsort(tf.idf_)
    print("Features with lowest idf:\n{}".format(
        feature_names[sorted_by_idf[:3]]))
    print("\nFeatures with highest idf:\n{}".format(
        feature_names[sorted_by_idf[-3:]]))
