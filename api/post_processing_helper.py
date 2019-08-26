import arpa
from nltk.util import ngrams


def error_detector(lmAdaptPath, sentence, threshold):
    # Reading input language model.
    models = arpa.loadf(lmAdaptPath)
    # ARPA files may contain several models.
    lm = models[0]
    words = sentence.split()
    scores = dict(zip(words, [0] * len(words)))
    n_grams = list(ngrams(words, 3))
    for n_gram in n_grams:
        prop = lm.p(n_gram)
        if prop < threshold:
            for word in n_gram:
                scores[word] += 1
    sent_errors = ['0']
    for n_gram in n_grams:
        if scores[n_gram[1]] > 1:
            sent_errors.append('1')
        else:
            sent_errors.append('0')
    sent_errors.append('0')
    return " ".join(sent_errors)
