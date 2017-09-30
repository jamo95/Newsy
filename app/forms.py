from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.widgets import TextArea, Input
from wtforms.validators import Required, NumberRange


class SummaryForm(FlaskForm):
    title = StringField('title')
    text = StringField('text', widget=TextArea())
    url = StringField('url')
    count = IntegerField('count', widget=Input('number'), validators=[
        Required(), NumberRange(min=0)], default=4)

    def is_text(self):
        return self.text.data or self.url.data
