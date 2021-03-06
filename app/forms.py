from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class QueryForm(FlaskForm):
    campaign_number = StringField('Campaign Number (i6qx)', validators=[DataRequired()])
    table_name = StringField('Table Name')
    start_time = StringField('Start Time')
    end_time = StringField('End Time')