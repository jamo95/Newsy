import nltk
import string


def tokenize_sentences(text):
    '''Tokenizes the given text into a list of sentences.'''

    return nltk.sent_tokenize(text)


def tokenize_words(text, clean=True):
    '''Tokenizes the given text into a list of words.'''

    tokens = nltk.word_tokenize(text)
    # Comment out below if you dont want to lowercase everything
    tokens = [t.lower() for t in tokens]

    # NN => Noun JJ => Adjective NNP => Pronoun
    tags = ['NN', 'JJ']
    tokens  = pos_tag_tokens(tokens)
    tokens  = [t[0] for t in tokens if t[1] in tags]

    if clean:
        unclean = _unclean_words()
        clean = [t for t in tokens if t not in unclean]
        return clean

    return tokens


def normalize_url(url):
    clean_url = url.rstrip('/')
    clean_url = clean_url.replace('http://', '', 1)
    clean_url = clean_url.replace('https://', '', 1)
    clean_url = clean_url.replace('www.', '', 1)

    return clean_url


def pos_tag_tokens(tokens, clean=True):
    '''POS tag a list of tokens.'''

    return nltk.pos_tag(tokens)


def _unclean_words():
    '''Gets a list of unclean words.'''

    unclean_words = nltk.corpus.stopwords.words('english')
    unclean_words += string.punctuation

    return unclean_words
