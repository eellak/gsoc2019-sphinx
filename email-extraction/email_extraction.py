from __future__ import print_function
import urllib
from bs4 import BeautifulSoup
import base64
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import email
from email.header import decode_header
from email.iterators import typed_subpart_iterator


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
    '''Read the user's emails and return them as a list of mime messages.

        Args:
            service: A recourse object, that helps us make requests.
            limit: Total number of messages to read.
            save_raw: If true, raw message files are saved too.
        Returns:
            mime_messages: A list contatining all the emails in MIME format.

        '''
    # Call the Gmail API.
    results = service.users().messages().list(
        userId='me', maxResults=limit).execute()
    # Get user's messages based on given limit.
    messages = results.get('messages', [])
    mime_messages = []
    for idx, message in enumerate(messages):
        # Get message based in the id.
        msg_dict = service.users().messages().get(
            userId='me', id=message['id'], format='raw').execute()
        raw_msg = msg_dict['raw']
        # Convert message encoding from base64 to utf-8.
        string_message = str(base64.urlsafe_b64decode(raw_msg), "utf-8")
        # Convert current message to mime format.
        mime_msg = email.message_from_string(string_message)
        mime_messages.append(mime_msg)
        if save_raw:
            with open('raw_email_' + str(idx), 'w') as w:
                w.write(string_message)
    return mime_messages


def clean_html(html_text):
    '''Remove html code from a given text, using the BeautifulSoup library.

        Args:
            html_text: string that may contain html code.
        Returns:
            clean_text: string that is equal to html_text without the html code.

        '''
    soup = BeautifulSoup(html_text, features='lxml')
    # Kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()
    # Get text
    text = soup.get_text()
    # Break it into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    clean_text = '\n'.join(chunk for chunk in chunks if chunk)

    return clean_text


def get_header(header_text, default="ascii"):
    '''Decode the specified header.

        Args:
            header_text: string that contains a header from a MIME message.
            default: default encoding
        Returns:
            header: decoded header.

        '''
    headers = decode_header(header_text)

    header_sections = [str(text, charset or default)
                       if charset is not None else text for text, charset in headers]
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
            body.append(str(part.get_payload(decode=True),
                            charset,
                            "replace"))

        body_part = u"\n".join(body).strip()
        return body_part

    else:
        # If it is not multipart, the payload will be a string
        # representing the message body.
        body = str(message.get_payload(decode=True),
                   get_charset(message),
                   "replace")
        body_part = body.strip()
        return body_part


def save(messages):
    '''Get the body of a message object.
        Args:
            message: MIME object

        '''
    with open('info', 'w') as w1:
        for i, msg in enumerate(raw_messages):
            with open('email_' + str(i), 'w') as w2:
                w1.write(msg["from"] + ' ' + msg["to"] +
                         ' ' + get_header(msg['subject']))
                w1.write('\n')
                w2.write(clean_html(get_body(msg)))


if __name__ == '__main__':
    # Connect to the Gmail API.
    service = connect()
    # Get the body of the inbox messages.
    raw_messages = read_emails(service, 10)
    # Save messages.
    save(raw_messages)
