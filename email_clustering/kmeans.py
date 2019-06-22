import os
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
import matplotlib.pyplot as plt
from numpy import sqrt


def get_metrics(X, plot, min_cl, max_cl):
    '''Run k-means and keep sum of squared errors and silhouette coefficients
        for each number of clusters (2 to n_samples-1).

        Args:
            X: A list that contains the vectors of the emails.
            plot: If True plot the metrics.
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
        clf = KMeans(n_clusters=k)
        clf = clf.fit(X)
        sse.append(clf.inertia_)
        silhouette.append(silhouette_score(X, clf.labels_))

    if plot:
        # Plot sum of Sum_of_squared_errors,
        plt.plot(ks, sse, 'bx-')
        plt.xlabel('k')
        plt.ylabel('Sum of squared error')
        plt.title('Elbow Method For Optimal k')
        plt.show()

        # Plot silhouette scores.
        plt.plot(ks, silhouette, 'bx-')
        plt.xlabel('k')
        plt.ylabel('Silhouette score')
        plt.show()

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
    clf = KMeans(n_clusters=n_clusters)
    labels = clf.fit_predict(X)
    return labels, clf.cluster_centers_


def save_clusters(emails, labels, out):
    '''Saves data according to the computed clusters.

        Args:
            emails: A list that contains the emails in string format.
            labels: A list that contains the label of each email.
            out: Output directory

        '''
    # If output directory does not exist, create it.
    if not os.path.exists(out):
        os.makedirs(out)

    for i, email in enumerate(emails):
        path = './' + out + 'cluster_' + str(labels[i]) + '/email_' + str(i)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(email)
