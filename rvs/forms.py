from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from flask.ext.wtf import Form
from .models import User
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired,ValidationError

class LoginForm(Form):
    username = StringField('Username', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])

    def validate_password(form, field):
        try:
            user = User.query.filter(User.username == form.username.data).one()
        except (MultipleResultsFound, NoResultFound):
            raise ValidationError("Invalid password")
        if user is None or not user.is_valid_password(form.password.data):
            raise ValidationError("Invalid password")

        form.user = user

class ReserveForm(Form):
    count = StringField('Count', validators = [InputRequired()])
