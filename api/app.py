#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import flask
from flask import Flask, redirect, request, url_for, jsonify, session, render_template
from flask_cors import CORS, cross_origin
import requests
import json
import email
from preprocess_helper import get_body, get_charset, get_header, mime2str, process_text
from clustering_helper import get_spacy, get_metrics, closest_point, extract_topn_from_vector, sort_coo, silhouette_analysis, find_knee, run_kmeans, save_clusters, cluster2text, closest_cluster
from stop_words import STOP_WORDS
from email.header import decode_header
from email.iterators import typed_subpart_iterator
import chardet
from bs4 import BeautifulSoup
import base64
from flask_cors import CORS
import database
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import subprocess
import base64
import urllib
import numpy as np
from dictation_helper import get_text_sphinx4, get_text_pocketsphinx
from py4j.java_gateway import JavaGateway

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
app.config['JSON_AS_ASCII'] = False
# Enable CORS
CORS(app)
# Load spacy Greek model
nlp = spacy.load('el_core_news_md')
# Connect to a JVM with a gateway in order to communicate with Java cmuSphinx
gateway = JavaGateway()
# Get useful paths for defaul models.
acousticPath = os.environ.get("general_ac")
dictPath = os.environ.get("general_dict")
lmPath = os.environ.get("general_lm")


@app.route("/info", methods=["POST"])
def getInfo():
    '''Endpoint that returns the email, the username and profile picture of a Gmail user.

        Args:
            token: Authentication token from Gmail api.
            cookie: Cookie of current user.
        '''
    data = request.form
    print(data)
    token = data['token']
    cookie = data['cookie']
    # Send get request to gmail api.
    info_endpoint = "https://www.googleapis.com/oauth2/v1/userinfo?alt=json"
    headers = {'Authorization': 'Bearer ' +
               token, 'Accept': 'application/json'}
    info_response = requests.get(info_endpoint, headers=headers)

    email = info_response.json()["email"]
    name = info_response.json()["given_name"]
    picture = info_response.json()["picture"]
    print(cookie)
    returned_data = {'email': email, 'name': name, 'picture': picture}

    # Save user information in database.
    database.insert_one(
        'info', {'_id': cookie, 'email': email, 'name': name, 'picture': picture, 'token': token})
    # Send user back to homepage
    return jsonify(returned_data)


@app.route("/emails", methods=["POST"])
def getEmails():
    '''Endpoint that returns the sent emails of a Gmail user.

        Args:
            cookie: Cookie of current user.
        '''
    data = request.form

    cookie = data['cookie']
    print(cookie)
    # Get authentication token of current user.
    token = data['token']
    # Send get request in gmail api.
    read_endpoint = "https://www.googleapis.com/gmail/v1/users/userId/messages"
    headers = {'Authorization': 'Bearer ' +
               token, 'Accept': 'application/json'}
    read_response = requests.get(read_endpoint, headers=headers, params={
                                 'userId': 'me', 'labelIds': ['SENT']})
    messages = read_response.json().get("messages")
    clean_messages = []
    for idx, message in enumerate(messages):
        print(idx)
        # Get message based in the id.0.5311486608012452
        get_endpoint = "https://www.googleapis.com/gmail/v1/users/userId/messages/id"
        get_response = requests.get(get_endpoint, headers=headers, params={
            'userId': 'me', 'id': message['id'], 'format': 'raw'})
        raw_msg = get_response.json().get("raw")
        string_message = str(
            base64.urlsafe_b64decode(raw_msg), "ISO-8859-7")
        # Convert current message to mime format.
        mime_msg = email.message_from_string(string_message)
        # Convert current message from mime to string.
        body, msg_headers = mime2str(mime_msg)
        proccesed_body = process_text(body)
        size = len(msg_headers)
        clean_messages.append(
            {'body': body, 'processed_body': proccesed_body, 'sender': (msg_headers[0] if size > 0 else " "), 'subject': (msg_headers[2] if size > 2 else " ")})

    # Save user emails in database.
    database.insert_one(
        'messages', {'_id': cookie, 'messages': clean_messages})
    return jsonify(clean_messages)


