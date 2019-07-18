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
        with open(os.path.join(dir, email), 'r') as f:
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
        with open(os.path.join(dir, email), 'r') as f:
            # Each line represents a sentence.
            for line in f:
                emails.append(line.strip('\n'))
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
    '''Represent emails as vectors using the tf-idf vectorizer.

        Args:
            emails: A list that contains the emails in string format.
        Returns:
            X: A list that contains the tf-idf of the emails.

        '''

    # Compute tf idf vectorizer of emails.
    tf = TfidfVectorizer()
    emails_fitted = tf.fit(emails)
    emails_transformed = emails_fitted.transform(emails)
    return emails_transformed


def get_trained_vec(emails, path, name):
    '''Represent emails as vectors using a trained word vector model (word2vec, cbow or skipgram).

        Args:
            emails: A list that contains the emails in string format.
        Returns:
            X: A list that contains the vector of each email.

        '''
    # Load corresponding model.
    if name == 'word2vec':
        model = Word2Vec.load(path)
    else:
        model = FastText.load(path)
    X = []
    # Represent a sentence as the mean value of its word vectors.
    for email in emails:
        X.append(np.mean([model.wv[tok]
                          for tok in email.strip('\n').split(' ') if tok in model.wv], axis=0))
    return X


def get_trained_doc(emails, path):
    '''Represent emails as vectors using a trained doc2vec model.

        Args:
            emails: A list that contains the emails in string format.
        Returns:
            X: A list that contains the vector of each email.

        '''
    model = Doc2Vec.load(path)
    X = []
    for email in emails:
        test_data = word_tokenize(email.lower())
        X.append(model.infer_vector(test_data))
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
    cluster = 0
    if metric == 'euclidean':
        min_distance = np.linalg.norm(centers[0] - point)
        for i in range(1, len(centers)):
            cur_distance = np.linalg.norm(centers[i] - point)
            if cur_distance < min_distance:
                min_distance = cur_distance
                cluster = i
    else:
        min_distance = cosine_similarity([centers[0]], [point])[0][0]
        for i in range(1, len(centers)):
            cur_distance = cosine_similarity(
                [centers[i]], [point])[0][0]
            if cur_distance > min_distance:
                min_distance = cur_distance
                cluster = i
    return cluster


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
        min_distance = np.linalg.norm(center - X[0])
    else:
        min_distance = cosine_similarity([center], [X[0]])
    min_point = 0
    # If X contains tfidf values, it is not a normal list.
    if scipy.sparse.issparse(X):
        total = X.shape[0]
    else:
        total = len(X)
    for i in range(1, total):
        if metric == 'euclidean':
            cur_distance = np.linalg.norm(center - X[i])
        else:
            cur_distance = cosine_similarity([center], [X[i]])
        if cur_distance < min_distance:
            min_distance = cur_distance
            min_point = i
    return min_point
