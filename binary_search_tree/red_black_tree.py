#!/usr/bin/env python3
"""
Red-Black Tree Implementation
"""

# Author Name: Prathamesh Pawar
# Email: prathameshpawar1301@gmail.com

class RedBlackNode:
    """
    Red-Black Tree Node class
    """
    
    RED = "RED"
    BLACK = "BLACK"
    
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None
        self.parent = None
        self.color = self.RED  # New nodes are red by default
    
    def __repr__(self):
        return f"RedBlackNode(data={self.data}, color={self.color})"
    
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
    
    def get_color(self):
        return self.color
    
    def set_color(self, new_color):
        self.color = new_color
    
    def is_red(self):
        return self.color == self.RED
    
    def is_black(self):
        return self.color == self.BLACK
    
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


class RedBlackTree:
    """
    Red-Black Tree implementation with:
    - Self-balancing binary search tree
    - Red-Black properties maintenance
    - Insertion and deletion with color fixing
    - Rotation operations
    - O(log n) guaranteed operations
    """
    
    def __init__(self):
        self.root = None
        self.size = 0
        # Sentinel node for easier implementation
        self.nil = RedBlackNode()
        self.nil.color = RedBlackNode.BLACK
        self.nil.left = None
        self.nil.right = None
        self.nil.parent = None
    
    def __len__(self):
        return self.size
    
    def is_empty(self):
        """Check if tree is empty"""
        return self.root is None
    
    def insert(self, data):
        """Insert a new node with given data"""
        new_node = RedBlackNode(data)
        new_node.left = self.nil
        new_node.right = self.nil
        
        if self.root is None:
            self.root = new_node
            new_node.color = RedBlackNode.BLACK
            self.size = 1
        else:
            self._insert_recursive(self.root, new_node)
            self._insert_fixup(new_node)
            self.size += 1
    
    def _insert_recursive(self, node, new_node):
        """Recursive helper for insertion"""
        if new_node.get_data() < node.get_data():
            if node.get_left() == self.nil:
                node.set_left(new_node)
                new_node.set_parent(node)
            else:
                self._insert_recursive(node.get_left(), new_node)
        elif new_node.get_data() > node.get_data():
            if node.get_right() == self.nil:
                node.set_right(new_node)
                new_node.set_parent(node)
            else:
                self._insert_recursive(node.get_right(), new_node)
        else:
            # Duplicate value, don't insert
            self.size -= 1
    
    def _insert_fixup(self, node):
        """Fix Red-Black properties after insertion"""
        while node.get_parent() and node.get_parent().is_red():
            parent = node.get_parent()
            grandparent = parent.get_parent()
            
            if parent == grandparent.get_left():
                uncle = grandparent.get_right()
                
                if uncle.is_red():
                    # Case 1: Uncle is red
                    parent.set_color(RedBlackNode.BLACK)
                    uncle.set_color(RedBlackNode.BLACK)
                    grandparent.set_color(RedBlackNode.RED)
                    node = grandparent
                else:
                    if node == parent.get_right():
                        # Case 2: Uncle is black, node is right child
                        node = parent
                        self._left_rotate(node)
                        parent = node.get_parent()
                    
                    # Case 3: Uncle is black, node is left child
                    parent.set_color(RedBlackNode.BLACK)
                    grandparent.set_color(RedBlackNode.RED)
                    self._right_rotate(grandparent)
            else:
                uncle = grandparent.get_left()
                
                if uncle.is_red():
                    # Case 1: Uncle is red
                    parent.set_color(RedBlackNode.BLACK)
                    uncle.set_color(RedBlackNode.BLACK)
                    grandparent.set_color(RedBlackNode.RED)
                    node = grandparent
                else:
                    if node == parent.get_left():
                        # Case 2: Uncle is black, node is left child
                        node = parent
                        self._right_rotate(node)
                        parent = node.get_parent()
                    
                    # Case 3: Uncle is black, node is right child
                    parent.set_color(RedBlackNode.BLACK)
                    grandparent.set_color(RedBlackNode.RED)
                    self._left_rotate(grandparent)
        
        self.root.set_color(RedBlackNode.BLACK)
    
    def search(self, data):
        """Search for a node with given data"""
        return self._search_recursive(self.root, data)
    
    def _search_recursive(self, node, data):
        """Recursive helper for search"""
        if node == self.nil or node is None:
            return False
        if data == node.get_data():
            return True
        elif data < node.get_data():
            return self._search_recursive(node.get_left(), data)
        else:
            return self._search_recursive(node.get_right(), data)
    
    def find_node(self, data):
        """Find and return the node with given data"""
        return self._find_node_recursive(self.root, data)
    
    def _find_node_recursive(self, node, data):
        """Recursive helper to find node"""
        if node == self.nil or node is None:
            return None
        if data == node.get_data():
            return node
        elif data < node.get_data():
            return self._find_node_recursive(node.get_left(), data)
        else:
            return self._find_node_recursive(node.get_right(), data)
    
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
        y = node
        y_original_color = y.get_color()
        
        if node.get_left() == self.nil:
            x = node.get_right()
            self._transplant(node, node.get_right())
        elif node.get_right() == self.nil:
            x = node.get_left()
            self._transplant(node, node.get_left())
        else:
            y = self._find_min_node(node.get_right())
            y_original_color = y.get_color()
            x = y.get_right()
            
            if y.get_parent() == node:
                x.set_parent(y)
            else:
                self._transplant(y, y.get_right())
                y.set_right(node.get_right())
                y.get_right().set_parent(y)
            
            self._transplant(node, y)
            y.set_left(node.get_left())
            y.get_left().set_parent(y)
            y.set_color(node.get_color())
        
        if y_original_color == RedBlackNode.BLACK:
            self._delete_fixup(x)
    
    def _transplant(self, u, v):
        """Replace subtree rooted at u with subtree rooted at v"""
        if u.get_parent() is None:
            self.root = v
        elif u == u.get_parent().get_left():
            u.get_parent().set_left(v)
        else:
            u.get_parent().set_right(v)
        
        if v != self.nil:
            v.set_parent(u.get_parent())
    
    def _delete_fixup(self, node):
        """Fix Red-Black properties after deletion"""
        while node != self.root and node.is_black():
            if node == node.get_parent().get_left():
                sibling = node.get_parent().get_right()
                
                if sibling.is_red():
                    # Case 1: Sibling is red
                    sibling.set_color(RedBlackNode.BLACK)
                    node.get_parent().set_color(RedBlackNode.RED)
                    self._left_rotate(node.get_parent())
                    sibling = node.get_parent().get_right()
                
                if sibling.get_left().is_black() and sibling.get_right().is_black():
                    # Case 2: Sibling and its children are black
                    sibling.set_color(RedBlackNode.RED)
                    node = node.get_parent()
                else:
                    if sibling.get_right().is_black():
                        # Case 3: Sibling's right child is black
                        sibling.get_left().set_color(RedBlackNode.BLACK)
                        sibling.set_color(RedBlackNode.RED)
                        self._right_rotate(sibling)
                        sibling = node.get_parent().get_right()
                    
                    # Case 4: Sibling's right child is red
                    sibling.set_color(node.get_parent().get_color())
                    node.get_parent().set_color(RedBlackNode.BLACK)
                    sibling.get_right().set_color(RedBlackNode.BLACK)
                    self._left_rotate(node.get_parent())
                    node = self.root
            else:
                sibling = node.get_parent().get_left()
                
                if sibling.is_red():
                    # Case 1: Sibling is red
                    sibling.set_color(RedBlackNode.BLACK)
                    node.get_parent().set_color(RedBlackNode.RED)
                    self._right_rotate(node.get_parent())
                    sibling = node.get_parent().get_left()
                
                if sibling.get_right().is_black() and sibling.get_left().is_black():
                    # Case 2: Sibling and its children are black
                    sibling.set_color(RedBlackNode.RED)
                    node = node.get_parent()
                else:
                    if sibling.get_left().is_black():
                        # Case 3: Sibling's left child is black
                        sibling.get_right().set_color(RedBlackNode.BLACK)
                        sibling.set_color(RedBlackNode.RED)
                        self._left_rotate(sibling)
                        sibling = node.get_parent().get_left()
                    
                    # Case 4: Sibling's left child is red
                    sibling.set_color(node.get_parent().get_color())
                    node.get_parent().set_color(RedBlackNode.BLACK)
                    sibling.get_left().set_color(RedBlackNode.BLACK)
                    self._right_rotate(node.get_parent())
                    node = self.root
        
        node.set_color(RedBlackNode.BLACK)
    
    def _left_rotate(self, node):
        """Left rotation around given node"""
        right_child = node.get_right()
        node.set_right(right_child.get_left())
        
        if right_child.get_left() != self.nil:
            right_child.get_left().set_parent(node)
        
        right_child.set_parent(node.get_parent())
        
        if node.get_parent() is None:
            self.root = right_child
        elif node == node.get_parent().get_left():
            node.get_parent().set_left(right_child)
        else:
            node.get_parent().set_right(right_child)
        
        right_child.set_left(node)
        node.set_parent(right_child)
    
    def _right_rotate(self, node):
        """Right rotation around given node"""
        left_child = node.get_left()
        node.set_left(left_child.get_right())
        
        if left_child.get_right() != self.nil:
            left_child.get_right().set_parent(node)
        
        left_child.set_parent(node.get_parent())
        
        if node.get_parent() is None:
            self.root = left_child
        elif node == node.get_parent().get_right():
            node.get_parent().set_right(left_child)
        else:
            node.get_parent().set_left(left_child)
        
        left_child.set_right(node)
        node.set_parent(left_child)
    
    def _find_min_node(self, node):
        """Find node with minimum value"""
        while node.get_left() != self.nil:
            node = node.get_left()
        return node
    
    def _find_max_node(self, node):
        """Find node with maximum value"""
        while node.get_right() != self.nil:
            node = node.get_right()
        return node
    
    def find_min(self):
        """Find minimum value in the tree"""
        if self.root is None:
            return None
        return self._find_min_node(self.root).get_data()
    
    def find_max(self):
        """Find maximum value in the tree"""
        if self.root is None:
            return None
        return self._find_max_node(self.root).get_data()
    
    def height(self):
        """Calculate height of the tree"""
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node):
        """Recursive helper for height calculation"""
        if node == self.nil or node is None:
            return 0
        return 1 + max(self._height_recursive(node.get_left()), 
                      self._height_recursive(node.get_right()))
    
    def black_height(self):
        """Calculate black height of the tree"""
        return self._black_height_recursive(self.root)
    
    def _black_height_recursive(self, node):
        """Recursive helper for black height calculation"""
        if node == self.nil or node is None:
            return 0
        
        left_black_height = self._black_height_recursive(node.get_left())
        right_black_height = self._black_height_recursive(node.get_right())
        
        # Add 1 if current node is black
        current_height = left_black_height
        if node.is_black():
            current_height += 1
        
        return current_height
    
    def inorder_traversal(self):
        """Inorder traversal: Left -> Root -> Right"""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        """Recursive helper for inorder traversal"""
        if node != self.nil and node is not None:
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
        if node != self.nil and node is not None:
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
        if node != self.nil and node is not None:
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
            if node != self.nil:
                result.append(node.get_data())
                
                if node.get_left() != self.nil:
                    queue.append(node.get_left())
                if node.get_right() != self.nil:
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
        if node == self.nil or node is None:
            return 0
        if node.is_leaf():
            return 1
        return (self._count_leaf_nodes_recursive(node.get_left()) + 
                self._count_leaf_nodes_recursive(node.get_right()))
    
    def is_valid_red_black_tree(self):
        """Check if tree satisfies Red-Black properties"""
        if self.root is None:
            return True
        
        # Property 1: Root must be black
        if self.root.is_red():
            return False
        
        # Property 2: All leaves (nil nodes) are black (already satisfied)
        
        # Property 3: Red nodes have black children
        if not self._check_red_children(self.root):
            return False
        
        # Property 4: All paths from root to leaves have same black height
        if not self._check_black_height(self.root):
            return False
        
        return True
    
    def _check_red_children(self, node):
        """Check if red nodes have black children"""
        if node == self.nil or node is None:
            return True
        
        if node.is_red():
            if (node.get_left() != self.nil and node.get_left().is_red()) or \
               (node.get_right() != self.nil and node.get_right().is_red()):
                return False
        
        return (self._check_red_children(node.get_left()) and 
                self._check_red_children(node.get_right()))
    
    def _check_black_height(self, node):
        """Check if all paths have same black height"""
        if node == self.nil or node is None:
            return True
        
        left_black_height = self._get_black_height(node.get_left())
        right_black_height = self._get_black_height(node.get_right())
        
        if left_black_height != right_black_height:
            return False
        
        return (self._check_black_height(node.get_left()) and 
                self._check_black_height(node.get_right()))
    
    def _get_black_height(self, node):
        """Get black height of a subtree"""
        if node == self.nil or node is None:
            return 0
        
        height = self._get_black_height(node.get_left())
        if node.is_black():
            height += 1
        
        return height
    
    def get_tree_statistics(self):
        """Get comprehensive tree statistics"""
        return {
            'total_nodes': self.size,
            'height': self.height(),
            'black_height': self.black_height(),
            'leaf_nodes': self.count_leaf_nodes(),
            'is_valid_rb_tree': self.is_valid_red_black_tree(),
            'root_data': self.root.get_data() if self.root else None,
            'root_color': self.root.get_color() if self.root else None
        }
    
    def display_tree(self):
        """Display tree structure"""
        if self.root is None:
            print("Red-Black Tree is empty")
            return
        
        print("Red-Black Tree structure:")
        self._display_recursive(self.root, "", True)
    
    def _display_recursive(self, node, prefix, is_last):
        """Recursive helper for tree display"""
        if node == self.nil or node is None:
            return
        
        color_info = f" ({node.get_color()})"
        print(prefix + ("└── " if is_last else "├── ") + str(node.get_data()) + color_info)
        
        children = []
        if node.get_left() != self.nil:
            children.append(node.get_left())
        if node.get_right() != self.nil:
            children.append(node.get_right())
        
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            child_prefix = prefix + ("    " if is_last else "│   ")
            self._display_recursive(child, child_prefix, is_last_child)
    
    def clear(self):
        """Clear all nodes from the tree"""
        self.root = None
        self.size = 0
