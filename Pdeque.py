#!/use/bin/env python3
"""This is a Deque class"""

#Auther Name: Prathamesh Pawar
#       Email: prathameshpawar1301@gmail.com


class Deque:

    def __init__(self):

        self.items = []

    def addFront(self, item):
        self.items.insert(0, item)

    def addRear(self, item):
        self.items.append(item)

    def removeRear(self):
        if self.items:
            return self.items.pop()
        return None

    def removeFront(self):
        if self.items:
            return self.items.pop(0)
        return None

    def peekFront(self):
        if self.items:
            return self.items[0]
        return None

    def peekRear(self):
        if self.items:
            return self.items[-1]
        return None

    def size(self):
        return len(self.items)

    def isEmpty(self):
        return self.items == []
