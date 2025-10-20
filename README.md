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
