#!/usr/bin/env python3
"""
Threaded Binary Search Tree Implementation
"""

# Author Name: Prathamesh Pawar
# Email: prathameshpawar1301@gmail.com

class ThreadedBSTNode:
    """
    Threaded Binary Search Tree Node class
    Uses threads to enable efficient inorder traversal without recursion or stack
    """
    
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None
        self.left_thread = False  # True if left is a thread
        self.right_thread = False  # True if right is a thread
    
    def __repr__(self):
        return f"ThreadedBSTNode(data={self.data}, left_thread={self.left_thread}, right_thread={self.right_thread})"
    
    def get_data(self):
        return self.data
    
    def set_data(self, new_data):
        self.data = new_data
    
    def get_left(self):
        return self.left
    
    def set_left(self, new_left):
        self.left = new_left
    
    def get_right(self):
        return self.right
    
    def set_right(self, new_right):
        self.right = new_right
    
    def is_left_thread(self):
        return self.left_thread
    
    def set_left_thread(self, is_thread):
        self.left_thread = is_thread
    
    def is_right_thread(self):
        return self.right_thread
    
    def set_right_thread(self, is_thread):
        self.right_thread = is_thread
    
    def is_leaf(self):
        """Check if node is a leaf (no children)"""
        return self.left_thread and self.right_thread


