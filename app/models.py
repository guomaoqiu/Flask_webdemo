from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager
from flask import current_app

# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     users = db.relationship('User', backref='role', lazy='dynamic')
#
#     def __repr__(self):
#         return '<Role %r>' % self.name




class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Boolean)
    #$role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    def is_admin(self):
        if role_id == 1:
            return 'True'
        else:
            return 'Flse'

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


    def to_json(self):
        return {
                'id': self.id,
                'email': self.email,
                'username': self.username,
                'role_id':self.role_id,
                }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginLog(db.Model):
    __tablename__ = 'login_log'
    id = db.Column(db.Integer, primary_key=True)
    loginuser = db.Column(db.String(64))
    logintime = db.Column(db.String(64))
    login_browser = db.Column(db.String(200))
    login_ip = db.Column(db.String(64))

    def to_json(self):
        return {
                'id': self.id,
                'loginuser': self.loginuser,
                'logintime': self.logintime,
                'login_browser':self.login_browser,
                'login_ip': self.login_ip,
                }
