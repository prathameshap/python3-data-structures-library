#!/usr/bin/env python3

"""ClassName :: Pnode"""

#Auther Name: Prathamesh Pawar 
#       Email: prathameshpawar1301@gmail.com

"""This Class is created as part of User drived data structes 
Namely: Linked List, Stack, Queue and Dequeue"""

class Node:

    def __init__(self, data = None):
        self.data = data
        self.next = None
        self.prev = None

    def getData(self):
        
        return self.data

    def setData(self, new_data):
        
        self.data = new_data

    def getNext(self):
        
        return self.next

    def setNext(self, new_next):

        self.next = new_next

    def getPrev(self):
        
        return self.prev

    def setPrev(self, new_prev):

        self.prev = new_prev
