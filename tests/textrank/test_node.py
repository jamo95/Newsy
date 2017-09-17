from app.textrank.node import Node


def test_equality():
    node_a = Node('a')
    node_b = Node('a')

    assert node_a == node_b


def test_inequality():
    node_a = Node('a')
    node_b = Node('b')

    assert node_a != node_b


def test_add_variation():
    node = Node('a')
    node.add_variation('v')

    assert set(node._variations) == set(['v'])


def test_remove_variation():
    node = Node('a')
    node._variations = ['v1', 'v2']
    node.remove_variation('v1')

    assert set(node._variations) == set(['v2'])


def test_has_variation():
    node = Node('a')
    node._variations = ['v']

    assert node.has_variation('v')
    assert not node.has_variation('w')


def test_get_variations():
    node = Node('a')
    node._variations = ['v']

    assert set(node.get_variations()) == set(['v'])


def test_get_averaged_score_variations():
    node = Node('a', score=10)
    node._variations = ['v1', 'v2']

    assert node.get_averaged_score() == 5.0


def test_get_averaged_score_data():
    node = Node('a', score=10)

    assert len(node._variations) == 0
    assert node.get_averaged_score() == 10.0
