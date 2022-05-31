from enum import unique
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db_name = 'todolistdatabase.db'

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_name}"
db = SQLAlchemy(app)


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    complete = db.Column(db.Boolean, default=False)


@app.route('/')
def home():
    todo_list = ToDo.query.all()
    return render_template('home.html', todo_list=todo_list)



@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    new_todo = ToDo(title=title)
    db.session.add(new_todo)
    db.session.commit()

    return redirect(url_for('home'))


@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = ToDo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()

    return redirect(url_for('home'))


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = ToDo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)