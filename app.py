from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Person
from forms import PersonForm
import os


def create_app():
    app = Flask(__name__)

    # 🔧 Load config
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'sqlite:///ancestor_tree.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'devsecret')

    # ✅ Bind SQLAlchemy to the app
    db.init_app(app)

    # ✅ Create tables before first request
    @app.before_request
    def create_tables():
        db.create_all()

    # 🏠 Home route
    @app.route('/')
    def index():
        persons = Person.query.all()
        return render_template('index.html', persons=persons)

    # ➕ Add new person
    @app.route('/add', methods=['POST'])
    def add_person():
        name = request.form.get('name')
        parent_id = request.form.get('parent_id') or None
        generation = int(request.form.get('generation', 1))

        if parent_id:
            parent = Person.query.get(parent_id)
            if parent:
                generation = parent.generation + 1

        new_person = Person(name=name, parent_id=parent_id, generation=generation)
        db.session.add(new_person)
        db.session.commit()

        return redirect(url_for('index'))
    
    
    @app.route('/delete/<int:person_id>', methods=['POST'])
    def delete_person(person_id):
        person = Person.query.get(person_id)
        if person:
            db.session.delete(person)
            db.session.commit()
        return redirect(url_for('index'))


    # 🌳 Tree view route
    @app.route("/tree")
    def tree_view():
        people = Person.query.all()
        data = [p.to_dict() for p in people]
        return render_template("tree_view.html", people=data)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
