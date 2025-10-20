#!/usr/bin/env python3
"""
Min/Max Heap Implementation
"""

# Author Name: Prathamesh Pawar
# Email: prathameshpawar1301@gmail.com

class MinHeap:
    """
    Min Heap implementation using array-based representation
    Parent nodes are always smaller than their children
    """
    
    def __init__(self):
        self.heap = []
        self.size = 0
    
    def __len__(self):
        return self.size
    
    def is_empty(self):
        """Check if heap is empty"""
        return self.size == 0
    
    def parent(self, index):
        """Get parent index of given index"""
        return (index - 1) // 2
    
    def left_child(self, index):
        """Get left child index of given index"""
        return 2 * index + 1
    
    def right_child(self, index):
        """Get right child index of given index"""
        return 2 * index + 2
    
    def has_parent(self, index):
        """Check if node has parent"""
        return self.parent(index) >= 0
    
    def has_left_child(self, index):
        """Check if node has left child"""
        return self.left_child(index) < self.size
    
    def has_right_child(self, index):
        """Check if node has right child"""
        return self.right_child(index) < self.size
    
    def swap(self, index1, index2):
        """Swap elements at given indices"""
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]
    
    def peek(self):
        """Get minimum element without removing it"""
        if self.is_empty():
            return None
        return self.heap[0]
    
    def insert(self, data):
        """Insert new element into heap"""
        self.heap.append(data)
        self.size += 1
        self._heapify_up()
    
    def _heapify_up(self):
        """Move element up to maintain heap property"""
        index = self.size - 1
        while self.has_parent(index) and self.heap[self.parent(index)] > self.heap[index]:
            self.swap(self.parent(index), index)
            index = self.parent(index)
    
    def extract_min(self):
        """Remove and return minimum element"""
        if self.is_empty():
            return None
        
        min_element = self.heap[0]
        self.heap[0] = self.heap[self.size - 1]
        self.heap.pop()
        self.size -= 1
        
        if not self.is_empty():
            self._heapify_down()
        
        return min_element
    
    def _heapify_down(self):
        """Move element down to maintain heap property"""
        index = 0
        while self.has_left_child(index):
            smaller_child_index = self.left_child(index)
            
            if self.has_right_child(index) and \
               self.heap[self.right_child(index)] < self.heap[smaller_child_index]:
                smaller_child_index = self.right_child(index)
            
            if self.heap[index] < self.heap[smaller_child_index]:
                break
            else:
                self.swap(index, smaller_child_index)
            
            index = smaller_child_index
    
    def build_heap(self, arr):
        """Build heap from given array"""
        self.heap = arr[:]
        self.size = len(arr)
        
        # Start from last non-leaf node and heapify down
        for i in range(self.parent(self.size - 1), -1, -1):
            self._heapify_down_at_index(i)
    
    def _heapify_down_at_index(self, index):
        """Heapify down from specific index"""
        while self.has_left_child(index):
            smaller_child_index = self.left_child(index)
            
            if self.has_right_child(index) and \
               self.heap[self.right_child(index)] < self.heap[smaller_child_index]:
                smaller_child_index = self.right_child(index)
            
            if self.heap[index] < self.heap[smaller_child_index]:
                break
            else:
                self.swap(index, smaller_child_index)
            
            index = smaller_child_index
    
    def heap_sort(self, arr):
        """Sort array using heap sort algorithm"""
        self.build_heap(arr)
        
        sorted_arr = []
        while not self.is_empty():
            sorted_arr.append(self.extract_min())
        
        return sorted_arr
    
    def display_heap(self):
        """Display heap structure"""
        if self.is_empty():
            print("Heap is empty")
            return
        
        print("Min Heap:", self.heap)
        print("Heap structure:")
        self._display_recursive(0, "", True)
    
    def _display_recursive(self, index, prefix, is_last):
        """Recursive helper for heap display"""
        if index >= self.size:
            return
        
        print(prefix + ("└── " if is_last else "├── ") + str(self.heap[index]))
        
        children = []
        if self.has_left_child(index):
            children.append(self.left_child(index))
        if self.has_right_child(index):
            children.append(self.right_child(index))
        
        for i, child_index in enumerate(children):
            is_last_child = (i == len(children) - 1)
            child_prefix = prefix + ("    " if is_last else "│   ")
            self._display_recursive(child_index, child_prefix, is_last_child)


