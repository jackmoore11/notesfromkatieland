from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class VideoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    video = FileField('Attach Video', validators=[FileRequired(), FileAllowed(['mp4', 'mov'])])
    submit = SubmitField('Post')