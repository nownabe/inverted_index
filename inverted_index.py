import numpy as np

class InvertedIndex(object):
    def __init__(self, items=0, users=0):
        self.num_items = items
        self.item_norms = [0 for _ in range(items)]
        self.item_users_index = {i:set() for i in range(items)}
        self.user_items_index = {i:set() for i in range(users)}

    def add_item(self, item):
        self.item_users_index[item] = set()
        self.num_items += 1
        self.item_norms.append(0)

    def delete_item(self, item):
        del(self.item_users_index[item])
        for v in self.user_items_index.values():
            if item in v:
                v.remove(item)
        self.num_items -= 1
        del(self.item_norms[item])

    def add_user(self, user):
        self.user_items_index[user] = set()

    def delete_user(self, user):
        del(self.user_items_index[user])
        for item, users in self.item_users_index.items():
            if user in users:
                v.remove(user)
                self.item_norms[item] -= 1

    def add_purchase(self, item, user):
        if user not in self.item_users_index[item]:
            self.item_users_index[item].add(user)
            self.user_items_index[user].add(item)
            self.item_norms[item] += 1

    def calc(self, item):
        users = self.item_users_index[item]
        cunter = Counter()
        for user in users:
            counter.update(self.user_items_index[user])

        counted = [counter[i] for i in range(self.num_items)]
        scores = [counted[i] / (self.item_norms[item] + self.item_norms[i] - counted[i]) for i in range(self.num_items)]
        return scores
