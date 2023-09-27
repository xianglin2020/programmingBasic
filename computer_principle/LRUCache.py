#! -*- encoding=utf-8 -*-

from DoubleLinkedList import DoubleLinkedList, Node


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.map = {}
        self.list = DoubleLinkedList(capacity)

    def get(self, key):
        if key in self.map:
            node = self.map[key]
            self.list.remove(node)
            self.list.append_front(node)
            return node.value
        else:
            return -1

    def put(self, key, value):
        if self.capacity == 0:
            return
        if key in self.map:
            node = self.map[key]
            self.list.remove(node)
            node.value = value
            self.list.append_front(node)
        else:
            if self.capacity == self.size:
                node = self.list.remove()
                del self.map[node.key]
                self.size -= 1
            node = Node(key, value)
            self.map[key] = node
            self.list.append_front(node)
            self.size += 1

    def print(self):
        self.list.print()


if __name__ == '__main__':
    cache = LRUCache(2)
    cache.put(2, 2)
    cache.print()
    cache.put(1, 1)
    cache.print()
    cache.put(3, 3)
    cache.print()
    print(cache.get(1))
    cache.print()
    print(cache.get(2))
    cache.print()
    print(cache.get(3))
    cache.print()