class MaxHeap:
    """
    Max Heap implementation using array-based representation
    Parent nodes are always larger than their children
    """
    
    def __init__(self):
        self.heap = []
        self.size = 0
    
    def __len__(self):
        return self.size
    
    def is_empty(self):
        """Check if heap is empty"""
        return self.size == 0
    
    def parent(self, index):
        """Get parent index of given index"""
        return (index - 1) // 2
    
    def left_child(self, index):
        """Get left child index of given index"""
        return 2 * index + 1
    
    def right_child(self, index):
        """Get right child index of given index"""
        return 2 * index + 2
    
    def has_parent(self, index):
        """Check if node has parent"""
        return self.parent(index) >= 0
    
    def has_left_child(self, index):
        """Check if node has left child"""
        return self.left_child(index) < self.size
    
    def has_right_child(self, index):
        """Check if node has right child"""
        return self.right_child(index) < self.size
    
    def swap(self, index1, index2):
        """Swap elements at given indices"""
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]
    
    def peek(self):
        """Get maximum element without removing it"""
        if self.is_empty():
            return None
        return self.heap[0]
    
    def insert(self, data):
        """Insert new element into heap"""
        self.heap.append(data)
        self.size += 1
        self._heapify_up()
    
    def _heapify_up(self):
        """Move element up to maintain heap property"""
        index = self.size - 1
        while self.has_parent(index) and self.heap[self.parent(index)] < self.heap[index]:
            self.swap(self.parent(index), index)
            index = self.parent(index)
    
    def extract_max(self):
        """Remove and return maximum element"""
        if self.is_empty():
            return None
        
        max_element = self.heap[0]
        self.heap[0] = self.heap[self.size - 1]
        self.heap.pop()
        self.size -= 1
        
        if not self.is_empty():
            self._heapify_down()
        
        return max_element
    
    def _heapify_down(self):
        """Move element down to maintain heap property"""
        index = 0
        while self.has_left_child(index):
            larger_child_index = self.left_child(index)
            
            if self.has_right_child(index) and \
               self.heap[self.right_child(index)] > self.heap[larger_child_index]:
                larger_child_index = self.right_child(index)
            
            if self.heap[index] > self.heap[larger_child_index]:
                break
            else:
                self.swap(index, larger_child_index)
            
            index = larger_child_index
    
    def build_heap(self, arr):
        """Build heap from given array"""
        self.heap = arr[:]
        self.size = len(arr)
        
        # Start from last non-leaf node and heapify down
        for i in range(self.parent(self.size - 1), -1, -1):
            self._heapify_down_at_index(i)
    
    def _heapify_down_at_index(self, index):
        """Heapify down from specific index"""
        while self.has_left_child(index):
            larger_child_index = self.left_child(index)
            
            if self.has_right_child(index) and \
               self.heap[self.right_child(index)] > self.heap[larger_child_index]:
                larger_child_index = self.right_child(index)
            
            if self.heap[index] > self.heap[larger_child_index]:
                break
            else:
                self.swap(index, larger_child_index)
            
            index = larger_child_index
    
    def heap_sort(self, arr):
        """Sort array using heap sort algorithm"""
        self.build_heap(arr)
        
        sorted_arr = []
        while not self.is_empty():
            sorted_arr.append(self.extract_max())
        
        return sorted_arr
    
    def display_heap(self):
        """Display heap structure"""
        if self.is_empty():
            print("Heap is empty")
            return
        
        print("Max Heap:", self.heap)
        print("Heap structure:")
        self._display_recursive(0, "", True)
    
    def _display_recursive(self, index, prefix, is_last):
        """Recursive helper for heap display"""
        if index >= self.size:
            return
        
        print(prefix + ("└── " if is_last else "├── ") + str(self.heap[index]))
        
        children = []
        if self.has_left_child(index):
            children.append(self.left_child(index))
        if self.has_right_child(index):
            children.append(self.right_child(index))
        
        for i, child_index in enumerate(children):
            is_last_child = (i == len(children) - 1)
            child_prefix = prefix + ("    " if is_last else "│   ")
            self._display_recursive(child_index, child_prefix, is_last_child)
