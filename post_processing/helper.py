import os
import editdistance
from sklearn.metrics.pairwise import cosine_similarity
import re
from nltk.util import ngrams
import spacy


def closest_pos(x, x_pos, corpus, w=0.5):
    '''Computes the closest sentence of x based on the Levenshtein dictance for both
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
    distance = 100000
    min_sent = None
    pos_dist = None
    word_dist = None
    first = x.split()[0]
    for elem in corpus:
        if first not in elem.split():
            continue
        curr_word_dist = editdistance.eval(x, elem)
        curr_pos_dict = editdistance.eval(x_pos, corpus[elem])
        curr_total_dist = curr_word_dist * w + curr_pos_dict * (1 - w)
        if curr_total_dist < distance:
            distance = curr_total_dist
            min_sent = [elem]
            pos_dist = curr_pos_dict
            word_dist = curr_word_dist
        elif curr_total_dist == distance and elem not in min_sent:
            min_sent.append(elem)

    if min_sent == None:
        for elem in corpus:
            curr_word_dist = editdistance.eval(x, elem)
            curr_pos_dict = editdistance.eval(x_pos, corpus[elem])
            curr_total_dist = curr_word_dist * w + curr_pos_dict * (1 - w)
            if curr_total_dist < distance:
                distance = curr_total_dist
                min_sent = [elem]
                pos_dist = curr_pos_dict
                word_dist = curr_word_dist
            elif curr_total_dist == distance and elem not in min_sent:
                min_sent.append(elem)
    return min_sent, word_dist, pos_dist


def closest_vec(x, x_vec, corpus, w=0.5):
    '''Computes the closest sentence of x based on the Levenshtein dictance for both
        the words and the semantic vectors.

        Args:
            x: The sentence from which the closest sentence we search.
            corpus: A list of possible closest sentences.
            w: Weight between words and POS tag.
        Returns:
            closest: The closest sentence from x.
            dist_word: The dictance from the closest sentence.
            dist_pos: The similatiry from the closest sentence.
        '''
    distance = 100000
    min_sent = None
    vec_dist = None
    word_dist = None
    first = x.split()[0]
    for elem in corpus:
        if first not in elem.split():
            continue
        curr_word_dist = editdistance.eval(x, elem)
        curr_vec_dict = 1 - cosine_similarity([x_vec], [corpus[elem]])[0][0]
        curr_total_dist = curr_word_dist * w + curr_vec_dict * (1 - w)
        if curr_total_dist < distance:
            distance = curr_total_dist
            min_sent = [elem]
            vec_dist = curr_vec_dict
            word_dist = curr_word_dist
        elif curr_total_dist == distance and elem not in min_sent:
            min_sent.append(elem)

    if min_sent == None:
        for elem in corpus:
            curr_word_dist = editdistance.eval(x, elem)
            curr_vec_dict = 1 - \
                cosine_similarity([x_vec], [corpus[elem]])[0][0]
            curr_total_dist = curr_word_dist * w + curr_vec_dict * (1 - w)
            if curr_total_dist < distance:
                distance = curr_total_dist
                min_sent = [elem]
                vec_dist = curr_vec_dict
                word_dist = curr_word_dist
            elif curr_total_dist == distance and elem not in min_sent:
                min_sent.append(elem)
    return min_sent, word_dist, vec_dist


def closest_ngram(x, corpus):
    distance = 100000
    min_sent = None
    first = x.split()[0]
    for elem in corpus:
        if first not in elem.split():
            continue
        curr_dist = editdistance.eval(x, elem)
        if curr_dist < distance:
            distance = curr_dist
            min_sent = [elem]
        elif curr_dist == distance and elem not in min_sent:
            min_sent.append(elem)
    if min_sent == None:
        for elem in corpus:
            curr_dist = editdistance.eval(x, elem)
            if curr_dist < distance:
                distance = curr_dist
                min_sent = [elem]
            elif curr_dist == distance and elem not in min_sent:
                min_sent.append(elem)
    return min_sent, distance


def get_sentences(dir):
    '''Get all the sentences of the emails from a specific directory and return them as a list.

        Args:
            dir: Directory that contains the emails in text files.
        Returns:
            emails: A list that contains the sentences of the emails in string format.

        '''
    if not os.path.exists(dir):
        sys.exit('Email folder does not exist')

    emails = []
    for email in os.listdir(dir):
        with open(os.path.join(dir, email), 'r') as f:
            # Each line represents a sentence.
            for line in f:
                emails.append(line.strip('\n'))
    return emails


def get_pos_doc(doc):
    tags_doc = []
    for tok in doc:
        tags_doc.append(tok.pos_)
    return " ".join(tags_doc)


def get_pos_sentence(sentences, n):
    tags = {}
    nlp = spacy.load('el_core_news_sm')
    for size in n:
        for sent in sentences:
            n_grams = ngrams(sent.split(), size)
            for n_gram in list(n_grams):
                n_gram_text = ' '.join(n_gram)
                doc = nlp(n_gram_text)
                if n_gram_text not in tags:
                    tags[n_gram_text] = get_pos_doc(doc)
    return tags


def get_vec(sentences, n):
    vectors = {}
    nlp = spacy.load('el_core_news_md')
    for size in n:
        for sent in sentences:
            n_grams = ngrams(sent.split(), size)
            for n_gram in list(n_grams):
                n_gram_text = ' '.join(n_gram)
                doc = nlp(n_gram_text)
                if n_gram_text not in vectors:
                    vectors[n_gram_text] = doc.vector
    return vectors


def get_ngrams(sentences, n):
    corpus = []
    for size in n:
        for sent in sentences:
            corpus.extend([" ".join(ngram)
                           for ngram in ngrams(sent.split(), size)])
    return corpus


def get_hypothesis(file, has_id):
    '''Read emails from a hypothesis file (one per line).

        Args:
            file: Path to the hypothesis file.
            has_id: If true, the file contains the id of the email at the end of each line (Sphinx format).
        Returns:
            emails: A list the contains the emails.
        '''
    emails = []
    with open(file, 'r') as f:
        for email in f:
            if has_id:
                # Remove id from each email.
                emails.append(
                    re.sub(r'\([^)]*\)$', '', email).strip('\n').strip(' '))
            else:
                emails.append(email.strip('\n').strip(' '))
    return emails
