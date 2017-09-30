from app.textrank import helpers


def test_tokenize_sentences():
    sentences = [
        'This is a sentence.',
        'This is another sentence.'
    ]

    assert helpers.tokenize_sentences(' '.join(sentences)) == sentences


def test_tokenize_words():
    words = ['This', 'is', 'a', 'sentence.']

    assert helpers.tokenize_words(' '.join(words)) == ['This', 'sentence']


def test_pos_tag_text():
    sentence = 'A quick brown fox named Josh.'

    assert helpers.pos_tag_text(sentence) == [
        ('A', 'DT'), ('quick', 'JJ'), ('brown', 'NN'), ('fox', 'NN'),
        ('named', 'VBN'), ('Josh', 'NNP')
    ]
