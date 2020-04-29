# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 05:59:31 2020

@author: AsteriskAmpersand
"""


from collections import deque

class Queue(deque):
    def put(self,item):
        self.append(item)
    def get(self):
        return self.popleft()
    def peek(self):
        return self[0]
    def empty(self):
        return len(self)==0
    
class Stack(deque):
    def put(self,item):
        self.append(item)
    def get(self):
        return self.pop()
    def peek(self):
        return self[-1]
    def empty(self):
        return len(self)==0