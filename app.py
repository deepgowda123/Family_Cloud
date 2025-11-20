import os
from flask import Flask, render_template, request, redirect, url_for
from models import db, Person
from flask_wtf import CSRFProtect

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)

    # ---------------------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------------------

    # Database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'sqlite:///ancestor_tree.db'  # safe fallback
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # SECRET_KEY - must be set as an environment variable
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        secret_key = "test-secret-key"
    app.config["SECRET_KEY"] = secret_key

    # ---------------------------------------------------------------------
    # Init Extensions
    # ---------------------------------------------------------------------
    csrf.init_app(app)
    db.init_app(app)

    # Create tables once at startup, not on every request
    with app.app_context():
        db.create_all()

    # ---------------------------------------------------------------------
    # Routes
    # ---------------------------------------------------------------------

    @app.route('/')
    def index():
        persons = Person.query.all()
        return render_template('index.html', persons=persons)

    @app.route('/add', methods=['POST'])
    def add_person():
        name = request.form.get('name')
        parent_id = request.form.get('parent_id') or None
        generation = int(request.form.get('generation', 1))

        # If parent exists → auto increment generation
        if parent_id:
            parent = db.session.get(Person, parent_id)
            if parent:
                generation = parent.generation + 1

        new_person = Person(
            name=name,
            parent_id=parent_id,
            generation=generation
        )
        db.session.add(new_person)
        db.session.commit()

        return redirect(url_for('index'))

    @app.route('/delete/<int:person_id>', methods=['POST'])
    def delete_person(person_id):
        person = db.session.get(Person, person_id)
        if person:
            db.session.delete(person)
            db.session.commit()
        return redirect(url_for('index'))

    @app.route('/tree')
    def tree_view():
        people = Person.query.all()
        data = [p.to_dict() for p in people]
        return render_template("tree_view.html", people=data)

    return app


# -------------------------------------------------------------------------
# Run locally (not used in Docker/Jenkins)
# -------------------------------------------------------------------------
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
