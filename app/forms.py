from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.widgets import TextArea, Input
from wtforms.validators import URL, Required, NumberRange


class SummaryForm(FlaskForm):
    title = StringField('title')
    text = StringField('text', widget=TextArea())
    url = StringField('url')
    count = IntegerField('count', widget=Input('number'), validators=[
        Required(), NumberRange(min=0)], default=4)
    k_count = IntegerField('count', widget=Input('number'), validators=[
        Required(), NumberRange(min=0)], default=20)

    def is_text(self):
        return self.text.data or self.url.data
