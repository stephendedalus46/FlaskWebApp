from flask_wtf import FlaskForm

from wtforms import StringField  # installed with pip, need for username attribute from StringField
from wtforms import SubmitField
from wtforms import TextAreaField

from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
