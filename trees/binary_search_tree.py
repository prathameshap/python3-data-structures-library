#!/usr/bin/env python3
"""
Binary Search Tree (BST) Implementation
"""

# Author Name: Prathamesh Pawar
# Email: prathameshpawar1301@gmail.com

from tree_node import TreeNode

class BinarySearchTree:
    """
    Binary Search Tree implementation with:
    - Insertion
    - Deletion
    - Search
    - Traversal methods (inorder, preorder, postorder)
    - Finding min/max values
    - Tree height calculation
    """
    
    def __init__(self):
        self.root = None
        self.size = 0
    
    def __len__(self):
        return self.size
    
    def is_empty(self):
        """Check if tree is empty"""
        return self.root is None
    
    def insert(self, data):
        """Insert a new node with given data"""
        if self.root is None:
            self.root = TreeNode(data)
            self.size = 1
        else:
            self._insert_recursive(self.root, data)
    
    def _insert_recursive(self, node, data):
        """Recursive helper for insertion"""
        if data < node.get_data():
            if node.get_left() is None:
                node.set_left(TreeNode(data))
                self.size += 1
            else:
                self._insert_recursive(node.get_left(), data)
        elif data > node.get_data():
            if node.get_right() is None:
                node.set_right(TreeNode(data))
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
            return self._search_recursive(node.get_left(), data)
        else:
            return self._search_recursive(node.get_right(), data)
    
    def delete(self, data):
        """Delete a node with given data"""
        self.root = self._delete_recursive(self.root, data)
    
    def _delete_recursive(self, node, data):
        """Recursive helper for deletion"""
        if node is None:
            return node
        
        if data < node.get_data():
            node.set_left(self._delete_recursive(node.get_left(), data))
        elif data > node.get_data():
            node.set_right(self._delete_recursive(node.get_right(), data))
        else:
            # Node to be deleted found
            self.size -= 1
            
            # Case 1: Node with no children (leaf node)
            if not node.has_any_children():
                return None
            
            # Case 2: Node with one child
            elif not node.has_both_children():
                if node.get_left():
                    return node.get_left()
                else:
                    return node.get_right()
            
            # Case 3: Node with two children
            else:
                # Find inorder successor (smallest in right subtree)
                successor = self._find_min(node.get_right())
                node.set_data(successor.get_data())
                node.set_right(self._delete_recursive(node.get_right(), successor.get_data()))
        
        return node
    
    def find_min(self):
        """Find minimum value in the tree"""
        if self.root is None:
            return None
        return self._find_min(self.root).get_data()
    
    def _find_min(self, node):
        """Find node with minimum value"""
        while node.get_left():
            node = node.get_left()
        return node
    
    def find_max(self):
        """Find maximum value in the tree"""
        if self.root is None:
            return None
        return self._find_max(self.root).get_data()
    
    def _find_max(self, node):
        """Find node with maximum value"""
        while node.get_right():
            node = node.get_right()
        return node
    
    def height(self):
        """Calculate height of the tree"""
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node):
        """Recursive helper for height calculation"""
        if node is None:
            return 0
        return 1 + max(self._height_recursive(node.get_left()), 
                      self._height_recursive(node.get_right()))
    
    def inorder_traversal(self):
        """Inorder traversal: Left -> Root -> Right"""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        """Recursive helper for inorder traversal"""
        if node:
            self._inorder_recursive(node.get_left(), result)
            result.append(node.get_data())
            self._inorder_recursive(node.get_right(), result)
    
    def preorder_traversal(self):
        """Preorder traversal: Root -> Left -> Right"""
        result = []
        self._preorder_recursive(self.root, result)
        return result
    
    def _preorder_recursive(self, node, result):
        """Recursive helper for preorder traversal"""
        if node:
            result.append(node.get_data())
            self._preorder_recursive(node.get_left(), result)
            self._preorder_recursive(node.get_right(), result)
    
    def postorder_traversal(self):
        """Postorder traversal: Left -> Right -> Root"""
        result = []
        self._postorder_recursive(self.root, result)
        return result
    
    def _postorder_recursive(self, node, result):
        """Recursive helper for postorder traversal"""
        if node:
            self._postorder_recursive(node.get_left(), result)
            self._postorder_recursive(node.get_right(), result)
            result.append(node.get_data())
    
    def level_order_traversal(self):
        """Level order traversal (Breadth-First)"""
        if self.root is None:
            return []
        
        result = []
        queue = [self.root]
        
        while queue:
            node = queue.pop(0)
            result.append(node.get_data())
            
            if node.get_left():
                queue.append(node.get_left())
            if node.get_right():
                queue.append(node.get_right())
        
        return result
    
    def count_nodes(self):
        """Count total number of nodes"""
        return self.size
    
    def is_valid_bst(self):
        """Check if the tree is a valid BST"""
        return self._is_valid_bst_recursive(self.root, float('-inf'), float('inf'))
    
    def _is_valid_bst_recursive(self, node, min_val, max_val):
        """Recursive helper to validate BST property"""
        if node is None:
            return True
        
        if node.get_data() <= min_val or node.get_data() >= max_val:
            return False
        
        return (self._is_valid_bst_recursive(node.get_left(), min_val, node.get_data()) and
                self._is_valid_bst_recursive(node.get_right(), node.get_data(), max_val))
    
    def display_tree(self):
        """Display tree structure (simple text representation)"""
        if self.root is None:
            print("Tree is empty")
            return
        
        print("Tree structure:")
        self._display_recursive(self.root, "", True)
    
    def _display_recursive(self, node, prefix, is_last):
        """Recursive helper for tree display"""
        if node is None:
            return
        
        print(prefix + ("└── " if is_last else "├── ") + str(node.get_data()))
        
        children = []
        if node.get_left():
            children.append(node.get_left())
        if node.get_right():
            children.append(node.get_right())
        
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            child_prefix = prefix + ("    " if is_last else "│   ")
            self._display_recursive(child, child_prefix, is_last_child)
