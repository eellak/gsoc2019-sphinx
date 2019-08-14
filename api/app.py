#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import flask
from flask import Flask, redirect, request, url_for, jsonify, session, render_template
from flask_cors import CORS, cross_origin
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
import requests
import json
import email
from preprocess_helper import get_body, get_charset, get_header, mime2str, process_text
from clustering_helper import get_spacy, get_metrics, closest_point, extract_topn_from_vector, sort_coo, silhouette_analysis, find_knee, run_kmeans, save_clusters, cluster2text
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

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
app.config['JSON_AS_ASCII'] = False
CORS(app)
nlp = spacy.load('el_core_news_md')


@app.route("/info", methods=["POST"])
def getInfo():
    data = request.form
    token = data['token']
    cookie = data['cookie']
    info_endpoint = "https://www.googleapis.com/oauth2/v1/userinfo?alt=json"
    headers = {'Authorization': 'Bearer ' +
               token, 'Accept': 'application/json'}

    info_response = requests.get(info_endpoint, headers=headers)
    email = info_response.json()["email"]
    name = info_response.json()["given_name"]
    picture = info_response.json()["picture"]

    returned_data = {'email': email, 'name': name, 'picture': picture}

    database.insert_one(
        'info', {'_id': cookie, 'email': email, 'name': name, 'picture': picture, 'token': token})
    # Send user back to homepage
    return jsonify(returned_data)


@app.route("/emails", methods=["POST"])
def getMessages():
    data = request.form
    cookie = data['cookie']
    res = database.find_one('info', {'_id': cookie})
    token = res['token']
    read_endpoint = "https://www.googleapis.com/gmail/v1/users/userId/messages"
    headers = {'Authorization': 'Bearer ' +
               token, 'Accept': 'application/json'}
    read_response = requests.get(read_endpoint, headers=headers, params={
                                 'userId': 'me', 'labelIds': ['SENT']})
    messages = read_response.json().get("messages")
    clean_messages = []
    for idx, message in enumerate(messages):
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
        # Fill missing headers
        size = len(msg_headers)
        clean_messages.append(
            {'body': body, 'processed_body': proccesed_body, 'sender': (msg_headers[0] if size > 0 else " "), 'subject': (msg_headers[2] if size > 2 else " ")})

    database.insert_one(
        'messages', {'_id': cookie, 'messages': clean_messages})
    # Send user back to homepage
    return jsonify(clean_messages)


@app.route("/clustering", methods=["POST"])
def getClusters():
    data = request.form
    print(data)
    cookie = data['cookie']
    # Get optional arguments
    metric = data['metric']
    n_clusters = data['n_clusters']
    method = data['method']
    min_cl = int(data['min_cl'])
    max_cl = int(data['max_cl'])
    level = data['level']

    res = database.find_one('messages', {'_id': cookie})
    messages_col = res['messages']

    emails = []
    for msg in messages_col:
        if level == "sentence":
            emails.extend(msg['processed_body'])
        else:
            emails.append(" ".join(msg['processed_body']))

    X = get_spacy(emails, nlp)

    if n_clusters == "":
        # Get metrics in different number of clusters (range [min_cl, max_cl]).
        sse, silhouette = get_metrics(X, min_cl, max_cl)
        if method == 'elbow':
            n_clusters = find_knee(sse, min_cl)
        else:
            n_clusters = silhouette_analysis(silhouette, min_cl)
    # Run k-means with given number of clusters.
    labels, centers = run_kmeans(X, n_clusters)
    out = os.path.join('./data', cookie)
    save_clusters(emails, labels, cookie)
    cluster2text(out, n_clusters)
    samples = []
    # Save the closest email in each center.
    for i in range(n_clusters):
        samples.append(emails[closest_point(centers[i], X, metric)])

    # We want to keep some representative words for each cluster
    # in order to identify the topic it represents. So we take
    # the words with the heighest tf-idf metric in each cluster.
    cv = CountVectorizer(stop_words=STOP_WORDS)
    tfidf = TfidfTransformer(smooth_idf=True, use_idf=True)
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

    database.insert_one('clusters', {'_id': cookie, 'centers': centers.tolist(),
                                     'labels': labels.tolist(), 'samples': samples, 'keywords': keywords})

    clusters = [[] for i in range(n_clusters)]
    for idx, email in enumerate(emails):
        clusters[labels[idx]].append(email)

    mix = os.environ.get('general_lm')
    weight = "0.5"
    print(mix)
    for cluster in os.listdir(out):
        cluster_path = os.path.join(out, cluster)
        if os.path.isdir(cluster_path):
            if subprocess.call(['ngram-count -kndiscount -interpolate -text ' + os.path.join(cluster_path, 'corpus') + ' -wbdiscount1 -wbdiscount2 -wbdiscount3 -lm ' + os.path.join(cluster_path, 'model.lm')], shell=True):
                print('Error in subprocess')
            if subprocess.call(['ngram -lm ' + mix + ' -mix-lm ' + os.path.join(cluster_path, 'model.lm') + ' -lambda ' + weight + ' -write-lm ' + os.path.join(cluster_path, 'merged.lm')], shell=True):
                print('Error in subprocess')

    return jsonify({'samples': samples, 'keywords': keywords, 'clusters': clusters})


if __name__ == "__main__":
    app.run()
