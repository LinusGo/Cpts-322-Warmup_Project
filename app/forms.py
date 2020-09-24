from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length, Email
from wtforms import TextAreaField

from app.models import Tag
from wtforms.widgets import ListWidget, CheckboxInput


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Post message', validators=[DataRequired()])
    happiness_level = SelectField('Happiness Level',
                                  choices=[(3, 'I can\'t stop smiling'), (2, 'Really happy'), (1, 'Happy')])
    submit = SubmitField('Post')
    tag = QuerySelectMultipleField('Tag', query_factory=lambda: Tag.query.all(), get_label=lambda t: t.name,
                                   widget=ListWidget(prefix_label=False),
                                   option_widget=CheckboxInput())


class SortForm(FlaskForm):
    sort = SelectField('Sort by', choices=[(4, 'Date'), (3, 'Title'), (2, '# of likes'), (1, 'Happiness level')])
    refresh = SubmitField('Refresh')
