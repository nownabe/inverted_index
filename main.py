from collections import Counter

import numpy as np
from numpy.random import seed, rand

from benchmarker import Benchmarker

class Naive(object):
    def __init__(self, table):
        self.table = table

    def calc(self, item):
        scores = [self.similarity(item, j) for j in range(self.table.shape[0])]
        return scores

    def similarity(self, i, j):
        a = self.table[i]
        b = self.table[j]
        return (a & b).sum() / (a | b).sum()


class InvertedIndex(object):
    def __init__(self, table):
        self.item_users_index = {}
        self.user_items_index = {}
        self.num_items = table.shape[0]
        self.item_norms = np.zeros(self.num_items)

        for i in range(table.shape[0]):
            users = np.argwhere(table[i] == 1)
            self.item_users_index[i] = users.reshape(users.shape[0])
            self.item_norms[i] = table[i].sum()

        inverted_table = table.T
        for i in range(inverted_table.shape[0]):
            items = np.argwhere(inverted_table[i] == 1)
            self.user_items_index[i] = items.reshape(items.shape[0])

    def calc(self, item):
        users = self.item_users_index[item]
        counter = Counter()
        for user in users:
            counter.update(self.user_items_index[user])

        counted = [counter[i] for i in range(self.num_items)]

        scores = [counted[i] / (self.item_norms[item] + self.item_norms[i] - counted[i]) for i in range(self.num_items)]
        return scores


threshold = 0.3


seed(0)
num_users = 5
num_items = 10

table = (rand(num_users, num_items) >= threshold).astype(int)
print("table:")
print(table)

naive = Naive(table)
iisim = InvertedIndex(table)

for i in range(table.shape[0]):
    naive_scores = naive.calc(i)
    iisim_scores = iisim.calc(i)
    for j in range(table.shape[0]):
        print(f"{i:d} <=> {j:d}: Naive={naive_scores[j]:.3f}, InvertedIndex={iisim_scores[j]:.3f}")


seed(0)
num_users = 500
num_items = 1000
big_table = (rand(num_users, num_items) >= threshold).astype(int)

naive = Naive(big_table)
iisim = InvertedIndex(big_table)

with Benchmarker(1) as bench:
    @bench("Naive")
    def _(bm):
        for i in range(big_table.shape[0]):
            naive.calc(i)

    @bench("Inverted Index")
    def _(bm):
        for i in range(big_table.shape[0]):
            iisim.calc(i)
