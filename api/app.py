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
from user import User
import requests
import json
import email
from helper import get_body, get_charset, get_header, mime2str
from email.header import decode_header
from email.iterators import typed_subpart_iterator
import chardet
from bs4 import BeautifulSoup
import base64
from flask_cors import CORS
from database import db
import string
import random
import urllib


# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
app.config['JSON_AS_ASCII'] = False
CORS(app)


@app.route("/info", methods=["POST"])
def getInfo():
    data = request.form
    token = data['token']
    info_endpoint = "https://www.googleapis.com/oauth2/v1/userinfo?alt=json"
    headers = {'Authorization': 'Bearer ' +
               token, 'Accept': 'application/json'}

    info_response = requests.get(info_endpoint, headers=headers)
    email = info_response.json()["email"]
    name = info_response.json()["given_name"]
    picture = info_response.json()["picture"]
    returned_data = {'email': email, 'name': name, 'picture': picture}
    # Send user back to homepage
    return returned_data


@app.route("/messages", methods=["POST"])
def getMessages():
    data = request.form
    token = data['token']
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
        body, header = mime2str(mime_msg)

        clean_messages.append(
            {'body': body, 'sender': header[0], 'subject': header[2]})
        print(idx)
    # Send user back to homepage
    return jsonify(clean_messages)


if __name__ == "__main__":
    app.run()
