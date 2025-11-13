# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    generation = db.Column(db.Integer, nullable=False, default=1)
    parent_id = db.Column(db.Integer, db.ForeignKey('persons.id'), nullable=True)

    parent = db.relationship('Person', remote_side=[id], backref='children', lazy='joined')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "generation": self.generation,
            "parent_id": self.parent_id
        }

    def __repr__(self):
        return f"<Person {self.name} (gen {self.generation})>"
