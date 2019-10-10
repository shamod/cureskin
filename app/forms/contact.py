from wtforms import TextField, TextAreaField
from wtforms.validators import (Required, Email)
from flask_wtf import FlaskForm

class ContactUs(FlaskForm):

    ''' Contact Form to send message to team. '''

    name =  TextField(validators=[Required()],
                      description='Your Name')
    email = TextField(validators=[Required(), Email()],
                      description='Your Email Address')
    message = TextAreaField(validators=[Required()],
                      description='Your Message To The Team')
