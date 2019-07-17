from __future__ import print_function
from helper import process_text, save_messages
import urllib
import base64
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import email
from email.header import decode_header
from email.iterators import typed_subpart_iterator
import chardet
from bs4 import BeautifulSoup
import argparse

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def connect(reload):
    '''Open the default browser and ask the user for authentication reading his emails.

        Args:
            reload: If true, ignore any token already available.
        Returns:
            service: A recourse object. All calls will be done through this object.

        '''
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if not reload and os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)

    return service


def read_emails(service, limit=100, save_raw=False):
    '''Read the user's sent emails.

        Args:
            service: A recourse object, that helps us make requests.
            limit: Total number of messages to read.
            save_raw: If true, raw message files will be saved too.
        Returns:
            body_messages: A list that contains the body of each message.
            header_messages = A list that contains the headers of each message.

        '''
    # Call the Gmail API and get all sent emails.
    results = service.users().messages().list(
        userId='me', maxResults=limit, labelIds=['SENT']).execute()
    # Get user's messages based on given limit.
    messages = results.get('messages', [])
    body_messages = []
    header_messages = []
    for idx, message in enumerate(messages):
        # Get message based in the id.
        msg_dict = service.users().messages().get(
            userId='me', id=message['id'], format='raw').execute()
        raw_msg = msg_dict['raw']
        # Convert message encoding from base64 to iso-8859-7.
        string_message = str(
            base64.urlsafe_b64decode(raw_msg), "ISO-8859-7")
        # Convert current message to mime format.
        mime_msg = email.message_from_string(string_message)
        # Convert current message from mime to string.
        body, header = mime2str(mime_msg)
        # If message is not empty, keep it.
        if body:
            body_messages.append(body)
            header_messages.append(header)
    return body_messages, header_messages


def get_header(header_text, default="ascii"):
    '''Decode the specified header.

        Args:
            header_text: string that contains a header from a MIME message.
            default: default encoding
        Returns:
            header: decoded header.

        '''
    headers = decode_header(header_text)
    header_sections = []
    for text, charset in headers:
        if charset is not None:
            header_sections.append(str(text, charset or default))
        elif isinstance(text, (bytes, bytearray)):
            header_sections.append(text.decode("utf-8"))
        else:
            header_sections.append(text)
    return u"".join(header_sections)


def get_charset(message, default="ascii"):
    '''Get the charset of a message object.

        Args:
            message: MIME object
            default: default encoding
        Returns:
            charset of message

        '''
    if message.get_content_charset():
        return message.get_content_charset()

    if message.get_charset():
        return message.get_charset()

    return default


def get_body(message):
    '''Get the body of a message object.

        Args:
            message: MIME object
        Returns:
            body_part: string containg the body of the message

        '''
    # Check if the message is multipart.
    if message.is_multipart():
        # Get the plain text version only
        text_parts = [part for part in typed_subpart_iterator(
            message, 'text', 'plain')]
        body = []
        for part in text_parts:
            charset = get_charset(part, get_charset(message))
            if charset == "utf-8":
                body.append(str(part.get_payload(decode=True),
                                charset,
                                "replace"))
            else:
                body.append(part.get_payload())
        body_part = u"\n".join(body).strip()
        return body_part

    else:
        # If it is not multipart, the payload will be a string
        # representing the message body.
        charset = get_charset(message)
        if charset == "utf-8":
            body = str(message.get_payload(decode=True),
                       get_charset(message),
                       "replace")
        else:
            body = message.get_payload()
        body_part = body.strip()
        return body_part


def mime2str(msg):
    '''Convert a mime message in string format.

        Args:
            msg: A mime message.
        Returns:
            body: The body of the message as a string.
            headers: A list that contains the sender, the receiver
                and the subject of the message.

        '''
    # Get the body and clean any html code.
    text_without_html = BeautifulSoup(get_body(msg), "lxml").text
    # Clean the text.
    clean_text = process_text(text_without_html)
    # Keep message and its header only if it contains some text in the body.
    if clean_text:
        headers = [get_header(msg["from"]), get_header(
            msg["to"]), get_header(msg["subject"])]

        return clean_text, headers

    # Else return empty string.
    return "", ""


if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool for extracting sent emails from a user's account
    ''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--output', help="Output directory", required=True)
    optional.add_argument(
        '--reload', help="If true, remove any existing account.", action='store_true')
    optional.add_argument(
        '--info', help="If true, create an info file containing the headers.", action='store_true')
    optional.add_argument(
        '--sentence', help="If true, save each sentence of the emails in separate files.", action='store_true')

    args = parser.parse_args()
    output = args.output
    reload = args.reload
    info = args.info
    sentence = args.sentence

    if not output.endswith('/'):
        output = output + '/'

    print('Connecting to the gmail account...')
    # Connect to the Gmail API.
    service = connect(reload)
    print('Reading emails...')
    # Get the body and the header of the sent messages.
    body, headers = read_emails(service)
    print('Saving emails...')
    # Save messages in txt files.
    save_messages(body, headers, output, info, sentence)
    print(len(body), 'emails have been fetched successfully')
