import os
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt


def get_optimal_clusters(X):
    '''Run k-means and search for the omptimal number of clusters
        by using the Elbow Criterion and silhouette metric.

        Args:
            X: A list that contains the vectors of the emails.
        '''

    sse = []
    silhouette = []
    for k in range(2, len(X)):
        clf = KMeans(n_clusters=k)
        clf = clf.fit(X)
        sse.append(clf.inertia_)
        silhouette.append(silhouette_score(X, clf.labels_))

    # Plot sum of Sum_of_squared_errors,
    plt.plot(range(2, len(X)), sse, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_error')
    plt.title('Elbow Method For Optimal k')
    plt.show()

    # Plot silhouette scores.
    plt.plot(range(2, len(X)), silhouette, 'bx-')
    plt.xlabel('k')
    plt.ylabel('silhouette score')
    plt.show()


def run_kmeans(X, n_clusters):
    '''Run k-means algorithm for given number of clusters.

        Args:
            X: A list that contains the vectors.
            n_clusters: number of clusters
        Returns:
            labels: Label of each vector.

        '''
    # Run k-means with the optimal number of clusters
    best_clf = KMeans(n_clusters=n_clusters)
    labels = best_clf.fit_predict(X)
    return labels


def save_clusters(emails, labels):
    '''Saves data according to the computed clusters.

        Args:
            emails: A list that contains the emails in string format.
            labels: A list that contains the label of each email.

        '''
    for i, email in enumerate(emails):
        path = './cluster_' + str(labels[i]) + '/email_' + str(i)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(email)
