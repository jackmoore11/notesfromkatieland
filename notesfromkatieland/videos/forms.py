from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class VideoForm(FlaskForm):
    locations = [('New_York', 'New York'), ('Milwaukee', 'Milwaukee'), ('Madison', 'Madison'), ('Chicago', 'Chicago')]
    location = SelectField('Katieland Region', choices=locations)
    title = StringField('Title', validators=[DataRequired()])
    video = FileField('Attach Video', validators=[FileRequired(), FileAllowed(['mp4', 'mov'])])
    submit = SubmitField('Post')