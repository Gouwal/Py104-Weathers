from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class QueryForm(FlaskForm):
    city = StringField('city')
    query = SubmitField('查询')
    history = SubmitField('历史')
    update = SubmitField('更新')
    help = SubmitField('帮助')
