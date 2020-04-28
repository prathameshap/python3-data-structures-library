#!/usr/bin/env python3
"""This is queue data structure file"""

#Auther Name: Prathamesh Pawar
#       Email: prathameshpawar1301@gmail.com

class Queue:

    def __init__(self):
        self.items = []

    def enqueue(self, item):
        
        self.items.insert(0, item)

    def dequeue(self):
        if self.items:
            return self.items.pop()
        return None

    def peek(self):
        if self.items:
            return self.items[-1]
        return None

    def size(self):
        return len(self.items)

    def isEmpty(self):
        return self.items == []
