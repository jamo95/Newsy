from app.textrank.node import Node


# This is an undirected, unweighted graph represented by an adjacnecy list.
class Graph:
    def __init__(self):
        # Adjacency list of node to list of nodes. The key node represents the
        # initial node in the edge, and each node in the list represents an
        # edge where it is the final node.
        self._adjacency_list = {}

    def add_node(self, node):
        '''Add node to the graph.'''

        if node not in self._adjacency_list:
            self._adjacency_list[node] = []

    def add_edge(self, node_i, node_f):
        '''Add edge to the graph. If node_i or node_f doesn't exist then it
        will add them to the graph.'''

        if (node_i == node_f):
            return

        self.add_node(node_i)
        self.add_node(node_f)

        if node_f not in self._adjacency_list[node_i]:
            self._adjacency_list[node_i].append(node_f)
            

    def get_nodes_count(self):
        '''Return the number of nodes in the graph.'''

        return len(self._adjacency_list.keys())

    def get_edges_count(self):
        '''Return the number of edges in the graph.'''

        return sum(map(len, self._adjacency_list.values()))

    def has_node(self, data):
        '''Return true if there exists a node with the specified data.'''

        return Node(data) in self._adjacency_list

    def get_nodes(self):
        '''Get all nodes in the graph.'''

        return self._adjacency_list.keys()

    def get_connected_to(self, node_f):
        '''Get all the nodes connected to final node `node_f`.'''

        connected_to = []
        for i, f in self._adjacency_list.items():
            if node_f in f:
                connected_to.append(i)

        return connected_to

    def get_connected_from(self, node_i):
        '''Get all the nodes connected to initial node `node_i`.'''
        return self._adjacency_list[node_i]

    def find(self, node_id=None, node_text=None, node_variation=None):
        '''Finds the first node in the graph by `node_id`, `node_text`, or
        `node_variations`.'''

        if node_id:
            # Search by Node ID.
            found = list(filter(_filter_node_id(node_id), self.nodes))
            if len(found) > 0:
                return found[0]

        if node_text:
            # Search by Node Text.
            found = list(filter(_filter_node_text(node_text), self.nodes))
            if len(found) > 0:
                return found[0]

        if node_variation:
            # Search by Node Variations.
            found = list(filter(_filter_node_variation(node_variation), self.nodes))
            if len(found) > 0:
                return found[0]
