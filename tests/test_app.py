from app import create_app
from models import db, Person


def setup_app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    with app.app_context():
        db.create_all()
    return app


def test_home_page():
    app = setup_app()
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_add_person_no_parent():
    app = setup_app()
    client = app.test_client()

    response = client.post("/add", data={"name": "Alice", "generation": 1})
    assert response.status_code == 302

    with app.app_context():
        p = Person.query.filter_by(name="Alice").first()
        assert p is not None
        assert p.generation == 1


def test_add_person_with_parent():
    app = setup_app()
    client = app.test_client()

    with app.app_context():
        parent = Person(name="Root", generation=1)
        db.session.add(parent)
        db.session.commit()
        parent_id = parent.id

    response = client.post("/add", data={"name": "Child", "parent_id": parent_id})
    assert response.status_code == 302

    with app.app_context():
        child = Person.query.filter_by(name="Child").first()
        assert child.generation == 2


def test_delete_person_existing():
    app = setup_app()
    client = app.test_client()

    with app.app_context():
        p = Person(name="DeleteMe")
        db.session.add(p)
        db.session.commit()
        pid = p.id

    response = client.post(f"/delete/{pid}")
    assert response.status_code == 302

    with app.app_context():
        assert db.session.get(Person, pid) is None


def test_delete_person_non_existing():
    app = setup_app()
    client = app.test_client()
    response = client.post("/delete/9999")
    assert response.status_code == 302
