from binary_tree.tree import BinaryTree
from binary_tree.node import Node

tree = BinaryTree(Node(13))
tree.add(Node(1))
tree.add(Node(99))
tree.add(Node(12))
tree.add(Node(0))

tree.in_order()

