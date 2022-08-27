import warnings

from binary_tree.node import Node


class BinaryTree:
    def __init__(self, head: Node):
        self.head = head

    def add(self, new_node: Node):
        current_node = self.head
        while current_node:
            if new_node.value == current_node.value:
                warnings.warn(f'A node with {current_node.value} value already exists')
                break
            elif new_node.value < current_node.value:
                if current_node.left:
                    current_node = current_node.left
                else:
                    current_node.left = new_node
                    break
            else:
                if current_node.right:
                    current_node = current_node.right
                else:
                    current_node.right = new_node
                    break

    def find(self, value: int):
        current_node = self.head
        while current_node:
            if value == current_node.value:
                return current_node
            elif value > current_node.value:
                current_node = current_node.right
            else:
                current_node = current_node.left
        raise LookupError(f'A node with value {value} was not found.')

    def in_order(self):
        self._in_order_recursive(self.head)

    def _in_order_recursive(self, current_node):
        if not current_node:
            return
        self._in_order_recursive(current_node.left)
        print(current_node)
        self._in_order_recursive(current_node.right)
