#!/etc/bin/env python3
"""Filename: Pstack"""

#Auther Name: Prathamesh Pawar
#       Email: prathameshpawar1301@gmail.com

"""This is Stack class"""

class Pstack:

    def __init__(self):
        self.items = []

    def push(self, item):

        self.items.append(item)

    def pop(self):

        if self.items:
            return self.items.pop()


    def peek(self):

        return self.items[-1]


    def size(self):

        return len(self.items)

    def isEmpty(self):

        return self.items == []
