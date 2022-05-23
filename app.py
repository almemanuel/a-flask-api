from itertools import count
from typing import Optional, List
from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel, Field
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Any API')
spec.register(server)
database = TinyDB(storage = MemoryStorage)
c = count()


class Person(BaseModel):
    id: Optional[int] = Field(default_factory = lambda: next(c))
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


@server.get('/person/<int:id>')
@spec.validate(resp = Response(HTTP_200=Person))
def getPerson(id: int):
    """Get a person on the database

    Return a JSON
    """

    try:
        return jsonify(database.search(Query().id == id)[0])
    except IndexError:
        return {"message": "Person not found"}, 404


@server.post('/person')
@spec.validate(body = Request(Person), resp = Response(HTTP_201 = Person))
def insertPerson():
    """Insert a person on the database

    Returns a JSON
    """

    body = request.context.body.dict()
    database.insert(body)
    return body


@server.put('/person/<int:id>')
@spec.validate(body = Request(Person), resp = Response(HTTP_201 = Person))
def updatePerson(id: int):
    """Update a person on the database

    Returns a JSON
    """

    body = request.context.body.dict()
    database.update(body, Query().id == id)
    return jsonify(body)


@server.delete('/person/<int:id>')
@spec.validate(resp = Response('HTTP_204'))
def deletePerson(id: int):
    """Delete a person on the database

    Returns a JSON
    """

    database.remove(Query().id == id)
    return jsonify({})

server.run()