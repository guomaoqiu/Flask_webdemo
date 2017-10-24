# -*- coding:utf-8 -*-
# jsonify 用于返回jsons数据
from flask import render_template,redirect,request,Response,flash,jsonify,url_for
from sqlalchemy import desc
from . import main
from flask_login import current_user, login_required
from ..decorators import admin_required , permission_required
import json,commands,datetime,sys,os
from .forms import RegistrationForm, EditProfileForm, EditProfileAdminForm
from ..models import User,LoginLog
from .. import db
from ..models import Role, User

reload(sys)
sys.setdefaultencoding("utf-8")

###############################################################################

@main.route('/admin')      
@login_required
@admin_required
def for_admin_only():
    '''
    @note: 在登陆状态下只允许管理者进入，否则来到403禁止登陆界面
    '''
    return render_template('admin.html')

###############################################################################

@main.route('/')
# @admin_required
@login_required
def index():
    '''
    @note: 返回主页内容
    '''
    if not current_user.is_authenticated:
        return redirect('auth/login')
    else:
        return render_template('index.html')

###############################################################################

@main.route('/user/<username>')
def user(username):
    '''
    @note: 返回用户信息页面
    '''
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

###############################################################################

@main.route('/usermanager',methods=['GET', 'POST'])
@login_required
def usermanager():
    '''
    @note: 用户注册
    '''
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

        flash(u'添加用户成功','success')

    # 列出用户
    res = User.query.all()
    data = []
    for x in res:
        data.append(x.to_json())

    return render_template('user_manager.html',form=form,data=data)

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
    @note: 查询登录日志
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

###############################################################################

@main.route('/test',methods=['GET', 'POST'])
#@login_required
def test():
    if request.method == 'POST':
        print request.method
        result = {"result":True}
        return  jsonify(result)

###############################################################################

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    '''
    @note: 普通用户编辑
    '''
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.','success')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

###############################################################################

@main.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    '''
    @note: 管理员编辑
    '''
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.','success')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

###############################################################################