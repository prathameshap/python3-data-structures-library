#!/usr/bin/env python3
"""
TreeNode class for tree data structures
"""

# Author Name: Prathamesh Pawar
# Email: prathameshpawar1301@gmail.com

class TreeNode:
    """
    TreeNode class for tree data structures
    Supports binary trees, BST, AVL trees, etc.
    """
    
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None
        self.parent = None
        self.height = 1  # For AVL trees
        self.balance = 0  # For AVL trees
    
    def __repr__(self):
        return f"TreeNode(data={self.data}, height={self.height})"
    
    def get_data(self):
        return self.data
    
    def set_data(self, new_data):
        self.data = new_data
    
    def get_left(self):
        return self.left
    
    def set_left(self, new_left):
        self.left = new_left
        if new_left:
            new_left.parent = self
    
    def get_right(self):
        return self.right
    
    def set_right(self, new_right):
        self.right = new_right
        if new_right:
            new_right.parent = self
    
    def get_parent(self):
        return self.parent
    
    def set_parent(self, new_parent):
        self.parent = new_parent
    
    def get_height(self):
        return self.height
    
    def set_height(self, new_height):
        self.height = new_height
    
    def get_balance(self):
        return self.balance
    
    def set_balance(self, new_balance):
        self.balance = new_balance
    
    def is_leaf(self):
        """Check if node is a leaf (no children)"""
        return self.left is None and self.right is None
    
    def has_left_child(self):
        """Check if node has left child"""
        return self.left is not None
    
    def has_right_child(self):
        """Check if node has right child"""
        return self.right is not None
    
    def has_any_children(self):
        """Check if node has any children"""
        return self.left is not None or self.right is not None
    
    def has_both_children(self):
        """Check if node has both children"""
        return self.left is not None and self.right is not None
    
    def update_height(self):
        """Update height based on children heights"""
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        self.height = 1 + max(left_height, right_height)
    
    def update_balance(self):
        """Update balance factor for AVL trees"""
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        self.balance = left_height - right_height
