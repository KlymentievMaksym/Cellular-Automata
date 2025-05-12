import numpy as np
import copy


class Cell:
    def __init__(self, state=0):
        self.state = state
        self.neighbours = None

    def ConnectNeighbours(self, neighbours: np.ndarray['Cell']):
        self.neighbours = neighbours

    def ApplyRule(self, rule: callable, cell=None):
        if cell is None:
            return rule(self)
        return rule(cell)

    def __copy__(self):
        return type(self)(self.state)

    def __deepcopy__(self, memo):
        copied = type(self)(copy.deepcopy(self.state, memo))
        copied.neighbours = copy.deepcopy(self.neighbours, memo)
        return copied

    def __array__(self, dtype=None):
        return np.array(float(self), dtype=dtype)

    def __gt__(self, other):
        return self.state > other

    def __add__(self, other: 'Cell'):
        return self.state + other.state

    def __radd__(self, other):
        return other + self.state

    def __float__(self):
        return float(self.state)

    def __repr__(self):
        return str(self.state)

    def __str__(self):
        return str(self.state)
