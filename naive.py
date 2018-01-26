import numpy as np

class Naive(object):
    def __init__(self, items=0, users=0):
        self.table = np.zeros([items, users], dtype=int)

    def add_item(self, item):
        self.table.append(np.zeros(self.table.shape[1], dtype=int))

    def delete_item(self, item):
        np.delete(self.table, item, axis=0)

    def add_user(self, user):
        self.table = np.hstack([self.table, np.zeros([self.table.shape[0], 1], dtype=int))

    def delete_user(self, user):
        np.delete(self.table, user, axis=1)
        pass

    def add_purchase(self, item, user):
        self.table[item, user] = 1

    def calc(self, item):
        scores = [self._calc(item, j) for j in range(self.table.shape[0])]
        return scores

    def _calc(self, i, j):
        a = self.table[i]
        b = self.table[j]
        return (a & b).sum() / (a | b).sum()
