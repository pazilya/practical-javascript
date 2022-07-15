from enum import unique
import json
import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todoText = db.Column(db.String(144), nullable=False)
    completed = db.Column(db.Boolean, unique=False)

    def __init__(self, todo, completed):
        self.todoText = todo
        self.completed = completed

    def __repr__(self):
        return f"[{'x' if self.completed else ' '}]- {self.todo}"


@app.route('/')
def index():
    return render_template('todoList.html')


@app.route('/todos')
def get_todos():
    output = []
    for todo in Todo.query.all():
        output.append({'id': todo.id,
                       'todoText': todo.todoText,
                       'completed': todo.completed})
    return {"todos": output}


@app.route('/todos/<id>')
def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return {'todoText': todo.todoText, 'completed': todo.completed}


@app.route('/todos', methods=['POST'])
def add_todos():
    result = request.json
    Todo.__table__.drop(db.engine)
    db.create_all()
    for todo in result["todos"]:
        print(todo["todoText"])
        newItem = Todo(todo=todo["todoText"], completed=todo["completed"])
        db.session.add(newItem)
        db.session.commit()
    # db.session.commit()
    # return json.dumps({"message": "success"})
    return get_todos()


@app.route('/todos/<id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    if todo is None:
        return {"error": "todo not found"}
    db.session.delete(todo)
    db.session.commit()
    return {"message": "yeet!"}


@app.route('/todos/<id>', methods=['PUT'])
def edit_todo(id):
    todo = Todo.query.get(id)
    if todo is None:
        return {"error": "todo not found"}
    todo.todoText = request.get_json()["todoText"]
    db.session.commit()
    return {"id": todo.id}


if __name__ == '__main__':
    app.run(debug=True)
