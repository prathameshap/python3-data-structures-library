#!/usr/bin/env python3
"""
Binary Search Tree Utilities and Helper Functions
"""

# Author Name: Prathamesh Pawar
# Email: prathameshpawar1301@gmail.com

import random
import time
from typing import List, Tuple, Any

class BSTUtils:
    """
    Utility class for Binary Search Tree operations and analysis
    """
    
    @staticmethod
    def generate_random_data(size: int, min_val: int = 1, max_val: int = 1000) -> List[int]:
        """Generate random data for BST testing"""
        return [random.randint(min_val, max_val) for _ in range(size)]
    
    @staticmethod
    def generate_sorted_data(size: int, start: int = 1) -> List[int]:
        """Generate sorted data for BST testing"""
        return list(range(start, start + size))
    
    @staticmethod
    def generate_reverse_sorted_data(size: int, start: int = 1000) -> List[int]:
        """Generate reverse sorted data for BST testing"""
        return list(range(start, start - size, -1))
    
    @staticmethod
    def measure_insertion_time(tree_class, data: List[int]) -> Tuple[float, int]:
        """Measure time taken to insert data into BST"""
        tree = tree_class()
        start_time = time.time()
        
        for item in data:
            tree.insert(item)
        
        end_time = time.time()
        return end_time - start_time, len(tree)
    
    @staticmethod
    def measure_search_time(tree, search_data: List[int]) -> Tuple[float, int]:
        """Measure time taken to search data in BST"""
        start_time = time.time()
        found_count = 0
        
        for item in search_data:
            if tree.search(item):
                found_count += 1
        
        end_time = time.time()
        return end_time - start_time, found_count
    
    @staticmethod
    def measure_deletion_time(tree, delete_data: List[int]) -> Tuple[float, int]:
        """Measure time taken to delete data from BST"""
        start_time = time.time()
        deleted_count = 0
        
        for item in delete_data:
            if tree.delete(item):
                deleted_count += 1
        
        end_time = time.time()
        return end_time - start_time, deleted_count
    
    @staticmethod
    def analyze_tree_performance(tree_class, data_sizes: List[int]) -> dict:
        """Analyze BST performance across different data sizes"""
        results = {
            'insertion_times': [],
            'search_times': [],
            'deletion_times': [],
            'heights': [],
            'node_counts': []
        }
        
        for size in data_sizes:
            # Generate random data
            random_data = BSTUtils.generate_random_data(size)
            
            # Measure insertion
            tree = tree_class()
            insert_time, node_count = BSTUtils.measure_insertion_time(tree_class, random_data)
            results['insertion_times'].append(insert_time)
            results['node_counts'].append(node_count)
            results['heights'].append(tree.height())
            
            # Measure search
            search_time, found_count = BSTUtils.measure_search_time(tree, random_data[:size//2])
            results['search_times'].append(search_time)
            
            # Measure deletion
            delete_time, deleted_count = BSTUtils.measure_deletion_time(tree, random_data[:size//4])
            results['deletion_times'].append(delete_time)
        
        return results
    
    @staticmethod
    def compare_tree_types(data: List[int]) -> dict:
        """Compare performance of different BST implementations"""
        from basic_bst import BinarySearchTree
        from splay_tree import SplayTree
        from red_black_tree import RedBlackTree
        
        trees = {
            'Basic BST': BinarySearchTree,
            'Splay Tree': SplayTree,
            'Red-Black Tree': RedBlackTree
        }
        
        results = {}
        
        for name, tree_class in trees.items():
            tree = tree_class()
            
            # Insert data
            insert_start = time.time()
            for item in data:
                tree.insert(item)
            insert_time = time.time() - insert_start
            
            # Search data
            search_start = time.time()
            for item in data[:len(data)//2]:
                tree.search(item)
            search_time = time.time() - search_start
            
            # Get statistics
            stats = tree.get_tree_statistics() if hasattr(tree, 'get_tree_statistics') else {
                'height': tree.height(),
                'total_nodes': len(tree)
            }
            
            results[name] = {
                'insert_time': insert_time,
                'search_time': search_time,
                'height': stats.get('height', 0),
                'nodes': stats.get('total_nodes', len(tree)),
                'is_balanced': stats.get('is_balanced', False) if 'is_balanced' in stats else None
            }
        
        return results
    
    @staticmethod
    def validate_bst_property(tree) -> bool:
        """Validate that tree maintains BST property"""
        return tree.is_valid_bst() if hasattr(tree, 'is_valid_bst') else BSTUtils._validate_bst_recursive(tree.root)
    
    @staticmethod
    def _validate_bst_recursive(node, min_val=float('-inf'), max_val=float('inf')):
        """Recursive helper to validate BST property"""
        if node is None:
            return True
        
        if node.get_data() <= min_val or node.get_data() >= max_val:
            return False
        
        return (BSTUtils._validate_bst_recursive(node.get_left(), min_val, node.get_data()) and
                BSTUtils._validate_bst_recursive(node.get_right(), node.get_data(), max_val))
    
    @staticmethod
    def find_common_ancestor(tree, val1: int, val2: int) -> Any:
        """Find lowest common ancestor of two values in BST"""
        if not tree.root:
            return None
        
        current = tree.root
        while current:
            if val1 < current.get_data() and val2 < current.get_data():
                current = current.get_left()
            elif val1 > current.get_data() and val2 > current.get_data():
                current = current.get_right()
            else:
                return current.get_data()
        
        return None
    
    @staticmethod
    def find_kth_smallest(tree, k: int) -> Any:
        """Find kth smallest element in BST"""
        if k <= 0 or k > len(tree):
            return None
        
        inorder_list = tree.inorder_traversal()
        return inorder_list[k-1] if k <= len(inorder_list) else None
    
    @staticmethod
    def find_kth_largest(tree, k: int) -> Any:
        """Find kth largest element in BST"""
        if k <= 0 or k > len(tree):
            return None
        
        reverse_inorder_list = tree.reverse_inorder_traversal() if hasattr(tree, 'reverse_inorder_traversal') else tree.inorder_traversal()[::-1]
        return reverse_inorder_list[k-1] if k <= len(reverse_inorder_list) else None
    
    @staticmethod
    def find_range_sum(tree, low: int, high: int) -> int:
        """Find sum of all values in range [low, high]"""
        inorder_list = tree.inorder_traversal()
        return sum(val for val in inorder_list if low <= val <= high)
    
    @staticmethod
    def find_closest_value(tree, target: int) -> Any:
        """Find value closest to target in BST"""
        if not tree.root:
            return None
        
        closest = tree.root.get_data()
        current = tree.root
        
        while current:
            if abs(current.get_data() - target) < abs(closest - target):
                closest = current.get_data()
            
            if target < current.get_data():
                current = current.get_left()
            elif target > current.get_data():
                current = current.get_right()
            else:
                return current.get_data()
        
        return closest
    
    @staticmethod
    def serialize_tree(tree) -> List[Any]:
        """Serialize BST to list (level-order)"""
        if not tree.root:
            return []
        
        result = []
        queue = [tree.root]
        
        while queue:
            node = queue.pop(0)
            if node:
                result.append(node.get_data())
                queue.append(node.get_left())
                queue.append(node.get_right())
            else:
                result.append(None)
        
        # Remove trailing None values
        while result and result[-1] is None:
            result.pop()
        
        return result
    
    @staticmethod
    def deserialize_tree(tree_class, data: List[Any]):
        """Deserialize list to BST"""
        if not data:
            return tree_class()
        
        tree = tree_class()
        for item in data:
            if item is not None:
                tree.insert(item)
        
        return tree
    
    @staticmethod
    def merge_trees(tree1, tree2) -> Any:
        """Merge two BSTs into one"""
        if not tree1.root and not tree2.root:
            return tree1.__class__()
        
        # Get all values from both trees
        values1 = tree1.inorder_traversal() if tree1.root else []
        values2 = tree2.inorder_traversal() if tree2.root else []
        
        # Merge and sort values
        merged_values = sorted(values1 + values2)
        
        # Create new tree
        new_tree = tree1.__class__()
        for value in merged_values:
            new_tree.insert(value)
        
        return new_tree
    
    @staticmethod
    def split_tree(tree, value: int) -> Tuple[Any, Any]:
        """Split BST into two trees based on value"""
        if not tree.root:
            return tree.__class__(), tree.__class__()
        
        left_values = []
        right_values = []
        
        inorder_list = tree.inorder_traversal()
        for val in inorder_list:
            if val < value:
                left_values.append(val)
            elif val > value:
                right_values.append(val)
        
        # Create new trees
        left_tree = tree.__class__()
        right_tree = tree.__class__()
        
        for val in left_values:
            left_tree.insert(val)
        for val in right_values:
            right_tree.insert(val)
        
        return left_tree, right_tree
    
    @staticmethod
    def print_performance_report(results: dict):
        """Print formatted performance report"""
        print("BST Performance Analysis Report")
        print("=" * 50)
        
        for tree_name, metrics in results.items():
            print(f"\n{tree_name}:")
            print(f"  Insert Time: {metrics['insert_time']:.6f}s")
            print(f"  Search Time: {metrics['search_time']:.6f}s")
            print(f"  Height: {metrics['height']}")
            print(f"  Nodes: {metrics['nodes']}")
            if metrics['is_balanced'] is not None:
                print(f"  Balanced: {metrics['is_balanced']}")
    
    @staticmethod
    def generate_tree_visualization_data(tree) -> dict:
        """Generate data for tree visualization"""
        if not tree.root:
            return {'nodes': [], 'edges': []}
        
        nodes = []
        edges = []
        
        def traverse(node, parent_id=None):
            if node:
                node_id = id(node)
                nodes.append({
                    'id': node_id,
                    'data': node.get_data(),
                    'color': getattr(node, 'get_color', lambda: 'black')() if hasattr(node, 'get_color') else 'black'
                })
                
                if parent_id:
                    edges.append({'from': parent_id, 'to': node_id})
                
                if node.get_left():
                    traverse(node.get_left(), node_id)
                if node.get_right():
                    traverse(node.get_right(), node_id)
        
        traverse(tree.root)
        return {'nodes': nodes, 'edges': edges}
