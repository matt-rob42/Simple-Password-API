# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 22:00:19 2020

@author: matt_
"""

## project to build a simple REST API - will store password data and receive/return in JSON format
## There will be a single authenticated user
## data will be stored in a dictionary internally
## implement 4 major HTML commands, maybe the get all
## implement security for each HTML method
## Passwords will have an associated company
## Passwords will have one of five descriptions - API, Website, ITSystem, Database, Superadmin
## We'll use the get all to return the company name and description, plus a unique ID!
## this ID will be what we use to look up a specific password!

from flask import Flask, jsonify
from flask_restful import Resource, Api, request, reqparse
from flask_jwt import JWT, jwt_required

from Security import authenticate, identity # our files

app = Flask(__name__)
app.secret_key = 'Matt' ### important
api = Api(app) 

jwt = JWT(app, authenticate, identity)

passwords = [{"name": "Shell", "User":"matt", "Password": "abc", "Type": "API", "UniqueID": "1" }] # simple in mem DB

class Password(Resource):
    ### !! we put the parser at the class level - so
    ## single PoC
    #parser = reqparse.RequestParser()
    #parser.add_argument('price', type=float, required=True)
        
    
    @jwt_required()
    def get(self, UniqueID):  ##!! This resource can only be accessed with a GET
        password = next(filter(lambda x: x['UniqueID'] == str(UniqueID), passwords), None) # filter returns a filter object!
        #the wrapper next just gets the first item - for our purposes, since items are unique, only 1!
        #None is the default
        return {'password': password}, 200 if password else 404 # this is the failure case, we need it in JSON format!
                                    # the 404 is a status code!
                                    # Nice use of shortened if statement!
    
    def delete(self, UniqueID):
        global passwords # makes it refer to top level variable!
        passwords = list(filter(lambda x: x['UniqueID'] != UniqueID, passwords))
        # problem here is the aliasing/side effects - I
        # don't like this
        return {'message': 'Item Deleted'}
    
    def put(self, UniqueID): # allows us to modify items
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('User', type=str, required=True)
        parser.add_argument('Password', type=str, required=True)
        parser.add_argument('Type', type=str, required=True)
        
        ##this will look at the JSON payload and pull certain
        ## things out - so we can only change price!!!
        ## this is huge - allows us to filter lots of 
        ## nonsense from the json file, and just get what we want
        data = parser.parse_args() # formerly requests.get_json()
        print(data)
        password = next(filter(lambda x : x['UniqueID'] == UniqueID, passwords), None)
        if password is None:
            password = {"name": data['name'], 'User': data["User"], "Password": data['Password'], "Type": data['Type'], "UniqueID": UniqueID}
            passwords.append(password)
        else:
            password.update(data)
        return password
                                    

class PasswordList(Resource): # use this to figure out passwords, then request based on unique ID!
    def get(self):
        passback = [(password["name"], password["Type"], password["UniqueID"]) for password in passwords]
        return {'passwords': passback}
    
api.add_resource(Password, '/password/<string:UniqueID>') 
api.add_resource(PasswordList, '/passwords')
app.run(port=4998) # adding the param debug=True gives us rich errors!

## Some important notes - the adding resources need the name of the class as part of it!
## more important though, the API doesn't take multiple <string:...> constructs,
## just a single one referring to the resource, then the rest are captured as part of the data
## which we collect with the parsing of the JSON post
## PasswordList is a sep. class! Same with any return multiple type things - because it's accessing a 
## different resource!


















































# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 22:00:19 2020

@author: matt_
"""

## project to build a simple REST API - will store password data and receive/return in JSON format
## There will be a single authenticated user
## data will be stored in a dictionary internally
## implement 4 major HTML commands, maybe the get all
## implement security for each HTML method
## Passwords will have an associated company
## Passwords will have one of five descriptions - API, Website, ITSystem, Database, Superadmin

#from flask import Flask, jsonify
#from flask_restful import Resource, Api, request, reqparse
#from flask_jwt import JWT, jwt_required
#
#from Security import authenticate, identity # our files
#
#app = Flask(__name__)
#app.secret_key = 'Matt' ### important
#api = Api(app) 
#
#jwt = JWT(app, authenticate, identity)
#
#passwords = [{"name": "Shell", "User":"matt", "Password": "abc", "Type": "API", "UniqueID": "1" }] # simple in mem DB
#
#class Password(Resource):
#    ### !! we put the parser at the class level - so
#    ## single PoC
#    parser = reqparse.RequestParser()
#    #parser.add_argument('price', type=float, required=True)
#        
#    
#    
#    def get(self, name):  ##!! This resource can only be accessed with a GET
#        password = next(filter(lambda x: x['name'] == name, passwords), None) # filter returns a filter object!
#        #the wrapper next just gets the first item - for our purposes, since items are unique, only 1!
#        #None is the default
#        return {'password': password}, 200 if password else 404 # this is the failure case, we need it in JSON format!
#                                    # the 404 is a status code!
#                                    # Nice use of shortened if statement!
#                                    
#
#class PasswordList(Resource): # use this to figure out passwords, then request based on unique ID!
#    def get(self):
#        passback = [(password["name"], password["Type"], password["UniqueID"]) for password in passwords]
#        return {'passwords': passback}
#    
#api.add_resource(Password, '/password/<string:name>') 
#api.add_resource(PasswordList, '/passwords')
#app.run(port=4998) # adding the param debug=True gives us rich errors!
