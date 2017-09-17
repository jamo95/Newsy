from app.textrank.graph import Graph
from app.textrank.node import Node


def test_add_node():
    graph = Graph()
    graph.add_node(Node('a'))

    assert Node('a') in graph._adjacency_list.keys()
    assert len(graph._adjacency_list.keys()) == 1
    assert len(graph._adjacency_list[Node('a')]) == 0


def test_add_duplicate_node():
    graph = Graph()
    graph.add_node(Node('a'))
    graph.add_node(Node('a'))

    assert Node('a') in graph._adjacency_list.keys()
    assert len(graph._adjacency_list.keys()) == 1
    assert len(graph._adjacency_list[Node('a')]) == 0


def test_add_edge():
    graph = Graph()
    graph.add_edge(Node('a'), Node('b'))

    assert Node('a') in graph._adjacency_list.keys()
    assert Node('b') in graph._adjacency_list.keys()
    assert len(graph._adjacency_list.keys()) == 2
    assert len(graph._adjacency_list[Node('a')]) == 1
    assert len(graph._adjacency_list[Node('b')]) == 0


def test_add_duplicate_edge():
    graph = Graph()
    graph.add_edge(Node('a'), Node('b'))
    graph.add_edge(Node('a'), Node('b'))

    assert Node('a') in graph._adjacency_list.keys()
    assert Node('b') in graph._adjacency_list.keys()
    assert len(graph._adjacency_list.keys()) == 2
    assert len(graph._adjacency_list[Node('a')]) == 1
    assert len(graph._adjacency_list[Node('b')]) == 0


def test_get_nodes_count():
    graph = Graph()
    graph.add_node(Node('a'))

    assert graph.get_nodes_count() == 1


def test_get_edges_count():
    graph = Graph()
    graph.add_edge(Node('a'), Node('b'))

    assert graph.get_nodes_count() == 2
    assert graph.get_edges_count() == 1


def test_has_node():
    graph = Graph()
    graph.add_node(Node('a'))

    assert graph.has_node('a')
    assert not graph.has_node('b')


def test_get_nodes():
    graph = Graph()
    graph.add_node(Node('a'))
    graph.add_node(Node('b'))

    nodes = graph.get_nodes()
    assert len(nodes) == 2
    assert Node('a') in nodes and Node('b') in nodes


def test_get_connected_to():
    graph = Graph()
    graph.add_edge(Node('b'), Node('a'))
    graph.add_edge(Node('c'), Node('a'))

    assert graph.get_nodes_count() == 3
    assert graph.get_edges_count() == 2

    connected_to = graph.get_connected_to(Node('a'))
    assert len(connected_to) == 2
    assert Node('b') in connected_to
    assert Node('c') in connected_to


def test_get_connected_from():
    graph = Graph()
    graph.add_edge(Node('a'), Node('b'))
    graph.add_edge(Node('a'), Node('c'))

    assert graph.get_nodes_count() == 3
    assert graph.get_edges_count() == 2

    connected_from = graph.get_connected_from(Node('a'))
    assert len(connected_from) == 2
    assert Node('b') in connected_from
    assert Node('c') in connected_from
