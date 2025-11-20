import pytest
from app import create_app
from models import Person
from app import db

@pytest.fixture
def app_instance():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app_instance):
    return app_instance.test_client()

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200

def test_add_person_without_parent(client):
    response = client.post("/add", data={"name": "Alice"})
    assert response.status_code == 302  # Redirect to index
    # Check DB
    from models import Person
    person = Person.query.filter_by(name="Alice").first()
    assert person is not None
    assert person.generation == 1

def test_add_person_with_parent(client):
    from models import Person
    parent = Person(name="Bob", generation=1)
    db.session.add(parent)
    db.session.commit()
    response = client.post("/add", data={"name": "Charlie", "parent_id": str(parent.id)})
    assert response.status_code == 302
    child = Person.query.filter_by(name="Charlie").first()
    assert child.generation == 2

def test_delete_person_existing(client):
    from models import Person
    person = Person(name="David")
    db.session.add(person)
    db.session.commit()
    response = client.post(f"/delete/{person.id}")
    assert response.status_code == 302
    assert db.session.get(Person, person.id) is None

def test_delete_person_non_existing(client):
    response = client.post("/delete/9999")
    assert response.status_code == 302  # Should redirect even if person not found

def test_tree_view(client):
    from models import Person
    person = Person(name="Eve")
    db.session.add(person)
    db.session.commit()
    response = client.get("/tree")
    assert response.status_code == 200
    assert b"Eve" in response.data
