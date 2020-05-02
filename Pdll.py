#!/usr/bin/env python3

"""filename: Pdll.py for Doubly linked list"""
#Author name: Prathamesh Pawar
#       email: prathameshpawar1301@gmail.com

##################################################################################################################
# supporting meathods
##  isEmpty
##  size
##  search
##  addFront
##  remove
##################################################################################################################
"""Importing Node class from Pnode file"""
from Pnode import *

class DLL:

    def __init__(self):
        self.head = None

    def __repr__(self):
        return "The node data is: data = {}".format(self.data)

    def isEmpty(self):
        return self.head is None

    def size(self):
        size = 0

        if self.head is None:
            return 0
        
        current = self.head
        while current is not None:
            size += 1
            current =  current.getNext()

        return size

    def search(self, data):
        if self.head is None:
            return "Empty List. No Nodes exist to search from."

        current =  self.head
        while current is not None:
            if current.getData() == data:
                return True
            else:
                current =  current.getNext()
                
        return False

    def addFront(self, new_data):

        temp = Node(new_data)
        temp.setNext(self.head)

        if self.head is not  None:
            self.head.setPrev(temp)

        self.head = temp

    def remove(self, data):

        if self.head is None:
            return "Empty list: No nodes to remove"

        current = self.head
        found = False

        while not found:
            if current.getData() == data:
                found = True
            else:
                if current.getNext() is None:
                    return "No node contains provided data. No node is removed"
                else:
                    current = current.getNext()

        if current.getPrev() is None:
            self.head = current.getNext()
        else:
            current.prev.setNext(current.getNext())
            current.next.setPrev(current.getPrev())
