# Name: Shuyao Zeng
# OSU Email: zengs@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 4
# Due Date: 07/31/2023
# Description:


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        TODO: Write your implementation
        """
        node = AVLNode(value)
        if self.is_empty():
            self._root = node
        else:
            cur = self._root
            while cur:
                if value < cur.value:
                    if cur.left:
                        cur = cur.left
                    else:
                        cur.left = node
                        node.parent = cur
                        cur = False
                elif value > cur.value:
                    if cur.right:
                        cur = cur.right
                    else:
                        cur.right = node
                        node.parent = cur
                        cur = False
                else:
                    return
            if self.is_valid_avl():
                return
            else:
                while node:
                    self._rebalance(node)
                    node = node.parent

    def remove(self, value: object) -> bool:
        """
        TODO: Write your implementation
        """
        if not self.contains(value):
            return False
        node_changed = AVLNode(0)

        def bfs(root, key):
            nonlocal node_changed
            if not root:
                return root
            if key < root.value:
                root.left = bfs(root.left, key)
            elif key > root.value:
                root.right = bfs(root.right, key)
            else:
                if root.left and root.right:
                    if root.right.left:
                        leftmost = root.right.left
                        while leftmost.left:
                            leftmost = leftmost.left
                        leftmostParent = leftmost.parent
                        node_changed = leftmost
                        if leftmost.right:
                            leftmostParent.left = leftmost.right
                            leftmost.right.parent = leftmostParent
                        else:
                            leftmostParent.left = None
                        root.value = leftmost.value
                    else:
                        root.right.left = root.left
                        root.left.parent = root.right
                        root.right.parent = root.parent
                        root = root.right
                        node_changed = root.left
                elif root.left:
                    root.value = root.left.value
                    node_changed = root.left
                    root.left = None
                elif root.right:
                    root.value = root.right.value
                    node_changed = root.right
                    root.right = None
                else:
                    if not root.parent:
                        self.make_empty()
                    else:
                        node_changed = root
                    root = None
            return root
        self._root = bfs(self.root, value)
        if not node_changed:
            return True
        target = node_changed.parent
        while target:
            self._rebalance(target)
            target = target.parent
        return True


    # Experiment and see if you can use the optional                         #
    # subtree removal methods defined in the BST here in the AVL.            #
    # Call normally using self -> self._remove_no_subtrees(parent, node)     #
    # You need to override the _remove_two_subtrees() method in any case.    #
    # Remove these comments.                                                 #
    # Remove these method stubs if you decide not to use them.               #
    # Change this method in any way you'd like.                              #

    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        TODO: Write your implementation
        """
        pass

    # It's highly recommended to implement                          #
    # the following methods for balancing the AVL Tree.             #
    # Remove these comments.                                        #
    # Remove these method stubs if you decide not to use them.      #
    # Change these methods in any way you'd like.                   #

    def _balance_factor(self, node: AVLNode) -> int:
        """
        TODO: Write your implementation
        """
        return self._get_height(node.right) - self._get_height(node.left)

    def _get_height(self, node: AVLNode) -> int:
        """
        TODO: Write your implementation
        """
        if not node:
            return -1
        return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        TODO: Write your implementation
        """
        temp = node.right
        node.right = temp.left
        if node.right:
            node.right.parent = node
        temp.left = node
        node.parent = temp
        self._update_height(node)
        self._update_height(temp)
        return temp

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        TODO: Write your implementation
        """
        temp = node.left
        node.left = temp.right
        if node.left:
            node.left.parent = node
        temp.right = node
        node.parent = temp
        self._update_height(node)
        self._update_height(temp)
        return temp

    def _update_height(self, node: AVLNode) -> None:
        """
        TODO: Write your implementation
        """
        if node.left and node.right:
            node.height = max(node.left.height, node.right.height) + 1
        elif node.left:
            node.height = node.left.height + 1
        elif node.right:
            node.height = node.right.height + 1
        else:
            node.height = 0

    def _rebalance(self, node: AVLNode) -> None:
        """
        TODO: Write your implementation
        """
        if self._balance_factor(node) == -2:
            if self._balance_factor(node.left) > 0:
                node.left = self._rotate_left(node.left)
                node.left.parent = node
            newParent = node.parent
            newRoot = self._rotate_right(node)
            newRoot.parent = newParent
            if not newParent:
                self.root = newRoot
                newRoot.parent = None
                return
            if newParent.left == node:
                newParent.left = newRoot
            else:
                newParent.right = newRoot
        elif self._balance_factor(node) == 2:
            # the R-L case
            if self._balance_factor(node.right) < 0:
                node.right = self._rotate_right(node.right)
                node.right.parent = node
            newParent = node.parent
            newRoot = self._rotate_left(node)
            newRoot.parent = newParent
            if not newParent:
                self.root = newRoot
                newRoot.parent = None
                return
            if newParent.left == node:
                newParent.left = newRoot
            else:
                newParent.right = newRoot
        else:
            self._update_height(node)

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
