# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 12:00:41 2020

@author: matt_
"""
from user import User

users = [
        
        User(1, 'bob', 'asdf')
        
        ]

username_mapping = {u.username: u for u in users} # set comprehension

userid_mapping = {u.id: u for u in users}


## why? so we don't have to iterate over list many times - different ways to access
## now authenticate user fn:

def authenticate(username, password): # given user and password, select correct username
    user = username_mapping.get(username, None) # default returns None
    if user and user.password == password:
        return user
    

def identity(payload): ## takes a payload (JWT token) and see if we have it
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)

## note that we have avoided iteration!

    