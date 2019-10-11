from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin

from app import db, bcrypt
from app.predict_api import PredictAPI


class User(db.Model, UserMixin):

    ''' A user who has an account on the website. '''

    __tablename__ = 'users'

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String, primary_key=True)
    confirmation = db.Column(db.Boolean)
    credits = db.Column(db.Integer, default=0)
    _password = db.Column(db.String)
    stripeId = db.Column(db.String)
    diagnoses = db.relationship("Diagnosis", order_by="desc(Diagnosis.id)")

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self.password, plaintext)

    def get_id(self):
        return self.email

    def get_credits(self):
        return self.credits

    def add_credits(self, credits):
        self.credits += credits

    def use_credit(self):
        self.credits -= 1


class Diagnosis(db.Model):

    ''' A list of all the diagnosises run using the model. '''

    __tablename__ = 'diagnoses'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, db.ForeignKey('users.email'))
    time = db.Column(db.Integer)
    prediction = db.Column(db.Integer)
    certainty = db.Column(db.Float)
    filename = db.Column(db.String)
    img = db.Column(db.Binary)

    @property
    def title(self):
        return PredictAPI.getClass(self.prediction)['name']

    @property
    def url(self):
        return PredictAPI.getClass(self.prediction)['url']

