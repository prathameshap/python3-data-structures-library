#!/usr/bin/env python3
"""
Trie (Prefix Tree) Implementation
"""

# Author Name: Prathamesh Pawar
# Email: prathameshpawar1301@gmail.com

class TrieNode:
    """
    TrieNode class for Trie data structure
    Each node represents a character and contains:
    - children: dictionary mapping characters to child nodes
    - is_end_of_word: boolean indicating if this node marks end of a word
    - word_count: number of words that end at this node
    """
    
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.word_count = 0
    
    def __repr__(self):
        return f"TrieNode(is_end={self.is_end_of_word}, count={self.word_count})"


class Trie:
    """
    Trie (Prefix Tree) implementation with:
    - Insertion of words
    - Search for complete words
    - Search for words with given prefix
    - Deletion of words
    - Finding all words with given prefix
    - Word count and statistics
    """
    
    def __init__(self):
        self.root = TrieNode()
        self.total_words = 0
    
    def __len__(self):
        return self.total_words
    
    def is_empty(self):
        """Check if trie is empty"""
        return self.total_words == 0
    
    def insert(self, word):
        """Insert a word into the trie"""
        if not word:
            return
        
        current = self.root
        
        for char in word.lower():
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        
        # Mark end of word and increment count
        if not current.is_end_of_word:
            self.total_words += 1
        current.is_end_of_word = True
        current.word_count += 1
    
    def search(self, word):
        """Search for a complete word in the trie"""
        if not word:
            return False
        
        current = self.root
        
        for char in word.lower():
            if char not in current.children:
                return False
            current = current.children[char]
        
        return current.is_end_of_word
    
    def starts_with(self, prefix):
        """Check if any word in trie starts with given prefix"""
        if not prefix:
            return True
        
        current = self.root
        
        for char in prefix.lower():
            if char not in current.children:
                return False
            current = current.children[char]
        
        return True
    
    def delete(self, word):
        """Delete a word from the trie"""
        if not word or not self.search(word):
            return False
        
        self._delete_recursive(self.root, word.lower(), 0)
        self.total_words -= 1
        return True
    
    def _delete_recursive(self, node, word, index):
        """Recursive helper for deletion"""
        if index == len(word):
            if node.is_end_of_word:
                node.is_end_of_word = False
                node.word_count -= 1
                return node.word_count == 0
            return False
        
        char = word[index]
        if char not in node.children:
            return False
        
        should_delete_child = self._delete_recursive(node.children[char], word, index + 1)
        
        if should_delete_child:
            del node.children[char]
            return len(node.children) == 0 and not node.is_end_of_word
        
        return False
    
    def get_all_words_with_prefix(self, prefix):
        """Get all words that start with given prefix"""
        if not prefix:
            return self.get_all_words()
        
        current = self.root
        
        # Navigate to prefix node
        for char in prefix.lower():
            if char not in current.children:
                return []
            current = current.children[char]
        
        # Collect all words from this node
        words = []
        self._collect_words(current, prefix.lower(), words)
        return words
    
    def get_all_words(self):
        """Get all words in the trie"""
        words = []
        self._collect_words(self.root, "", words)
        return words
    
    def _collect_words(self, node, current_word, words):
        """Recursive helper to collect all words"""
        if node.is_end_of_word:
            words.append(current_word)
        
        for char, child_node in node.children.items():
            self._collect_words(child_node, current_word + char, words)
    
    def get_word_count(self, word):
        """Get count of how many times a word appears"""
        if not word:
            return 0
        
        current = self.root
        
        for char in word.lower():
            if char not in current.children:
                return 0
            current = current.children[char]
        
        return current.word_count if current.is_end_of_word else 0
    
    def longest_common_prefix(self):
        """Find longest common prefix of all words in trie"""
        if self.is_empty():
            return ""
        
        prefix = ""
        current = self.root
        
        # Keep going while there's only one child
        while len(current.children) == 1 and not current.is_end_of_word:
            char = list(current.children.keys())[0]
            prefix += char
            current = current.children[char]
        
        return prefix
    
    def get_words_by_length(self, length):
        """Get all words of specific length"""
        words = []
        self._collect_words_by_length(self.root, "", length, words)
        return words
    
    def _collect_words_by_length(self, node, current_word, target_length, words):
        """Recursive helper to collect words of specific length"""
        if len(current_word) == target_length:
            if node.is_end_of_word:
                words.append(current_word)
            return
        
        if len(current_word) > target_length:
            return
        
        for char, child_node in node.children.items():
            self._collect_words_by_length(child_node, current_word + char, target_length, words)
    
    def autocomplete(self, prefix, max_suggestions=10):
        """Get autocomplete suggestions for given prefix"""
        suggestions = self.get_all_words_with_prefix(prefix)
        return suggestions[:max_suggestions]
    
    def get_statistics(self):
        """Get trie statistics"""
        total_nodes = self._count_nodes(self.root)
        max_depth = self._get_max_depth(self.root)
        
        return {
            'total_words': self.total_words,
            'total_nodes': total_nodes,
            'max_depth': max_depth,
            'average_word_length': self._get_average_word_length()
        }
    
    def _count_nodes(self, node):
        """Count total nodes in trie"""
        count = 1
        for child in node.children.values():
            count += self._count_nodes(child)
        return count
    
    def _get_max_depth(self, node):
        """Get maximum depth of trie"""
        if not node.children:
            return 0
        
        max_child_depth = 0
        for child in node.children.values():
            max_child_depth = max(max_child_depth, self._get_max_depth(child))
        
        return 1 + max_child_depth
    
    def _get_average_word_length(self):
        """Calculate average word length"""
        if self.total_words == 0:
            return 0
        
        total_length = 0
        words = self.get_all_words()
        for word in words:
            total_length += len(word)
        
        return total_length / self.total_words
    
    def display_trie(self):
        """Display trie structure"""
        if self.is_empty():
            print("Trie is empty")
            return
        
        print("Trie structure:")
        self._display_recursive(self.root, "", True)
    
    def _display_recursive(self, node, prefix, is_last):
        """Recursive helper for trie display"""
        if not node.children:
            return
        
        children = list(node.children.items())
        for i, (char, child_node) in enumerate(children):
            is_last_child = (i == len(children) - 1)
            end_marker = " (END)" if child_node.is_end_of_word else ""
            count_marker = f" [{child_node.word_count}]" if child_node.word_count > 1 else ""
            
            print(prefix + ("└── " if is_last_child else "├── ") + 
                  char + end_marker + count_marker)
            
            child_prefix = prefix + ("    " if is_last_child else "│   ")
            self._display_recursive(child_node, child_prefix, is_last_child)
    
    def clear(self):
        """Clear all words from trie"""
        self.root = TrieNode()
        self.total_words = 0
