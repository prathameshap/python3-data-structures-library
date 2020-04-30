#!/usr/bin/env python3

"""This file includes sinle linked list class"""

#Author Name: Prathamesh Pawar
#       Email: prathameshpawar1301@gmail.com

"""Including Node class to create and traverse the link list"""
from Pnode import *

class SLL:

    def __init__(self):
        self.head = None

    def __repr__(self):
        return "Node obbject: data = {}".format(self.data)

    def isEmpty(self):
        return self.head is None

    def addFront(self, new_data):
        temp  = Node(new_data)
        temp.setNext(self.head)
        self.head = temp

    def size(self):
        size = 0

        if self.head == None:
            return 0
        
        current = self.head
        while current is not None: #while there are nodes to count
            size += 1
            current = current.getNext()

        return size

    def search(self, data):
        if self.head is None:
            return "Linked List is empty. No Nodes to search."

        current = self.head
        while current is not None:
            if current.getData() == data:
                return True
            else:
                current = current.getNext()
                
        return False

    def remove(self, data):
        if self.head is None:
            return "Empty List, No nodes to remove"

        current =  self.head
        previous = None
        found = False
        while not found:
            if current.getData() == data:
                found = True
            else:
                if current.getNext() == None:
                    return "A node with that value is not present."
                else:
                    previous = current
                    current = current.getNext()

        if previous is None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())
