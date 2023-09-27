#! -*- encoding=utf-8 -*-

from DoubleLinkedList import DoubleLinkedList, Node


class LFUNode(Node):
    def __init__(self, key, value, freq):
        super().__init__(key, value)
        self.freq = freq


class LFUCache(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        # 保存缓存值
        self.map = {}
        # 保存频率链表
        self.freq_map = {}

    # 更新节点频率
    def _freq_node(self, node):
        freq = node.freq
        if freq > 0:
            l = self.freq_map[freq]
            l.remove(node)
            if l.size == 0:
                del self.freq_map[freq]
        node.freq = freq + 1
        if not freq + 1 in self.freq_map:
            l = DoubleLinkedList()
            self.freq_map[node.freq] = l
        self.freq_map[node.freq].append(node)

    def _remove_freq_node(self):
        freq = min(self.freq_map)
        l = self.freq_map[freq]
        node = l.pop()
        if l.size == 0:
            del self.freq_map[freq]
        return node

    def get(self, key):
        if key in self.map:
            node = self.map[key]
            self._freq_node(node)
            return node.value
        return -1

    def put(self, key, value):
        if self.capacity == 0:
            return
        if key in self.map:
            node = self.map[key]
            self._freq_node(node)
            self.map[key] = node
        else:
            if self.capacity == self.size:
                node = self._remove_freq_node()
                del self.map[node.key]
                self.size -= 1
            node = LFUNode(key, value, 0)
            self._freq_node(node)
            self.map[key] = node
            self.size += 1

    def print(self):
        for k, v in self.freq_map.items():
            print('freq = %d | v = ' % k, end='')
            v.print()
        print()


if __name__ == '__main__':
    cache = LFUCache(2)
    cache.put(1, 1)
    cache.print()
    cache.put(2, 2)
    cache.print()
    print(cache.get(1))
    cache.print()
    cache.put(3, 3)
    cache.print()
    print(cache.get(2))
    cache.print()
    print(cache.get(3))
    cache.print()
    cache.put(4, 4)
    cache.print()
    print(cache.get(1))
    cache.print()
    print(cache.get(3))
    cache.print()
    print(cache.get(4))
    cache.print()
