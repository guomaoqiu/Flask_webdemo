# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField, PasswordField

from wtforms.validators import DataRequired, Length, Email , EqualTo, Regexp, Required
from wtforms import ValidationError
from ..models import User,Role
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


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')




class ApiForm(FlaskForm):
    app_name = StringField('应用名称', validators=[Length(0, 64)])
    api_user = StringField('Api用户', validators=[Length(0, 64)])
    api_paas = StringField('API密码', validators=[Length(0, 64)])
    api_url = StringField('API地址', validators=[Length(0, 64)])
    submit = SubmitField('Submit')
