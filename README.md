# Python3-Data-Structures-Library

A comprehensive collection of data structures and algorithms implemented in Python.

## Basic Data Structures

### Linear Data Structures
- **Stack** (`pstack.py`) - LIFO (Last In, First Out) data structure
- **Queue** (`pqueue.py`) - FIFO (First In, First Out) data structure  
- **Deque** (`pdeque.py`) - Double-ended queue supporting insertion/deletion at both ends
- **Single Linked List** (`psll.py`) - Linear data structure with nodes pointing to next element
- **Doubly Linked List** (`pdll.py`) - Linear data structure with nodes pointing to both next and previous elements
- **Node** (`pnode.py`) - Basic node class for linked list implementations

## Tree Data Structures (`trees/` package)

### Binary Trees
- **Binary Search Tree** (`trees/binary_search_tree.py`) - Self-organizing binary tree with O(log n) search, insert, delete
- **AVL Tree** (`trees/avl_tree.py`) - Self-balancing binary search tree maintaining height balance
- **Min/Max Heap** (`trees/heap.py`) - Complete binary tree maintaining heap property for priority queues
- **Trie** (`trees/trie.py`) - Prefix tree for efficient string operations and autocomplete

### Tree Features
- **TreeNode** (`trees/tree_node.py`) - Enhanced node class for tree structures with height and balance tracking
- Multiple traversal methods (inorder, preorder, postorder, level-order)
- Tree visualization and display functions
- Comprehensive search, insert, and delete operations
- Balance factor calculations and rotations (AVL)
- Heap operations with heapify algorithms
- String prefix matching and autocomplete (Trie)

## Binary Search Tree Variations (`binary_search_tree/` package)

### BST Implementations
- **Basic BST** (`binary_search_tree/basic_bst.py`) - Standard binary search tree with comprehensive operations
- **Threaded BST** (`binary_search_tree/threaded_bst.py`) - BST with threads for efficient inorder traversal
- **Splay Tree** (`binary_search_tree/splay_tree.py`) - Self-adjusting BST that moves accessed elements to root
- **Red-Black Tree** (`binary_search_tree/red_black_tree.py`) - Self-balancing BST with color properties

### BST Features
- **BSTUtils** (`binary_search_tree/bst_utils.py`) - Comprehensive utility functions for BST analysis
- **Examples** (`binary_search_tree/examples.py`) - Detailed demonstrations of all BST implementations
- Performance analysis and comparison tools
- Tree merging, splitting, and serialization
- Advanced operations (kth smallest/largest, range queries, LCA)
- Visualization data generation
- Edge case handling and validation

## Usage Examples

### Basic Data Structures
```python
from pstack import Pstack
from pqueue import Queue
from psll import SLL

# Stack operations
stack = Pstack()
stack.push(1)
stack.push(2)
print(stack.pop())  # 2

# Queue operations  
queue = Queue()
queue.enqueue(1)
queue.enqueue(2)
print(queue.dequeue())  # 1

# Linked List operations
sll = SLL()
sll.addFront(1)
sll.addFront(2)
print(sll.search(1))  # True
```

### Tree Data Structures
```python
from trees import BinarySearchTree, AVLTree, MinHeap, Trie

# Binary Search Tree
bst = BinarySearchTree()
bst.insert(5)
bst.insert(3)
bst.insert(7)
print(bst.inorder_traversal())  # [3, 5, 7]

# AVL Tree (self-balancing)
avl = AVLTree()
avl.insert(1)
avl.insert(2)
avl.insert(3)
print(avl.is_balanced())  # True

# Min Heap
min_heap = MinHeap()
min_heap.insert(3)
min_heap.insert(1)
min_heap.insert(4)
print(min_heap.extract_min())  # 1

# Trie for string operations
trie = Trie()
trie.insert("hello")
trie.insert("world")
print(trie.search("hello"))  # True
print(trie.starts_with("hel"))  # True
```

### Binary Search Tree Variations
```python
from binary_search_tree import BinarySearchTree, ThreadedBinarySearchTree, SplayTree, RedBlackTree, BSTUtils

# Basic BST
bst = BinarySearchTree()
bst.insert(50)
bst.insert(30)
bst.insert(70)
print(bst.inorder_traversal())  # [30, 50, 70]

# Threaded BST (efficient inorder traversal)
threaded_bst = ThreadedBinarySearchTree()
threaded_bst.insert(50)
threaded_bst.insert(30)
threaded_bst.insert(70)
print(threaded_bst.inorder_traversal())  # [30, 50, 70]

# Splay Tree (self-adjusting)
splay_tree = SplayTree()
splay_tree.insert(50)
splay_tree.insert(30)
splay_tree.search(30)  # Moves 30 to root
print(splay_tree.root.get_data())  # 30

# Red-Black Tree (self-balancing)
rb_tree = RedBlackTree()
rb_tree.insert(50)
rb_tree.insert(30)
rb_tree.insert(70)
print(rb_tree.is_valid_red_black_tree())  # True

# BST Utilities
print(BSTUtils.find_kth_smallest(bst, 2))  # Find 2nd smallest element
print(BSTUtils.find_range_sum(bst, 25, 75))  # Sum of values in range
print(BSTUtils.find_common_ancestor(bst, 30, 70))  # Lowest common ancestor
```

## Author
**Prathamesh Pawar**  
Email: prathameshpawar1301@gmail.com

## Features
- Clean, well-documented code
- Comprehensive method implementations
- Error handling and edge cases
- Tree visualization capabilities
- Performance optimizations
- Educational examples and use cases
