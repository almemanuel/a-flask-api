from typing import Optional, List
from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel
from tinydb import TinyDB, Query

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Any API')
spec.register(server)
database = TinyDB('database.json')


class Person(BaseModel):
    id: Optional[int]
    name: str
    age :int


class People(BaseModel):
    people: List[Person]
    count: int


@server.get('/')
def get():
    """Try to get the slash

    Return a message
    """

    return 'Works!'


@server.get('/people')
@spec.validate(resp = Response(HTTP_200=People))
def getPeople():
    """Get all people on the database

    Return a JSON
    """

    return   jsonify(
                        People(
                            people = database.all(),
                            count = len(database.all())
                        ).dict()
                    )


@server.post('/person')
@spec.validate(body = Request(Person), resp = Response(HTTP_200 = Person))
def insertPerson():
    """Insert a person on the database

    Returns a JSON
    """

    body = request.context.body.dict()
    database.insert(body)
    return body


@server.put('/person/<int:id>')
@spec.validate(body = Request(Person), resp = Response(HTTP_200 = Person))
def updatePerson(id: int):
    """Update a person on the database

    Returns a JSON
    """

    body = request.context.body.dict()
    database.update(body, Query().id == id)
    return jsonify(body)


@server.delete('/person/<int:id>')
@spec.validate(resp = Response(HTTP_200 = Person))
def deletePerson(id: int):
    """Delete a person on the database

    Returns a JSON
    """

    database.remove(Query().id == id)
    return jsonify({})

server.run()