"""
Design a data structure that supports insert, remove, and get random element operations in constant time.0(1)

insert(x) - Insert an element x to the data structure.
remove(x) - Remove an element x from the data structure.
get_random() - Get a random element from the data structure.


"""

import random


class O1DataStructure:
    def __init__(self):
        self.dict = {}
        self.values = []

    def insert(self, x):
        if x in self.dict:
            return False
        self.values.append(x)
        self.dict[x] = len(self.values) - 1
        return True

    def remove(self, x):
        # print("remove", self.dict)
        if x not in self.dict:
            return False
        index = self.dict[x]

        last_element = self.values[-1]
        self.values[index] = last_element
        self.dict[last_element] = index

        self.values.pop()
        del self.dict[x]
        return True

    def search(self, x):
        return x in self.dict

    def get_random(self):
        if not self.values:
            return None
        return random.choice(self.values)


def test_cases():
    ds = O1DataStructure()

    # insert
    print("insert 10", ds.insert(10))
    print("insert 20", ds.insert(20))
    print("insert 30", ds.insert(30))
    print("insert 40", ds.insert(40))
    print("insert 50", ds.insert(50))

    # Search
    print("search 10", ds.search(10))
    print("search 90", ds.search(90))

    # get random
    print("random 1", ds.get_random())
    print("random 2", ds.get_random())
    print("random 3", ds.get_random())

    # remove
    print("remove 20", ds.remove(20))
    print("search 20", ds.search(20))
    print("remove 20", ds.remove(20))

    print("all data", ds.values)
    print("insert 40", ds.insert(40))
    print("all data after 40", ds.values)
    print("last random", ds.get_random())


test_cases()
