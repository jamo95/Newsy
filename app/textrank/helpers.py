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

    if clean:
        tokens = _clean_words(tokens)
        tagged_tokens = pos_tag_tokens(tokens)
        tokens = lemmatize(tagged_tokens)

    return tokens


def normalize_url(url):
    clean_url = url.rstrip('/')
    clean_url = clean_url.replace('http://', '', 1)
    clean_url = clean_url.replace('https://', '', 1)
    clean_url = clean_url.replace('www.', '', 1)

    return clean_url


def pos_tag_tokens(tokens,wanted_tags=['J','N'], clean=True):
    '''POS tag a list of tokens. 
    Note that wanted_tags is just start of tag wanted
    https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html 
    for definitions '''

    tagged = nltk.pos_tag(tokens)
    return [t for t in tagged if t[1][0] in wanted_tags]


def _clean_words(words):
    '''Returns a list of clean words.'''

    unclean_words = nltk.corpus.stopwords.words('english')
    unclean_words += string.punctuation

    clean_words = [t for t in words if t not in unclean_words]

    return clean_words

def lemmatize(tagged_tokens):
    lemmatized = []
    lemmatizer = nltk.wordnet.WordNetLemmatizer()
    for t in tagged_tokens:
        lemma = lemmatizer.lemmatize(
                t[0], get_wordnet_pos(t[1]))

        lemmatized.append(lemma)
    return lemmatized

# Cannibalized from a stackoverflow post
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return 'a'
    elif treebank_tag.startswith('V'):
        return 'v'
    elif treebank_tag.startswith('N'):
        return 'n'
    elif treebank_tag.startswith('R'):
        return 'r'
    else:
        # If we get here gg...
        return None
