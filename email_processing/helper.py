from alphabet_detector import AlphabetDetector


def process_text(text):

    ad = AlphabetDetector()
    out = ""
    lines = text.split('\n')
    for i in range(len(lines)):
        if lines[i].startswith('>'):
            continue
        elif lines[i].startswith('Στις') and lines[i].strip().endswith('έγραψε:'):
            break
        elif i < len(lines) - 1 and lines[i].startswith('Στις') and lines[i + 1].strip().endswith('έγραψε:'):
            break
        else:
            for word in lines[i].split(' '):
                if ad.only_alphabet_chars(word, "GREEK"):
                    out += word + ' '
    return out.replace("\r", "")


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
                    header_messages[i][0] + ' | ' + header_messages[i][1] + ' | ' + header_messages[i][2])
                w1.write('\n')
                w2.write(msg)
