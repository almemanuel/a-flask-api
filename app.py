from flask import Flask, request
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Any API')
spec.register(server)

class Person(BaseModel):
    id: int
    name: str
    age :int


@server.get('/')
def get():
    """Try to get the slash

    Return a message
    """
    return 'Works!'


@server.get('/person')
def getPerson():
    """Get a person on the database

    Return a message
    """
    return 'some person'


@server.post('/person')
@spec.validate(body=Request(Person), resp=Response(HTTP_200=Person))
def insertPerson():
    """Insert a person on the database

    Returns a JSON
    """
    body = request.context.body.dict()
    return body


server.run()