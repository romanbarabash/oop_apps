from random import randint

from binary_tree.node import Node
from binary_tree.tree import BinaryTree

tree = BinaryTree(Node(13))

for i in range(0, 10):
    tree.add(Node(randint(1, 100)))

tree.in_order()

tree.find(100)
