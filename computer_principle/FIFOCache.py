#! -*- encoding=utf-8 -*-

from DoubleLinkedList import DoubleLinkedList, Node


class FIFOCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.map = {}
        self.list = DoubleLinkedList(capacity)

    def get(self, key):
        if key in self.map:
            return self.map[key].value
        else:
            return -1

    def put(self, key, value):
        if self.capacity == 0:
            return

        if key in self.map:
            self.map[key].value = value
        else:
            if self.size == self.capacity:
                node = self.list.pop()
                del self.map[node.key]
                self.size -= 1

            node = Node(key, value)
            self.map[key] = node
            self.list.append(node)
            self.size += 1

    def print(self):
        self.list.print()


if __name__ == '__main__':
    cache = FIFOCache(2)
    cache.put(1, 1)
    cache.print()
    cache.put(2, 2)
    cache.print()
    print(cache.get(1))
    cache.put(3, 3)
    cache.print()
    print(cache.get(2))
    cache.print()
    cache.put(4, 4)
    cache.print()
    print(cache.get(1))
