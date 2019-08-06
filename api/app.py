#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from flask import Flask, redirect, request, url_for, jsonify, session
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
from oauthlib.oauth2 import WebApplicationClient
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

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)
db.init()


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile",
               'https://www.googleapis.com/auth/gmail.readonly']
    )
    return jsonify(request_uri)


clean_messages = []


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    # Create a user in your db with the information provided
    # by Google
    return redirect('http://localhost:4200/')


@app.route("/messages")
def readMessages():
    read_endpoint = "https://www.googleapis.com/gmail/v1/users/userId/messages"
    uri, headers, body = client.add_token(read_endpoint)
    read_response = requests.get(
        uri, headers=headers, data=body, params={'userId': 'me', 'labelIds': ['SENT']})
    messages = read_response.json().get("messages")
    for idx, message in enumerate(messages):
        # Get message based in the id.
        get_endpoint = "https://www.googleapis.com/gmail/v1/users/userId/messages/id"
        uri, headers, body = client.add_token(get_endpoint)
        get_response = requests.get(uri, headers=headers, data=body, params={
            'userId': 'me', 'id': message['id'], 'format': 'raw'})
        raw_msg = get_response.json().get("raw")
        string_message = str(
            base64.urlsafe_b64decode(raw_msg), "ISO-8859-7")
        # Convert current message to mime format.
        mime_msg = email.message_from_string(string_message)
        # Convert current message from mime to string.
        body, header = mime2str(mime_msg)
        clean_messages.append(body)
    # Send user back to homepage
    return jsonify(clean_messages)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("/login"))


if __name__ == "__main__":
    app.run()
