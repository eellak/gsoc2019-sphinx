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
from clustering_helper import get_spacy, get_metrics, closest_point, extract_topn_from_vector, sort_coo
from email.header import decode_header
from email.iterators import typed_subpart_iterator
import chardet
from bs4 import BeautifulSoup
import base64
from flask_cors import CORS
import database

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
app.config['JSON_AS_ASCII'] = False
CORS(app)


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
        # Get message based in the id.
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
        proccesed_body = "\n".join(process_text(body))
        print(idx)
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
    cookie = data['cookie']
    # Get optional arguments
    metric = data['metric']
    n_clusters = data['n_clusters']
    method = data['method']
    min_cl = data['min_cl']
    max_cl = data['max_cl']
    sentence = data['sentence']

    res = database.find_one('messages', {'_id': cookie})
    messages_col = res['messages']
    emails = []
    for msg in messages_col:
        emails.append(msg['proccesed_body'])

    X = get_spacy(emails)
    if n_clusters is None:
        # Get metrics in different number of clusters (range [min_cl, max_cl]).
        sse, silhouette = get_metrics(X, min_cl, max_cl)
        if method == 'elbow':
            n_clusters = find_knee(sse, min_cl)
        else:
            n_clusters = silhouette_analysis(silhouette, min_cl)
    # Run k-means with given number of clusters.
    labels, centers = run_kmeans(X, n_clusters)

    # TODO: save clusters in db
    # TODO: save centers in db

    # TODO: save samples in db
    # TODO: save keywords in db

    if samples:
        # Save the closest email in each center.
        with open(os.path.join(output + 'samples'), 'w') as w:
            for i in range(n_clusters):
                w.write('Cluster ' + str(i) + '\n')
                w.write(emails[closest_point(centers[i], X, metric)])
                w.write('\n')

    if keywords:
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
    return '1'


if __name__ == "__main__":
    app.run()
