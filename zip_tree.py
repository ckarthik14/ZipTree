# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file.

import random
from typing import TypeVar, Optional

KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')

class ZipTreeNode:
	def __init__(self, key: KeyType, val: ValType, rank: int):
		self.key = key
		self.val = val
		self.rank = rank
		self.left: ZipTreeNode = None
		self.right: ZipTreeNode = None

class ZipTree:
	def __init__(self):
		self.root = None
		self.size = 0

	@staticmethod
	def get_random_rank() -> int:
		# Geometric distribution simulation with p=0.5 (mean=1)
		rank = 0
		while random.randint(0, 1) == 0:
			rank += 1
		return rank

	def insert(self, key: KeyType, val: ValType, rank: int = -1):
		if rank == -1:
			rank = self.get_random_rank()
		self.root = self._insert_rec(self.root, key, val, rank)
		self.size += 1

	def _insert_rec(self, node, key, val, rank):
		if node is None:
			return ZipTreeNode(key, val, rank)
		if key < node.key:
			node.left = self._insert_rec(node.left, key, val, rank)
			if node.left.rank > node.rank:
				node = self._rotate_right(node)
		elif key > node.key:
			node.right = self._insert_rec(node.right, key, val, rank)
			if node.right.rank > node.rank:
				node = self._rotate_left(node)
		else:  # Update the value if the key already exists
			node.val = val
		return node

	def _rotate_left(self, node):
		new_root = node.right
		node.right = new_root.left
		new_root.left = node
		return new_root

	def _rotate_right(self, node):
		new_root = node.left
		node.left = new_root.right
		new_root.right = node
		return new_root

	def _zip(self, x, y):
		if x == None:
			return y
		if y == None:
			return x
		if x.rank < y.rank:
			y.left = zip(x, y.left)
			return y
		else:
			x.right = zip(x.right , y)
			return x
		
	def _remove(self, key: KeyType, node: ZipTreeNode):
		if node is None:
			return None

		if key == node.key:
			return self._zip(node.left, node.right)
		elif key < node.key:
			if node.left and key == node.left.key:
				node.left = self._zip(node.left.left, node.left.right)
			else:
				node.left = self._remove(key, node.left)
		else:  # key > node.key
			if node.right and key == node.right.key:
				node.right = self._zip(node.right.left, node.right.right)
			else:
				node.right = self._remove(key, node.right)
		return node

	def remove(self, key: KeyType):
		self.root = self._remove(self.root, key)
		if self.root is not None:
			self.size -= 1

	def find(self, key: KeyType) -> ValType:
		node = self.root
		while node is not None:
			if key < node.key:
				node = node.left
			elif key > node.key:
				node = node.right
			else:
				return node.val
		return None  # Or raise an exception if the item does not exist

	def get_size(self) -> int:
		return self.size

	def get_height(self) -> int:
		return self._get_height_rec(self.root)

	def _get_height_rec(self, node):
		if node is None:
			return 0
		return 1 + max(self._get_height_rec(node.left), self._get_height_rec(node.right))

	def get_depth(self, key: KeyType) -> int:
		depth = 0
		node = self.root
		while node is not None:
			if key < node.key:
				node = node.left
				depth += 1
			elif key > node.key:
				node = node.right
				depth += 1
			else:
				return depth
		return -1  # Or raise an exception if the item does not exist