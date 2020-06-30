from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ChatHistoryForm(FlaskForm):
    content = TextAreaField('Chat', validators=[DataRequired()])
    submit = SubmitField("Chat")


