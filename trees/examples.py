#!/usr/bin/env python3
"""
Tree Data Structures Examples and Demonstrations
"""

# Author Name: Prathamesh Pawar
# Email: prathameshpawar1301@gmail.com

from trees import BinarySearchTree, AVLTree, MinHeap, MaxHeap, Trie

def demonstrate_bst():
    """Demonstrate Binary Search Tree operations"""
    print("=== Binary Search Tree Demo ===")
    bst = BinarySearchTree()
    
    # Insert elements
    elements = [50, 30, 70, 20, 40, 60, 80]
    for elem in elements:
        bst.insert(elem)
    
    print(f"Inserted elements: {elements}")
    print(f"Tree size: {len(bst)}")
    print(f"Tree height: {bst.height()}")
    print(f"Min value: {bst.find_min()}")
    print(f"Max value: {bst.find_max()}")
    
    # Traversals
    print(f"Inorder traversal: {bst.inorder_traversal()}")
    print(f"Preorder traversal: {bst.preorder_traversal()}")
    print(f"Postorder traversal: {bst.postorder_traversal()}")
    print(f"Level order traversal: {bst.level_order_traversal()}")
    
    # Search operations
    print(f"Search 40: {bst.search(40)}")
    print(f"Search 90: {bst.search(90)}")
    
    # Display tree
    bst.display_tree()
    print()

def demonstrate_avl():
    """Demonstrate AVL Tree operations"""
    print("=== AVL Tree Demo ===")
    avl = AVLTree()
    
    # Insert elements that would create unbalanced BST
    elements = [10, 20, 30, 40, 50, 25]
    for elem in elements:
        avl.insert(elem)
    
    print(f"Inserted elements: {elements}")
    print(f"Tree size: {len(avl)}")
    print(f"Tree height: {avl.height()}")
    print(f"Is balanced: {avl.is_balanced()}")
    
    # Traversals
    print(f"Inorder traversal: {avl.inorder_traversal()}")
    print(f"Level order traversal: {avl.level_order_traversal()}")
    
    # Display tree with balance factors
    avl.display_tree()
    print()

def demonstrate_heap():
    """Demonstrate Min and Max Heap operations"""
    print("=== Heap Demo ===")
    
    # Min Heap
    print("Min Heap:")
    min_heap = MinHeap()
    elements = [4, 10, 3, 5, 1]
    for elem in elements:
        min_heap.insert(elem)
    
    print(f"Inserted elements: {elements}")
    print(f"Min heap peek: {min_heap.peek()}")
    
    # Extract elements
    print("Extracting elements:")
    while not min_heap.is_empty():
        print(f"Extracted: {min_heap.extract_min()}")
    
    # Max Heap
    print("\nMax Heap:")
    max_heap = MaxHeap()
    for elem in elements:
        max_heap.insert(elem)
    
    print(f"Max heap peek: {max_heap.peek()}")
    
    # Extract elements
    print("Extracting elements:")
    while not max_heap.is_empty():
        print(f"Extracted: {max_heap.extract_max()}")
    
    # Heap Sort
    print(f"\nHeap Sort (Min Heap): {min_heap.heap_sort([4, 10, 3, 5, 1])}")
    print(f"Heap Sort (Max Heap): {max_heap.heap_sort([4, 10, 3, 5, 1])}")
    print()

def demonstrate_trie():
    """Demonstrate Trie operations"""
    print("=== Trie Demo ===")
    trie = Trie()
    
    # Insert words
    words = ["hello", "world", "help", "heaven", "hero", "python", "programming"]
    for word in words:
        trie.insert(word)
    
    print(f"Inserted words: {words}")
    print(f"Total words: {len(trie)}")
    
    # Search operations
    print(f"Search 'hello': {trie.search('hello')}")
    print(f"Search 'help': {trie.search('help')}")
    print(f"Search 'hero': {trie.search('hero')}")
    print(f"Search 'heroes': {trie.search('heroes')}")
    
    # Prefix operations
    print(f"Starts with 'he': {trie.starts_with('he')}")
    print(f"Starts with 'pro': {trie.starts_with('pro')}")
    print(f"Starts with 'xyz': {trie.starts_with('xyz')}")
    
    # Get words with prefix
    print(f"Words with prefix 'he': {trie.get_all_words_with_prefix('he')}")
    print(f"Words with prefix 'pro': {trie.get_all_words_with_prefix('pro')}")
    
    # Autocomplete
    print(f"Autocomplete for 'he' (max 3): {trie.autocomplete('he', 3)}")
    
    # Statistics
    stats = trie.get_statistics()
    print(f"Trie statistics: {stats}")
    
    # Longest common prefix
    print(f"Longest common prefix: '{trie.longest_common_prefix()}'")
    
    # Display trie structure
    trie.display_trie()
    print()

def main():
    """Run all demonstrations"""
    print("Tree Data Structures Library - Examples")
    print("=" * 50)
    
    demonstrate_bst()
    demonstrate_avl()
    demonstrate_heap()
    demonstrate_trie()
    
    print("All demonstrations completed!")

if __name__ == "__main__":
    main()
