from typing import TypeVar, Optional, List, Tuple
import random
from zip_tree import ZipTree

KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')

class SkipListNode:
    def __init__(self, key: KeyType, val: ValType, level: int):
        self.key = key
        self.val = val
        # Array to hold references to node of different levels
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self):
        self.max_level = 20  # Maximum level for this skip list
        self.head = SkipListNode(None, None, self.max_level)  # header node
        self.level = 0  # Current level of skip list

    def get_random_level(self, key: KeyType) -> int:
        random.seed(str(key))
        level = 0
        while random.random() < 0.5 and level < self.max_level:
            level += 1
        return level

    def insert(self, key: KeyType, val: ValType):
        update = [None] * (self.max_level + 1)
        current = self.head
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current is None or current.key != key:
            new_level = self.get_random_level(key)
            if new_level > self.level:
                for i in range(self.level + 1, new_level + 1):
                    update[i] = self.head
                self.level = new_level

            new_node = SkipListNode(key, val, new_level)
            for i in range(new_level + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node

    def remove(self, key: KeyType):
        update = [None] * (self.level + 1)
        current = self.head
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]
        if current and current.key == key:
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]

            while self.level > 0 and self.head.forward[self.level] is None:
                self.level -= 1

    def find(self, key: KeyType) -> Optional[ValType]:
        current = self.head
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]
        if current and current.key == key:
            return current.val
        return None

    def get_list_size_at_level(self, level: int) -> int:
        if level > self.level:
            return 0
        size = 0
        node = self.head.forward[level]
        while node:
            size += 1
            node = node.forward[level]
        return size

    def from_zip_tree(self, zip_tree: ZipTree) -> None:
        # Implementation depends on traversal of the ZipTree and using the insert method here
        pass
