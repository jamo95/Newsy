from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators
from wtforms.validators import DataRequired

#TODO
# Make sure article URLs are correctly validated
# Maybe implement recaptcha
class ArticleForm(FlaskForm):
    article = StringField('article')
    #article = StringField('article', [
    #    validators.DataRequired(message='You forgot the URL!'),
    #    validators.length(min=4, max=500)
    #])

