from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    generation = db.Column(db.Integer, default=1)

    parent = db.relationship('Person', remote_side=[id], backref='children')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "parent_id": self.parent_id,
            "generation": self.generation,
        }
