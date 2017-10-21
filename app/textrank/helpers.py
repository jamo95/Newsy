import nltk
import string
import re

def tokenize_sentences(text):
    '''Tokenizes the given text into a list of sentences.'''

    return nltk.sent_tokenize(text)


def tokenize_words(text, clean=True):
    '''Tokenizes the given text into a list of words.'''

    # Only ASCII
    #text = ''.join(s for s in text if s in string.printable)
    tokens = []
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        for word in words:
            tokens.append(word)

    if clean:
        unclean_words = get_unclean_words(tokens)

        tokens = [t.lower() for t in tokens]
        tokens = [t for t in tokens if t not in unclean_words]

        alphanumeric = re.compile("^[A-Za-z0-9]+$")
        tokens = [t for t in tokens if re.match(alphanumeric, t)]
       
        #for t in tokens:
        #    if not re.match(alphanumeric, t):
        #        print(t)
        #print(tokens)

        tagged_tokens = pos_tag_tokens(tokens)
        tokens = lemmatize(tagged_tokens)


    return tokens


def normalize_url(url):
    clean_url = url.rstrip('/')
    clean_url = clean_url.replace('http://', '', 1)
    clean_url = clean_url.replace('https://', '', 1)
    clean_url = clean_url.replace('www.', '', 1)

    return clean_url


def pos_tag_tokens(tokens,wanted_tags=['JJ','NN'], clean=True):
    '''POS tag a list of tokens. 
    Note that wanted_tags is just start of tag wanted
    https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html 
    for definitions '''

    tagged = nltk.pos_tag(tokens)
    return [t for t in tagged if t[1] in wanted_tags]


def get_unclean_words(words):
    '''Returns a list of clean words.'''

    unclean_words = nltk.corpus.stopwords.words('english')
    unclean_words += string.punctuation

    return unclean_words

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
