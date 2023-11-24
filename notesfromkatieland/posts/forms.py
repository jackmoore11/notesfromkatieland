from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField, SelectField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    locations = [('New_York', 'New York'), ('Milwaukee', 'Milwaukee'), ('Madison', 'Madison'), ('Chicago', 'Chicago')]
    location = SelectField('Katieland Region', choices=locations)
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    pictures = MultipleFileField('Attach Picture(s)', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Post')