from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    pictures = MultipleFileField('Attach Picture(s)', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Post')