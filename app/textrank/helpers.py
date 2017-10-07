import nltk
import string


def tokenize_sentences(text):
    '''Tokenizes the given text into a list of sentences.'''

    return nltk.sent_tokenize(text)


def tokenize_words(text, clean=True):
    '''Tokenizes the given text into a list of words.'''

    tokens = nltk.word_tokenize(text)

    if clean:
        unclean = _unclean_words()
        return [t for t in tokens if t not in unclean]

    return tokens


def normalize_url(url):
    clean_url = url.rstrip('/')
    clean_url = clean_url.replace('http://', '', 1)
    clean_url = clean_url.replace('https://', '', 1)
    clean_url = clean_url.replace('www.', '', 1)

    return clean_url


def pos_tag_text(text, clean=True):
    '''POS tag a list of tokens.'''

    tokens = tokenize_words(text, clean=clean)
    return nltk.pos_tag(tokens)


def _unclean_words():
    '''Gets a list of unclean words.'''

    unclean_words = nltk.corpus.stopwords.words('english')
    unclean_words += string.punctuation

    return unclean_words
