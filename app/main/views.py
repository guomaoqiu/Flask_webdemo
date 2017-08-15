# -*- coding:utf-8 -*-
# jsonify 用于返回jsons数据
from flask import render_template,redirect,request,Response,flash,jsonify
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
    #print request.form.get('role')
    role_id = 1
    if request.form.get('role') == 'y':
        #print '管理员'
        role_id = 0

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    role_id=role_id)
        db.session.add(user)
        db.session.commit()

        flash(u'您已注册成功','success')

    # 列出用户
    res = User.query.all()
    data = []
    for x in res:
        data.append(x.to_json())

    return render_template('user_manager.html',form=form,data=data)
###############################################################################
@main.route('/')
@login_required
def index():
    '''
    @note: 返回主页内容
    '''
    res2 = User.query.filter_by()
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
@main.route('/loginlog',methods=['GET', 'POST'])
@login_required
def loginlog():
    '''
    @note: 返回主页内容
    '''
    if request.method == 'POST':
        return "ok"
        #return redirect('http://www.baidu.com')
    # 以ID 倒序查询 最近10条
    res = LoginLog.query.order_by(desc(LoginLog.id)).limit(10)
    #res = LoginLog.query.order_by(desc(LoginLog.id)).all() # 查询所有

    data = []
    for x in res:
        data.append(x.to_json())


    #user_list = User.query.all()
    return render_template('loginlog.html',data=data)



@main.route('/test',methods=['GET', 'POST'])
#@login_required
def test():
    if request.method == 'POST':
        print request.method
        result = {"result":True}
        return  jsonify(result)
