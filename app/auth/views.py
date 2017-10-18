# -*- coding: utf-8 -*-
from flask import render_template, request, flash, redirect, url_for
from . import auth
from .forms import LoginForm, RegistrationForm
from ..models import User, LoginLog
from .. import db
from flask_login import login_user, logout_user, login_required, current_user
import time
from ..email import send_email


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
   
        if not current_user.confirmed \
                and str(request.endpoint[:5]) != 'auth.' \
                and str(request.endpoint) != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/test.html')

# 发送确认邮件
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('您已经确认了您的帐户. 谢谢!','info')
    else:
        flash('确认链接无效或已过期.','warning')
    return redirect(url_for('main.index'))

# 从新发送确认邮件
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    print current_user.email
    print

    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('通过电子邮件发送了一封新的确认电子邮件.','info')
    return redirect(url_for('main.index'))

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

        token = user.generate_confirmation_token()
        print token
        print user.email

        send_email(user.email, '账户确认','auth/email/confirm', user=user, token=token)

        flash('已通过电子邮件向您发送确认电子邮件.','info')
        #flash('you are register successful , please login!','success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

# 用户登出
@auth.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('auth.login'))
