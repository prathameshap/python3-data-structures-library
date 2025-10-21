#!/usr/bin/env python3
"""
Splay Tree Implementation
"""

# Author Name: Prathamesh Pawar
# Email: prathameshpawar1301@gmail.com

class SplayNode:
    """
    Splay Tree Node class
    """
    
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None
        self.parent = None
    
    def __repr__(self):
        return f"SplayNode(data={self.data})"
    
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


class SplayTree:
    """
    Splay Tree implementation with:
    - Self-adjusting binary search tree
    - Splaying operations (zig, zag, zig-zig, zag-zag, zig-zag, zag-zig)
    - Amortized O(log n) operations
    - Recently accessed elements move to root
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
        """Insert a new node with given data and splay it to root"""
        if self.root is None:
            self.root = SplayNode(data)
            self.size = 1
        else:
            self._insert_recursive(self.root, data)
    
    def _insert_recursive(self, node, data):
        """Recursive helper for insertion"""
        if data < node.get_data():
            if node.get_left() is None:
                new_node = SplayNode(data)
                node.set_left(new_node)
                self.size += 1
                self._splay(new_node)
            else:
                self._insert_recursive(node.get_left(), data)
        elif data > node.get_data():
            if node.get_right() is None:
                new_node = SplayNode(data)
                node.set_right(new_node)
                self.size += 1
                self._splay(new_node)
            else:
                self._insert_recursive(node.get_right(), data)
        else:
            # Duplicate value, splay existing node
            self._splay(node)
    
    def search(self, data):
        """Search for a node with given data and splay it to root"""
        node = self._search_recursive(self.root, data)
        if node:
            self._splay(node)
            return True
        return False
    
    def _search_recursive(self, node, data):
        """Recursive helper for search"""
        if node is None:
            return None
        if data == node.get_data():
            return node
        elif data < node.get_data():
            if node.get_left() is None:
                return node  # Return closest node for splaying
            return self._search_recursive(node.get_left(), data)
        else:
            if node.get_right() is None:
                return node  # Return closest node for splaying
            return self._search_recursive(node.get_right(), data)
    
    def delete(self, data):
        """Delete a node with given data"""
        if self.root is None:
            return False
        
        # First, search and splay the node to root
        node_to_delete = self._search_recursive(self.root, data)
        if node_to_delete and node_to_delete.get_data() == data:
            self._splay(node_to_delete)
            self._delete_root()
            self.size -= 1
            return True
        return False
    
    def _delete_root(self):
        """Delete the root node"""
        if self.root is None:
            return
        
        if not self.root.has_any_children():
            # Root has no children
            self.root = None
        elif not self.root.has_both_children():
            # Root has one child
            if self.root.get_left():
                self.root = self.root.get_left()
                self.root.set_parent(None)
            else:
                self.root = self.root.get_right()
                self.root.set_parent(None)
        else:
            # Root has two children
            # Find maximum in left subtree
            max_left = self._find_max_node(self.root.get_left())
            self._splay(max_left)
            
            # Attach right subtree to max_left
            max_left.set_right(self.root.get_right())
            if self.root.get_right():
                self.root.get_right().set_parent(max_left)
            
            self.root = max_left
            self.root.set_parent(None)
    
    def _find_max_node(self, node):
        """Find node with maximum value"""
        while node.get_right():
            node = node.get_right()
        return node
    
    def _find_min_node(self, node):
        """Find node with minimum value"""
        while node.get_left():
            node = node.get_left()
        return node
    
    def find_min(self):
        """Find minimum value in the tree"""
        if self.root is None:
            return None
        min_node = self._find_min_node(self.root)
        self._splay(min_node)
        return min_node.get_data()
    
    def find_max(self):
        """Find maximum value in the tree"""
        if self.root is None:
            return None
        max_node = self._find_max_node(self.root)
        self._splay(max_node)
        return max_node.get_data()
    
    def _splay(self, node):
        """Splay the given node to root"""
        while node.get_parent() is not None:
            parent = node.get_parent()
            grandparent = parent.get_parent()
            
            if grandparent is None:
                # Zig or Zag (single rotation)
                if parent.get_left() == node:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            else:
                if grandparent.get_left() == parent and parent.get_left() == node:
                    # Zig-Zig (right-right rotation)
                    self._right_rotate(grandparent)
                    self._right_rotate(parent)
                elif grandparent.get_right() == parent and parent.get_right() == node:
                    # Zag-Zag (left-left rotation)
                    self._left_rotate(grandparent)
                    self._left_rotate(parent)
                elif grandparent.get_left() == parent and parent.get_right() == node:
                    # Zig-Zag (left-right rotation)
                    self._left_rotate(parent)
                    self._right_rotate(grandparent)
                else:
                    # Zag-Zig (right-left rotation)
                    self._right_rotate(parent)
                    self._left_rotate(grandparent)
    
    def _right_rotate(self, node):
        """Right rotation around given node"""
        left_child = node.get_left()
        if left_child is None:
            return
        
        # Update parent connections
        parent = node.get_parent()
        if parent is not None:
            if parent.get_left() == node:
                parent.set_left(left_child)
            else:
                parent.set_right(left_child)
        else:
            self.root = left_child
        
        # Update node's left child
        node.set_left(left_child.get_right())
        
        # Update left_child's right child
        left_child.set_right(node)
    
    def _left_rotate(self, node):
        """Left rotation around given node"""
        right_child = node.get_right()
        if right_child is None:
            return
        
        # Update parent connections
        parent = node.get_parent()
        if parent is not None:
            if parent.get_left() == node:
                parent.set_left(right_child)
            else:
                parent.set_right(right_child)
        else:
            self.root = right_child
        
        # Update node's right child
        node.set_right(right_child.get_left())
        
        # Update right_child's left child
        right_child.set_left(node)
    
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
    
    def get_tree_statistics(self):
        """Get comprehensive tree statistics"""
        return {
            'total_nodes': self.size,
            'height': self.height(),
            'leaf_nodes': self.count_leaf_nodes(),
            'root_data': self.root.get_data() if self.root else None
        }
    
    def display_tree(self):
        """Display tree structure"""
        if self.root is None:
            print("Splay Tree is empty")
            return
        
        print("Splay Tree structure:")
        self._display_recursive(self.root, "", True)
    
    def _display_recursive(self, node, prefix, is_last):
        """Recursive helper for tree display"""
        if node is None:
            return
        
        root_marker = " (ROOT)" if node == self.root else ""
        print(prefix + ("└── " if is_last else "├── ") + str(node.get_data()) + root_marker)
        
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
