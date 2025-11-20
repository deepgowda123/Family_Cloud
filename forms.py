from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class PersonForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    parent_id = IntegerField('Parent ID')
    generation = IntegerField('Generation', default=1)
    submit = SubmitField('Add Person')
