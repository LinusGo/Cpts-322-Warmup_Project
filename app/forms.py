from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length, Email
from wtforms import TextAreaField

from app.models import Post


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Post message', validators=[DataRequired()])
    happiness_level = SelectField('Happiness Level',
                                  choices=[(3, 'I can\'t stop smiling'), (2, 'Really happy'), (1, 'Happy')])
    submit = SubmitField('Post')
