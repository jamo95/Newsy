class Node:
    def __init__(self, data, score=1.0, multiplier=1.0):
        # Base data for the node. For a word this will be the stemmed version.
        # For a sentence it will just be the sentence.
        self.data = data

        # Score of the node. If the node also has variations then this will be
        # the sum of all the variations. If the node has no variations then it
        # will be the score of the data.
        self.score = score

        # Score multiplier for the node. May be useful when we want to boost
        # the value of specific nodes without explicitely modifying the score.
        self.multiplier = multiplier

        # Variations of the data. For a word this will be the stem of the word.
        # For a sentence this will likely be empty.
        self._variations = []

    def __eq__(self, node):
        return self.data == node.data

    def __neq__(self, node):
        return not self.__eq__(node)

    def __hash__(self):
        return hash(self.data)

    def add_variation(self, data):
        '''Add a variation to the node.'''

        if not self.has_variation(data):
            self._variations.append(data)

    def remove_variation(self, data):
        '''Remove a variation from the node.'''

        if self.has_variation(data):
            self._variations.remove(data)

    def has_variation(self, data):
        '''Return true if node has the provided variation.'''

        return data in self._variations

    def get_variations(self):
        '''Return all variations.'''

        return self._variations

    def get_averaged_score(self):
        '''Get the score of the node averaged over all variations.'''

        if len(self._variations) == 0:
            return float(self.score)
        return float(self.score) / float(len(self._variations))
