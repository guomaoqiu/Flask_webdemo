# coding: utf-8
from flask import render_template, request, flash, redirect, url_for
from . import auth
from .forms import LoginForm, RegistrationForm
from ..models import User, LoginLog
from .. import db
from flask_login import login_user, logout_user, current_user
import time

# 用户登录
@auth.route('/')
@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Check user info, email and password !
    '''
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # 数据库查询
        if user is not None and user.verify_password(form.password.data): # 用户是否存在以及是否正确

            login_user(user,form.remember_me.data) # 记住我功能，bool值

            print request.user_agent
            print request.cookies
            # 记录登陆日志
            users = LoginLog()
            print user.username # 用户
            users.loginuser=user.username
            users.logintime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) #时间
            users.login_browser=request.user_agent #代理
            users.login_ip=request.remote_addr # 登录地址
            db.session.add(users) # 提交
            db.session.commit()


            return redirect(url_for('main.index')) # 如果认证成功则重定向到已认证首页

        else:
            flash(u'邮箱或密码无效,请重新输入!','danger')    # 如果认证错误则flash一条消息过去
            #flash('email or password error','danger')    # 如果认证错误则flash一条消息过去
    return render_template('auth/login.html',form=form)
    #return render_template('auth/login.html')

#用户注册
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash(u'您已注册成功，请登录吧!','success')
        #flash('you are register successful , please login!','success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

# 用户登出
@auth.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('auth.login'))
