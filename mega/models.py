from mega import db,login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(25),nullable=False)
    age=db.Column(db.Integer,nullable=False)
    salary=db.Column(db.Integer,nullable=False)
    gender=db.Column(db.String(6),nullable=False)

    def __repr__(self):
        return '<name={} age={}>'.format(self.name,self.age)

class Admin(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(255),nullable=False,unique=True)
    password=db.Column(db.String(255),nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)