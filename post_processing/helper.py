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


def closest_sentence(x, x_pos, corpus, corpus_pos, w=0.5):
    '''Computes the closest seentence of x based on the Levenshtein dictance fo both
        the words and the POS tagging.

        Args:
            x: The sentence from which the closest sentence we search.
            corpus: A list of possible closest sentences.
            w: Weight between words and POS tag.
        Returns:
            closest: The closest sentence from x.
            dist_word: The dictance from the closest sentence.
            dist_pos: The pos distance from the closest sentence.
        '''
    word_distances = [editdistance.eval(x, elem) for elem in corpus]
    pos_distances = [editdistance.eval(
        x_pos, elem) for elem in corpus_pos]
    total_distances = [word_distances[i] * w + pos_distances[i]
                       * (1 - w) for i in range(len(word_distances))]
    min_dist = min(total_distances)
    idx = total_distances.index(min_dist)
    closest = corpus[idx]
    dist_word = word_distances[idx]
    dist_pos = pos_distances[idx]
    return closest, dist_word, dist_pos


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
