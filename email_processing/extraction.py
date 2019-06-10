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

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def connect():
    '''Open the default browser and ask the user for authentication reading his emails.

        Returns:
            service: A recourse object. All calls will be done through this object.

        '''
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
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
    '''Read the user's sent emails and return them as a list of mime messages.

        Args:
            service: A recourse object, that helps us make requests.
            limit: Total number of messages to read.
            save_raw: If true, raw message files will be saved too.
        Returns:
            mime_messages: A list contatining all the sent emails in MIME format.

        '''
    # Call the Gmail API and get all sent emails.
    results = service.users().messages().list(
        userId='me', maxResults=limit, labelIds=['SENT']).execute()
    # Get user's messages based on given limit.
    messages = results.get('messages', [])
    mime_messages = []
    for idx, message in enumerate(messages):
        # Get message based in the id.
        msg_dict = service.users().messages().get(
            userId='me', id=message['id'], format='raw').execute()
        raw_msg = msg_dict['raw']
        # Convert message encoding from base64 to iso-8859-7.
        string_message = str(base64.urlsafe_b64decode(raw_msg), "ISO-8859-7")
        # Convert current message to mime format.
        mime_msg = email.message_from_string(string_message)
        mime_messages.append(mime_msg)
        if save_raw:
            with open('/texts/raw_email_' + str(idx), 'w') as w:
                w.write(string_message)
    return mime_messages


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
        if charset == "utf-8":
            body = str(message.get_payload(decode=True),
                       get_charset(message),
                       "replace")
        else:
            body = message.get_payload()
        body_part = body.strip()
        return body_part


def mime2str(messages):
    '''Convert a list of raw messages to a list of strings.

        Args:
            messages: A list of raw messages.
        Returns:
            body_messages: A list of strings containing the body of each message.
            header_messages: A list of lists that contains the sender, the receiver
                and the subject of each message.

        '''
    body_messages = []
    header_messages = []
    for msg in messages:
        # Get the body and clean any html code.
        clean_text = BeautifulSoup(get_body(msg), "lxml").text
        # Remove non-greek and other symbols.
        processed_text = process_text(clean_text)
        # Keep message and its header only if it contains some text in the body.
        if processed_text and not processed_text.isspace():
            body_messages.append(processed_text)
            header_messages.append([get_header(msg["from"]), get_header(
                msg["to"]), get_header(msg["subject"])])

    return body_messages, header_messages


if __name__ == '__main__':
    # Connect to the Gmail API.
    service = connect()
    # Get the body of the inbox messages in raw format.
    raw_messages = read_emails(service)
    # Get the body and the header of each message.
    body_messages, header_messages = mime2str(raw_messages)
    # Save messages in txt files.
    save_messages(body_messages, header_messages)
