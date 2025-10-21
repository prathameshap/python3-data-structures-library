#!/usr/bin/env python3
"""
Basic Binary Search Tree Implementation
"""

# Author Name: Prathamesh Pawar
# Email: prathameshpawar1301@gmail.com

class BSTNode:
    """
    Binary Search Tree Node class
    """
    
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None
        self.parent = None
    
    def __repr__(self):
        return f"BSTNode(data={self.data})"
    
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


class BinarySearchTree:
    """
    Basic Binary Search Tree implementation with comprehensive operations:
    - Insertion, deletion, search
    - All traversal methods
    - Min/max finding
    - Tree validation and analysis
    - Visualization
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
            self.root = BSTNode(data)
            self.size = 1
        else:
            self._insert_recursive(self.root, data)
    
    def _insert_recursive(self, node, data):
        """Recursive helper for insertion"""
        if data < node.get_data():
            if node.get_left() is None:
                node.set_left(BSTNode(data))
                self.size += 1
            else:
                self._insert_recursive(node.get_left(), data)
        elif data > node.get_data():
            if node.get_right() is None:
                node.set_right(BSTNode(data))
                self.size += 1
            else:
                self._insert_recursive(node.get_right(), data)
        # If data == node.data, we don't insert duplicates
    
    def insert_iterative(self, data):
        """Iterative insertion method"""
        if self.root is None:
            self.root = BSTNode(data)
            self.size = 1
            return
        
        current = self.root
        while True:
            if data < current.get_data():
                if current.get_left() is None:
                    current.set_left(BSTNode(data))
                    self.size += 1
                    break
                else:
                    current = current.get_left()
            elif data > current.get_data():
                if current.get_right() is None:
                    current.set_right(BSTNode(data))
                    self.size += 1
                    break
                else:
                    current = current.get_right()
            else:
                # Duplicate value, don't insert
                break
    
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
    
    def search_iterative(self, data):
        """Iterative search method"""
        current = self.root
        while current is not None:
            if data == current.get_data():
                return True
            elif data < current.get_data():
                current = current.get_left()
            else:
                current = current.get_right()
        return False
    
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
            return self._find_node_recursive(node.get_left(), data)
        else:
            return self._find_node_recursive(node.get_right(), data)
    
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
                successor = self._find_min_node(node.get_right())
                node.set_data(successor.get_data())
                node.set_right(self._delete_recursive(node.get_right(), successor.get_data()))
        
        return node
    
    def find_min(self):
        """Find minimum value in the tree"""
        if self.root is None:
            return None
        return self._find_min_node(self.root).get_data()
    
    def _find_min_node(self, node):
        """Find node with minimum value"""
        while node.get_left():
            node = node.get_left()
        return node
    
    def find_max(self):
        """Find maximum value in the tree"""
        if self.root is None:
            return None
        return self._find_max_node(self.root).get_data()
    
    def _find_max_node(self, node):
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
    
    def depth(self, data):
        """Calculate depth of a node with given data"""
        return self._depth_recursive(self.root, data, 0)
    
    def _depth_recursive(self, node, data, current_depth):
        """Recursive helper for depth calculation"""
        if node is None:
            return -1
        if data == node.get_data():
            return current_depth
        elif data < node.get_data():
            return self._depth_recursive(node.get_left(), data, current_depth + 1)
        else:
            return self._depth_recursive(node.get_right(), data, current_depth + 1)
    
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
    
    def reverse_inorder_traversal(self):
        """Reverse inorder traversal: Right -> Root -> Left"""
        result = []
        self._reverse_inorder_recursive(self.root, result)
        return result
    
    def _reverse_inorder_recursive(self, node, result):
        """Recursive helper for reverse inorder traversal"""
        if node:
            self._reverse_inorder_recursive(node.get_right(), result)
            result.append(node.get_data())
            self._reverse_inorder_recursive(node.get_left(), result)
    
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
        return (self._count_leaf_nodes_recursive(node.get_left()) + 
                self._count_leaf_nodes_recursive(node.get_right()))
    
    def count_internal_nodes(self):
        """Count number of internal nodes"""
        return self.size - self.count_leaf_nodes()
    
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
    
    def is_balanced(self):
        """Check if tree is balanced (height difference <= 1)"""
        return self._is_balanced_recursive(self.root) != -1
    
    def _is_balanced_recursive(self, node):
        """Recursive helper to check balance"""
        if node is None:
            return 0
        
        left_height = self._is_balanced_recursive(node.get_left())
        if left_height == -1:
            return -1
        
        right_height = self._is_balanced_recursive(node.get_right())
        if right_height == -1:
            return -1
        
        if abs(left_height - right_height) > 1:
            return -1
        
        return 1 + max(left_height, right_height)
    
    def get_tree_statistics(self):
        """Get comprehensive tree statistics"""
        return {
            'total_nodes': self.size,
            'height': self.height(),
            'leaf_nodes': self.count_leaf_nodes(),
            'internal_nodes': self.count_internal_nodes(),
            'is_valid_bst': self.is_valid_bst(),
            'is_balanced': self.is_balanced(),
            'min_value': self.find_min(),
            'max_value': self.find_max()
        }
    
    def display_tree(self):
        """Display tree structure (simple text representation)"""
        if self.root is None:
            print("Tree is empty")
            return
        
        print("Binary Search Tree structure:")
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
    
    def clear(self):
        """Clear all nodes from the tree"""
        self.root = None
        self.size = 0
