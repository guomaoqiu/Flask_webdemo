# -*- coding:utf-8 -*-
from flask import render_template,redirect,request,Response,flash
from sqlalchemy import desc
from . import main
from flask_login import current_user, login_required
import json,commands,datetime,sys,os
from .forms import RegistrationForm
from ..models import User,LoginLog
from .. import db
reload(sys)
sys.setdefaultencoding("utf-8")


@main.route('/usermanager',methods=['GET', 'POST'])
@login_required
def usermanager():
    '''
    @note: 返回主页内容
    '''
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    role_id=form.role_id.data)
        db.session.add(user)
        db.session.commit()

        flash(u'您已注册成功，请登录吧!','success')
        #flash('you are register successful , please login!','success')
        #return redirect(url_for('auth.login'))
    return render_template('user_manager.html',form=form)
###############################################################################
@main.route('/')
@login_required
def index():
    '''
    @note: 返回主页内容
    '''
    return render_template('index.html')

###############################################################################
@main.route('/server_list')
@login_required
def server_list():
    '''
    @note: 主机列表
    '''
    return render_template('server_list.html')

###############################################################################
@main.route('/loginlog')
@login_required
def loginlog():
    '''
    @note: 返回主页内容
    '''
    # 以ID 倒序查询
    res = LoginLog.query.order_by(desc(LoginLog.id)).all()

    data = []
    for x in res:
        data.append(x.to_json())


    #user_list = User.query.all()
    return render_template('loginlog.html',data=data)
