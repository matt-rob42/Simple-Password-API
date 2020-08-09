# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 12:14:58 2020

@author: matt_
"""

## better way to store users (as an object)

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password