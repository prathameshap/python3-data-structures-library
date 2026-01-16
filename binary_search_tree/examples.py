#!/usr/bin/env python3
"""
Comprehensive Binary Search Tree Examples and Demonstrations
"""
# Author Name: Prathamesh Pawar
# Email: prathameshpawar1301@gmail.com

from basic_bst import BinarySearchTree
from threaded_bst import ThreadedBinarySearchTree
from splay_tree import SplayTree
from red_black_tree import RedBlackTree
from bst_utils import BSTUtils

def demonstrate_basic_bst():
    """Demonstrate Basic Binary Search Tree operations"""
    print("=== Basic Binary Search Tree Demo ===")
    bst = BinarySearchTree()
    
    # Insert elements
    elements = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    print(f"Inserting elements: {elements}")
    
    for elem in elements:
        bst.insert(elem)
    
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
    
    # Tree statistics
    stats = bst.get_tree_statistics()
    print(f"Tree statistics: {stats}")
    
    # Display tree
    bst.display_tree()
    print()

def demonstrate_threaded_bst():
    """Demonstrate Threaded Binary Search Tree operations"""
    print("=== Threaded Binary Search Tree Demo ===")
    threaded_bst = ThreadedBinarySearchTree()
    
    # Insert elements
    elements = [50, 30, 70, 20, 40, 60, 80]
    print(f"Inserting elements: {elements}")
    
    for elem in elements:
        threaded_bst.insert(elem)
    
    print(f"Tree size: {len(threaded_bst)}")
    print(f"Tree height: {threaded_bst.height()}")
    print(f"Min value: {threaded_bst.find_min()}")
    print(f"Max value: {threaded_bst.find_max()}")
    
    # Thread-based traversals
    print(f"Inorder traversal (using threads): {threaded_bst.inorder_traversal()}")
    print(f"Reverse inorder traversal (using threads): {threaded_bst.reverse_inorder_traversal()}")
    
    # Search operations
    print(f"Search 40: {threaded_bst.search(40)}")
    print(f"Search 90: {threaded_bst.search(90)}")
    
    # Display tree
    threaded_bst.display_tree()
    print()

def demonstrate_splay_tree():
    """Demonstrate Splay Tree operations"""
    print("=== Splay Tree Demo ===")
    splay_tree = SplayTree()
    
    # Insert elements
    elements = [50, 30, 70, 20, 40, 60, 80]
    print(f"Inserting elements: {elements}")
    
    for elem in elements:
        splay_tree.insert(elem)
        print(f"After inserting {elem}, root is: {splay_tree.root.get_data()}")
    
    print(f"Tree size: {len(splay_tree)}")
    print(f"Tree height: {splay_tree.height()}")
    
    # Search operations (will splay accessed nodes to root)
    print(f"Search 40: {splay_tree.search(40)}")
    print(f"After searching 40, root is: {splay_tree.root.get_data()}")
    
    print(f"Search 20: {splay_tree.search(20)}")
    print(f"After searching 20, root is: {splay_tree.root.get_data()}")
    
    # Find min/max (will splay to root)
    print(f"Find min: {splay_tree.find_min()}")
    print(f"After finding min, root is: {splay_tree.root.get_data()}")
    
    print(f"Find max: {splay_tree.find_max()}")
    print(f"After finding max, root is: {splay_tree.root.get_data()}")
    
    # Traversals
    print(f"Inorder traversal: {splay_tree.inorder_traversal()}")
    
    # Display tree
    splay_tree.display_tree()
    print()

def demonstrate_red_black_tree():
    """Demonstrate Red-Black Tree operations"""
    print("=== Red-Black Tree Demo ===")
    rb_tree = RedBlackTree()
    
    # Insert elements
    elements = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    print(f"Inserting elements: {elements}")
    
    for elem in elements:
        rb_tree.insert(elem)
        print(f"After inserting {elem}, root is: {rb_tree.root.get_data()} ({rb_tree.root.get_color()})")
    
    print(f"Tree size: {len(rb_tree)}")
    print(f"Tree height: {rb_tree.height()}")
    print(f"Black height: {rb_tree.black_height()}")
    print(f"Min value: {rb_tree.find_min()}")
    print(f"Max value: {rb_tree.find_max()}")
    
    # Validate Red-Black properties
    print(f"Is valid Red-Black tree: {rb_tree.is_valid_red_black_tree()}")
    
    # Search operations
    print(f"Search 40: {rb_tree.search(40)}")
    print(f"Search 90: {rb_tree.search(90)}")
    
    # Traversals
    print(f"Inorder traversal: {rb_tree.inorder_traversal()}")
    
    # Tree statistics
    stats = rb_tree.get_tree_statistics()
    print(f"Tree statistics: {stats}")
    
    # Display tree
    rb_tree.display_tree()
    print()

def demonstrate_performance_comparison():
    """Demonstrate performance comparison between different BST types"""
    print("=== Performance Comparison Demo ===")
    
    # Generate test data
    test_data = BSTUtils.generate_random_data(1000)
    
    print("Comparing BST implementations with 1000 random elements:")
    print("-" * 60)
    
    # Compare different tree types
    results = BSTUtils.compare_tree_types(test_data)
    BSTUtils.print_performance_report(results)
    print()

