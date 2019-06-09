from bs4 import BeautifulSoup
from alphabet_detector import AlphabetDetector


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


def keep_greek(text):
    '''Keep only greek words from a text.

        Args:
            message: MIME object
        Returns:
            body_part: string containg the body of the message

        '''
    ad = AlphabetDetector()
    greek = ""
    for word in text.split(' '):
        if ad.only_alphabet_chars(word, "GREEK"):
            greek += ' ' + word
    return greek


def save_messages(body_messages, header_messages):
    '''Save messages in separate files and keeps an info file with the headers.

        Args:
            body_messages: A list of strings that contains the body of the messages.
            header_messages: A list of strings that contains the header of the messages.

        '''
    # Keep an info file that contains the sender, the
    # receiver and the subject of the message.
    with open('info', 'w') as w1:
        for i, msg in enumerate(body_messages):
            with open('./texts/email_' + str(i), 'w') as w2:
                w1.write(
                    body_messages[i][0] + ' | ' + body_messages[i][1] + ' | ' + body_messages[i][2])
                w1.write('\n')
                w2.write(msg)