class ThreadedBinarySearchTree:
    """
    Threaded Binary Search Tree implementation with:
    - Efficient inorder traversal using threads
    - Insertion and deletion maintaining thread properties
    - Search operations
    - Thread-based inorder predecessor and successor finding
    """
    
    def __init__(self):
        self.root = None
        self.size = 0
        # Dummy header node for easier implementation
        self.header = ThreadedBSTNode()
        self.header.left_thread = True
        self.header.right_thread = False
        self.header.left = self.header
        self.header.right = self.header
    
    def __len__(self):
        return self.size
    
    def is_empty(self):
        """Check if tree is empty"""
        return self.root is None
    
    def insert(self, data):
        """Insert a new node with given data"""
        if self.root is None:
            self.root = ThreadedBSTNode(data)
            self.root.left = self.header
            self.root.right = self.header
            self.root.left_thread = True
            self.root.right_thread = True
            self.header.left = self.root
            self.size = 1
        else:
            self._insert_recursive(self.root, data)
    
    def _insert_recursive(self, node, data):
        """Recursive helper for insertion"""
        if data < node.get_data():
            if node.is_left_thread():
                # Insert as left child
                new_node = ThreadedBSTNode(data)
                new_node.left = node.left
                new_node.right = node
                new_node.left_thread = True
                new_node.right_thread = True
                node.left = new_node
                node.set_left_thread(False)
                self.size += 1
            else:
                self._insert_recursive(node.get_left(), data)
        elif data > node.get_data():
            if node.is_right_thread():
                # Insert as right child
                new_node = ThreadedBSTNode(data)
                new_node.left = node
                new_node.right = node.right
                new_node.left_thread = True
                new_node.right_thread = True
                node.right = new_node
                node.set_right_thread(False)
                self.size += 1
            else:
                self._insert_recursive(node.get_right(), data)
        # If data == node.data, we don't insert duplicates
    
    def search(self, data):
        """Search for a node with given data"""
        return self._search_recursive(self.root, data)
    
    def _search_recursive(self, node, data):
        """Recursive helper for search"""
        if node is None:
            return False
        if data == node.get_data():
            return True
        elif data < node.get_data():
            if node.is_left_thread():
                return False
            return self._search_recursive(node.get_left(), data)
        else:
            if node.is_right_thread():
                return False
            return self._search_recursive(node.get_right(), data)
    
    def find_node(self, data):
        """Find and return the node with given data"""
        return self._find_node_recursive(self.root, data)
    
    def _find_node_recursive(self, node, data):
        """Recursive helper to find node"""
        if node is None:
            return None
        if data == node.get_data():
            return node
        elif data < node.get_data():
            if node.is_left_thread():
                return None
            return self._find_node_recursive(node.get_left(), data)
        else:
            if node.is_right_thread():
                return None
            return self._find_node_recursive(node.get_right(), data)
    
    def inorder_successor(self, node):
        """Find inorder successor of given node"""
        if node.is_right_thread():
            return node.right
        else:
            # Find leftmost node in right subtree
            current = node.right
            while not current.is_left_thread():
                current = current.left
            return current
    
    def inorder_predecessor(self, node):
        """Find inorder predecessor of given node"""
        if node.is_left_thread():
            return node.left
        else:
            # Find rightmost node in left subtree
            current = node.left
            while not current.is_right_thread():
                current = current.right
            return current
    
    def inorder_traversal(self):
        """Efficient inorder traversal using threads"""
        if self.root is None:
            return []
        
        result = []
        current = self.header.left  # Start from leftmost node
        
        while current != self.header:
            result.append(current.get_data())
            current = self.inorder_successor(current)
        
        return result
    
    def reverse_inorder_traversal(self):
        """Reverse inorder traversal using threads"""
        if self.root is None:
            return []
        
        result = []
        current = self.header.right  # Start from rightmost node
        
        while current != self.header:
            result.append(current.get_data())
            current = self.inorder_predecessor(current)
        
        return result
    
    def find_min(self):
        """Find minimum value in the tree"""
        if self.root is None:
            return None
        return self.header.left.get_data()
    
    def find_max(self):
        """Find maximum value in the tree"""
        if self.root is None:
            return None
        return self.header.right.get_data()
    
    def delete(self, data):
        """Delete a node with given data"""
        node_to_delete = self.find_node(data)
        if node_to_delete is None:
            return False
        
        self._delete_node(node_to_delete)
        self.size -= 1
        return True
    
    def _delete_node(self, node):
        """Delete a specific node"""
        if node.is_left_thread() and node.is_right_thread():
            # Case 1: Leaf node
            self._delete_leaf_node(node)
        elif node.is_left_thread() or node.is_right_thread():
            # Case 2: Node with one child
            self._delete_node_with_one_child(node)
        else:
            # Case 3: Node with two children
            self._delete_node_with_two_children(node)
    
    def _delete_leaf_node(self, node):
        """Delete a leaf node"""
        parent = self._find_parent(node)
        
        if parent is None:  # Deleting root
            self.root = None
            self.header.left = self.header
            self.header.right = self.header
        elif parent.left == node:
            parent.left = node.left
            parent.set_left_thread(True)
        else:
            parent.right = node.right
            parent.set_right_thread(True)
    
    def _delete_node_with_one_child(self, node):
        """Delete a node with one child"""
        parent = self._find_parent(node)
        child = node.right if node.is_left_thread() else node.left
        
        if parent is None:  # Deleting root
            self.root = child
            if child.is_left_thread():
                child.left = self.header
            if child.is_right_thread():
                child.right = self.header
        elif parent.left == node:
            parent.left = child
            if child.is_left_thread():
                child.left = node.left
            if child.is_right_thread():
                child.right = node.right
        else:
            parent.right = child
            if child.is_left_thread():
                child.left = node.left
            if child.is_right_thread():
                child.right = node.right
    
    def _delete_node_with_two_children(self, node):
        """Delete a node with two children"""
        successor = self.inorder_successor(node)
        node.set_data(successor.get_data())
        self._delete_node(successor)
    
    def _find_parent(self, node):
        """Find parent of given node"""
        if node == self.root:
            return None
        
        current = self.root
        while current is not None:
            if (current.left == node and not current.is_left_thread()) or \
               (current.right == node and not current.is_right_thread()):
                return current
            
            if node.get_data() < current.get_data():
                if current.is_left_thread():
                    break
                current = current.left
            else:
                if current.is_right_thread():
                    break
                current = current.right
        
        return None
    
    def height(self):
        """Calculate height of the tree"""
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node):
        """Recursive helper for height calculation"""
        if node is None:
            return 0
        
        left_height = 0 if node.is_left_thread() else self._height_recursive(node.get_left())
        right_height = 0 if node.is_right_thread() else self._height_recursive(node.get_right())
        
        return 1 + max(left_height, right_height)
    
    def count_nodes(self):
        """Count total number of nodes"""
        return self.size
    
    def count_leaf_nodes(self):
        """Count number of leaf nodes"""
        return self._count_leaf_nodes_recursive(self.root)
    
    def _count_leaf_nodes_recursive(self, node):
        """Recursive helper to count leaf nodes"""
        if node is None:
            return 0
        if node.is_leaf():
            return 1
        
        left_count = 0 if node.is_left_thread() else self._count_leaf_nodes_recursive(node.get_left())
        right_count = 0 if node.is_right_thread() else self._count_leaf_nodes_recursive(node.get_right())
        
        return left_count + right_count
    
    def display_tree(self):
        """Display tree structure"""
        if self.root is None:
            print("Threaded BST is empty")
            return
        
        print("Threaded Binary Search Tree structure:")
        self._display_recursive(self.root, "", True)
    
    def _display_recursive(self, node, prefix, is_last):
        """Recursive helper for tree display"""
        if node is None:
            return
        
        thread_info = ""
        if node.is_left_thread():
            thread_info += " (L-thread)"
        if node.is_right_thread():
            thread_info += " (R-thread)"
        
        print(prefix + ("└── " if is_last else "├── ") + str(node.get_data()) + thread_info)
        
        children = []
        if not node.is_left_thread() and node.get_left():
            children.append(node.get_left())
        if not node.is_right_thread() and node.get_right():
            children.append(node.get_right())
        
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            child_prefix = prefix + ("    " if is_last else "│   ")
            self._display_recursive(child, child_prefix, is_last_child)
    
    def clear(self):
        """Clear all nodes from the tree"""
        self.root = None
        self.size = 0
        self.header.left = self.header
        self.header.right = self.header
