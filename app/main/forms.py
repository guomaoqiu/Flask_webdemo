# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email , EqualTo, Regexp
from wtforms import ValidationError
from ..models import User
from .. import db

# 用户登录
# class LoginForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Length(1, 64),Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     # recaptcha = RecaptchaField() # google验证码
#     remember_me = BooleanField('Keep me logged in')
#
#     submit = SubmitField('Log In')


# 用户注册
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                           Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    role = BooleanField('是否是管理员角色')
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
