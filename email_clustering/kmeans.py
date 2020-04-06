import os
import logging
import numpy as np
import matplotlib.pyplot as plt

from numpy import sqrt
from kneed import KneeLocator
from multiprocessing import cpu_count
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score, silhouette_samples
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


def get_metrics(X, plot, min_cl, max_cl):
    '''Run k-means and keep sum of squared errors and silhouette coefficients
        for each number of clusters.

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
        clf = KMeans(n_clusters=k, n_jobs=cpu_count(),
                     n_init=10 * cpu_count())
        logging.info(clf)
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
        plt.title('Silhouette Method for Optimal k')
        plt.show()

    return sse, silhouette


def run_dendrogram(X, n_clusters):
    '''Run divisive clustering algorithm for given number of clusters.

        Args:
            X: A list that contains the vectors.
            n_clusters: number of clusters
        Returns:
            labels: Label of each vector.

        '''
    Z = linkage(X, 'ward')
    labels = fcluster(Z, n_clusters, criterion='maxclust')
    for i in range(len(labels)):
        labels[i] -= 1
    centers = np.zeros((n_clusters, len(X[0])))
    for i in range(n_clusters):
        centers[i] = np.average([X[j]
                                 for j in range(len(labels)) if labels[j] == i])

    return labels, centers


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


def run_agglomerative(X, n_clusters):
    '''Run agglomerative hierarchical algorithm for given number of clusters.

        Args:
            X: A list that contains the vectors.
            n_clusters: number of clusters
        Returns:
            labels: Label of each vector.

        '''
    clf = AgglomerativeClustering(
        n_clusters=n_clusters,  affinity='euclidean', linkage='complete')
    labels = clf.fit_predict(X)
    centers = np.zeros((n_clusters, len(X[0])))
    for i in range(n_clusters):
        centers[i] = np.average([X[j]
                                 for j in range(len(labels)) if labels[j] == i])

    return labels, centers


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

    total_str = str(len(emails) - 1)
    for i, email in enumerate(emails):
        # Add leading zeros in order to have all names in the right order.
        i_zeroed = str(i).rjust(len(total_str), '0')
        path = './' + out + 'cluster_' + \
            str(labels[i]) + '/data/data_' + i_zeroed
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(email)