def demonstrate_utility_functions():
    """Demonstrate BST utility functions"""
    print("=== BST Utility Functions Demo ===")
    
    # Create a BST
    bst = BinarySearchTree()
    elements = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    for elem in elements:
        bst.insert(elem)
    
    print(f"BST with elements: {bst.inorder_traversal()}")
    
    # Find kth smallest/largest
    print(f"3rd smallest: {BSTUtils.find_kth_smallest(bst, 3)}")
    print(f"3rd largest: {BSTUtils.find_kth_largest(bst, 3)}")
    
    # Find range sum
    print(f"Sum of values in range [25, 60]: {BSTUtils.find_range_sum(bst, 25, 60)}")
    
    # Find closest value
    print(f"Closest value to 33: {BSTUtils.find_closest_value(bst, 33)}")
    print(f"Closest value to 55: {BSTUtils.find_closest_value(bst, 55)}")
    
    # Find common ancestor
    print(f"Common ancestor of 20 and 40: {BSTUtils.find_common_ancestor(bst, 20, 40)}")
    print(f"Common ancestor of 10 and 25: {BSTUtils.find_common_ancestor(bst, 10, 25)}")
    
    # Serialize and deserialize
    serialized = BSTUtils.serialize_tree(bst)
    print(f"Serialized tree: {serialized}")
    
    new_bst = BSTUtils.deserialize_tree(BinarySearchTree, serialized)
    print(f"Deserialized tree inorder: {new_bst.inorder_traversal()}")
    
    # Tree visualization data
    viz_data = BSTUtils.generate_tree_visualization_data(bst)
    print(f"Visualization data - Nodes: {len(viz_data['nodes'])}, Edges: {len(viz_data['edges'])}")
    print()

def demonstrate_tree_operations():
    """Demonstrate advanced tree operations"""
    print("=== Advanced Tree Operations Demo ===")
    
    # Create two BSTs
    bst1 = BinarySearchTree()
    bst2 = BinarySearchTree()
    
    elements1 = [50, 30, 70, 20, 40]
    elements2 = [60, 80, 10, 25, 35]
    
    for elem in elements1:
        bst1.insert(elem)
    for elem in elements2:
        bst2.insert(elem)
    
    print(f"BST1: {bst1.inorder_traversal()}")
    print(f"BST2: {bst2.inorder_traversal()}")
    
    # Merge trees
    merged_tree = BSTUtils.merge_trees(bst1, bst2)
    print(f"Merged tree: {merged_tree.inorder_traversal()}")
    
    # Split tree
    left_tree, right_tree = BSTUtils.split_tree(merged_tree, 40)
    print(f"Left tree (values < 40): {left_tree.inorder_traversal()}")
    print(f"Right tree (values > 40): {right_tree.inorder_traversal()}")
    print()

def demonstrate_edge_cases():
    """Demonstrate edge cases and error handling"""
    print("=== Edge Cases Demo ===")
    
    # Empty tree
    empty_bst = BinarySearchTree()
    print(f"Empty tree size: {len(empty_bst)}")
    print(f"Empty tree height: {empty_bst.height()}")
    print(f"Empty tree min: {empty_bst.find_min()}")
    print(f"Empty tree max: {empty_bst.find_max()}")
    print(f"Empty tree search: {empty_bst.search(10)}")
    
    # Single node tree
    single_bst = BinarySearchTree()
    single_bst.insert(42)
    print(f"Single node tree: {single_bst.inorder_traversal()}")
    print(f"Single node tree height: {single_bst.height()}")
    
    # Duplicate values
    duplicate_bst = BinarySearchTree()
    duplicates = [10, 20, 10, 30, 20, 10]
    for elem in duplicates:
        duplicate_bst.insert(elem)
    print(f"Tree with duplicates: {duplicate_bst.inorder_traversal()}")
    print(f"Tree size with duplicates: {len(duplicate_bst)}")
    
    # Delete non-existent element
    print(f"Delete non-existent 100: {duplicate_bst.delete(100)}")
    print(f"Tree after deleting non-existent: {duplicate_bst.inorder_traversal()}")
    print()

def main():
    """Run all demonstrations"""
    print("Binary Search Tree Library - Comprehensive Examples")
    print("=" * 60)
    
    demonstrate_basic_bst()
    demonstrate_threaded_bst()
    demonstrate_splay_tree()
    demonstrate_red_black_tree()
    demonstrate_performance_comparison()
    demonstrate_utility_functions()
    demonstrate_tree_operations()
    demonstrate_edge_cases()
    
    print("All demonstrations completed!")
    print("\nKey Features Demonstrated:")
    print("- Basic BST operations (insert, delete, search, traverse)")
    print("- Threaded BST with efficient inorder traversal")
    print("- Splay Tree with self-adjusting behavior")
    print("- Red-Black Tree with guaranteed balance")
    print("- Performance analysis and comparison")
    print("- Utility functions for advanced operations")
    print("- Tree merging, splitting, and serialization")
    print("- Edge case handling and error management")

if __name__ == "__main__":
    main()