@app.route("/clustering", methods=["POST"])
def getClusters():
    '''Endpoint that clusters the emails.

        Args:
            cookie: Cookie of current user.
            metric: Metric to be used for closest point calculation.
            n_clusters: Number of clusters.
            method: Method of selecting number of clusters to be used (knee, silhouette).
            min_cl: Min number of clusters.
            max_cl: Max number of clusters.
            level: Level of clustering (per sentence or per email).
        '''
    data = request.form
    cookie = data['cookie']
    metric = data['metric']
    n_clusters = data['n_clusters']
    method = data['method']
    min_cl = int(data['min_cl'])
    max_cl = int(data['max_cl'])
    level = data['level']

    # Get messages current user
    res = database.find_one('messages', {'_id': cookie})
    messages_col = res['messages']
    emails = []
    for msg in messages_col:
        if level == "sentence":
            emails.extend(msg['processed_body'])
        else:
            emails.append(" ".join(msg['processed_body']))
    # Represent them as vectors.
    X = get_spacy(emails, nlp)

    if n_clusters == "":
        # Get metrics in different number of clusters (range [min_cl, max_cl]).
        sse, silhouette = get_metrics(X, min_cl, max_cl)
        if method == 'elbow':
            n_clusters = find_knee(sse, min_cl)
        else:
            n_clusters = silhouette_analysis(silhouette, min_cl)
    # Run k-means with given number of clusters.
    n_clusters = int(n_clusters)
    labels, centers = run_kmeans(X, n_clusters)

    # Save computed clusters in filesystem.
    save_clusters(emails, labels, cookie)
    out = os.path.join('./data', cookie)
    cluster2text(out, n_clusters)

    # Get a sample from each cluster.
    samples = []
    # Save the closest email in each center.
    for i in range(n_clusters):
        samples.append(emails[closest_point(centers[i], X, metric)])

    # We want to keep some representative words for each cluster
    # in order to identify the topic it represents. So we take
    # the words with the heighest tf-idf metric in each cluster.
    cv = CountVectorizer(stop_words=STOP_WORDS)
    tfidf = TfidfTransformer(smooth_idf=True, use_idf=True)
    keywords_total = []
    for i in range(n_clusters):
        emails_cluster = [emails[j]
                          for j in range(len(emails)) if labels[j] == i]
        word_count_vector = cv.fit_transform(emails_cluster)
        tfidf.fit(word_count_vector)
        feature_names = cv.get_feature_names()
        tf_idf_vector = tfidf.transform(
            cv.transform(emails_cluster))
        sorted_items = sort_coo(tf_idf_vector.tocoo())
        keywords = extract_topn_from_vector(
            feature_names, sorted_items, 5)
        keywords_total.append(keywords)

    # Insert in database.
    database.insert_one('clusters', {'_id': cookie, 'centers': centers.tolist(),
                                     'labels': labels.tolist(), 'samples': samples, 'keywords': keywords_total, 'metric': metric})

    clusters = [[] for i in range(n_clusters)]
    for idx, email in enumerate(emails):
        clusters[labels[idx]].append(email)

    weight = "0.5"
    # Create language models using srilm.
    for cluster in os.listdir(out):
        cluster_path = os.path.join(out, cluster)
        if os.path.isdir(cluster_path):
            if subprocess.call(['ngram-count -kndiscount -interpolate -text ' + os.path.join(cluster_path, 'corpus') + ' -wbdiscount1 -wbdiscount2 -wbdiscount3 -lm ' + os.path.join(cluster_path, 'model.lm')], shell=True):
                print('Error in subprocess')
            if subprocess.call(['ngram -lm ' + lmPath + ' -mix-lm ' + os.path.join(cluster_path, 'model.lm') + ' -lambda ' + weight + ' -write-lm ' + os.path.join(cluster_path, 'merged.lm')], shell=True):
                print('Error in subprocess')

    return jsonify({'samples': samples, 'keywords': keywords_total, 'clusters': clusters})


@app.route("/dictation", methods=["POST"])
def getDictation():
    '''Endpoint that decodes speech to text.

        Args:
            cookie: Cookie of current user.
            method: Use language adaptation or not.
            package: Sphinx4 or pocketsphinx
            url: Sound file.

        '''
    cookie = request.form['cookie']
    method = request.form['method']
    package = request.form['package']
    url = request.files['url']

    out = os.path.join('./data', cookie)
    # Save current dictation in filesystem.
    url.save(os.path.join(out, 'curr_dictation.wav'))

    if package == "pocketsphinx":
        decoded_gen = get_text_pocketsphinx(
            out, lmPath, acousticPath, dictPath)
    else:
        py4j_relpath = os.path.join("../api/data", cookie)
        decoded_gen = get_text_sphinx4(
            py4j_relpath, acousticPath, dictPath, lmPath, gateway)

    returned_data = {'text_gen': decoded_gen,
                     'text_adapt': "", 'cluster': ""}
    if method == "adapted":
        # Find cluster
        res = database.find_one('clusters', {'_id': cookie})
        centers = res['centers']
        metric = res['metric']
        doc = nlp(decoded_gen)
        decoded_gen_spacy = doc.vector
        cluster = closest_cluster(np.array(centers), decoded_gen_spacy, metric)
        if package == "pocketsphinx":
            clusterPath = os.path.join(out, 'cluster_' + str(cluster))
            lmAdaptPath = os.path.join(clusterPath, 'merged.lm')
            decoded_adapt = get_text_pocketsphinx(
                out, lmAdaptPath, acousticPath, dictPath)
        else:
            clusterRelPath = os.path.join(
                py4j_relpath, 'cluster_' + str(cluster))
            lmAdaptPath = os.path.join(clusterRelPath, 'merged.lm')
            decoded_adapt = get_text_sphinx4(
                py4j_relpath, acousticPath, dictPath, lmAdaptPath, gateway)
        returned_data = {'text_gen': decoded_gen,
                         'text_adapt': decoded_adapt, 'cluster': cluster}

    return jsonify(returned_data)


@app.route("/saveDictation", methods=["POST"])
def saveDictation():
    '''Endpoint that saves a sound file for later acoustic adaptation.

        Args:
            cookie: Cookie of current user.
            url: Sound file.

        '''
    cookie = request.form['cookie']
    text = request.form['text']
    print(text)
    url = request.files['url']

    out = os.path.join('./data', cookie)

    res = database.find_one('savedDictations', {'_id': cookie})
    if res is None:
        print('1')
        counter = 0
        database.insert_one(
            'savedDictations', {'_id': cookie, 'num': counter})
    else:
        print('2')
        counter = res['num'] + 1
        database.update_one('savedDictations', {'_id': cookie}, {
                            "$set": {'num': counter}})

    # Save current dictation in filesystem.
    url.save(os.path.join(out, str(counter) + '.wav'))

    return '1'


if __name__ == "__main__":
    app.run()
