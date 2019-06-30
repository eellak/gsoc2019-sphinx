import os
import editdistance


def pos2str(pos):
    '''Each POS tag of a sentence is in form [(word1, pos1), ..., (wordN, posN)]. This function
        converts this form into two strings that contain the word and the pos sequence.

        Args:
            pos: A list of sentences in above form.
        Returns:
            pos_str: A list of strings that contains each sequence of pos tags separated by space.
            text_str: A list of strings that contains each sentence.
        '''
    pos_str = []
    text_str = []
    for sentence in pos:
        text_str.append(' '.join(elem[0] for elem in sentence))
        pos_str.append(' '.join(elem[1] for elem in sentence))
    return pos_str, text_str


def closest_string(x, corpus):
    '''Computes the closest string of x based on the Levenshtein dictance.

        Args:
            x: The string from which the closest string we search.
            corpus: A list of possible closest strings.
        Returns:
            closest: The closest string from x.
            dist: The dictance from the closest string.
        '''
    distances = [editdistance.eval(x, elem) for elem in corpus]
    min_dist = min(distances)
    closest = corpus[distances.index(min_dist)]
    return closest, min_dist


def get_emails(dir):
    '''Get emails from a specific directory and return them as a list.

        Args:
            dir: Directory that contains the emails in text files.
        Returns:
            emails: A list that contains the emails in string format.

        '''
    # If input directory does not exist, exit with error.
    if not os.path.exists(dir):
        sys.exit('Email folder does not exist')

    emails = []
    for email in os.listdir(dir):
        with open(dir + email, 'r') as f:
            emails.append(f.read())
    return emails
