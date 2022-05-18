from flask import Flask

server = Flask(__name__)

@server.get('/')
def get():
    return 'Hello World'

@server.get('/people')
def getPeople():
    return 'some person'

server.run()