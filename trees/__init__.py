#!/usr/bin/env python3
"""
Trees Package - Tree Data Structures Implementation
"""

# Author Name: Prathamesh Pawar
# Email: prathameshpawar1301@gmail.com

from .tree_node import TreeNode
from .binary_search_tree import BinarySearchTree
from .avl_tree import AVLTree
from .heap import MinHeap, MaxHeap
from .trie import Trie, TrieNode

__all__ = [
    'TreeNode',
    'BinarySearchTree', 
    'AVLTree',
    'MinHeap',
    'MaxHeap',
    'Trie',
    'TrieNode'
]

__version__ = "1.0.0"
