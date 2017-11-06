# -*- coding:utf-8 -*-
# jsonify 用于返回jsons数据
from flask import render_template,redirect,request,Response,flash,jsonify,url_for,current_app
from sqlalchemy import desc
from . import main
from flask_login import current_user, login_required
from ..decorators import admin_required , permission_required
import json,commands,datetime,sys,os
from .forms import RegistrationForm, EditProfileForm, EditProfileAdminForm, ApiForm
from ..models import User, LoginLog, Role, ApiMg, Hostinfo
from .. import db
from app.crypto import prpcrypt
import time
from ..salt.saltapi import SaltApi

#from ..saltstack import saltapi
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
    @note: 用户管理
    '''
    # 列出用户
    user = User.query.all()
    data = []

    for each_user in user:
        data.append(each_user.to_json())
    print data
    return render_template('user_manager.html',data=data)

###############################################################################

@main.route('/server_list')
@login_required
def server_list():
    '''
    @note: 主机列表
    '''
    host_list = Hostinfo.query.all()
    data = []
    [ data.append(i.to_json()) for i in host_list ]
    print data
    return render_template('server_list.html',data=data)

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

# 平台业务逻辑
@main.route('/api_manager',methods=['GET', 'POST'])
@login_required
def api_manager():
    '''
    @note: 对接第三方API管理函数
    '''
    form = ApiForm()
    #i#f form.validate_on_submit():
    if form.validate_on_submit():
        apiinfo = ApiMg(app_name=form.app_name.data,
                    api_user=form.api_user.data,
                    api_paas=form.api_paas.data,
                    api_url=form.api_url.data)
        try:
            # 加密api密码
            prpcrypt_key = prpcrypt(current_app.config.get('PRPCRYPTO_KEY'))
            apiinfo.api_paas = prpcrypt_key.encrypt(form.api_paas.data)
            db.session.add(apiinfo)
            db.session.commit()
            flash('添加Api信息成功','success')
        except Exception,e:
            db.session.rollback()
            print e
            flash('添加Api信息错误','danger')
    res = ApiMg.query.all()
    data = []
    for x in res:
        data.append(x.to_json())

    return render_template('api_manager.html',form=form,data=data)

# delete api
@main.route('/api_manager_del',methods=['GET', 'POST'])
@login_required
def api_manager_del():
    '''
    @note: 在登陆状态下只允许管理者进入，否则来到403禁止登陆界面
    '''
    if request.method == 'POST':
        check_id = json.loads(request.form.get('data'))['check_id']
        api_id = ApiMg.query.filter_by(id=check_id).first()
        try:
            db.session.delete(api_id)
            print check_id
            return  jsonify({"result":True,"message":"删除成功"})
        except Exception, e:
            db.session.rollback()
            print e
            return  jsonify({"result":False,"message":"删除失败".format(e)})
###############################################################################
@main.route('/task_center',methods=['GET', 'POST'])
@login_required
def task_center():
    '''
    @note: 在登陆状态下只允许管理者进入，否则来到403禁止登陆界面
    '''
    return render_template('task_center.html')

@main.route('/delete_server',methods=['GET', 'POST'])
def delete_server():
    '''
    @note: 从数据库中删除已经存在的主机
    '''
    delete_host = []
    hostname = json.loads(request.form.get('data'))['hostname']
    [ delete_host.append(host.encode('raw_unicode_escape')) for host in hostname.split(',')]
    try:
        [ db.session.query(Hostinfo).filter(Hostinfo.hostname == host).delete() for host in delete_host ]
        result = {'result': True, 'message': u"删除所选主机成功" }
    except Exception, e:
        result = {'result': False, 'message': u"删除所选主机失败,%s" % e}
    return jsonify(result)

@main.route('/get_server_info',methods=['GET', 'POST'])
def get_server_info():
    '''
    @note: 通过saltapi获取所有minion主机的服务器信息，填入写入数据库中
    '''
    # 获取所有server的hostname
    if request.method == "POST":
        if not ApiMg.query.filter_by(app_name='saltstack').first():
            result = {"result": False, "message": u'请确保api信息已录入！'}
            return jsonify(result)
        else:
            try:
                client = SaltApi('saltstack')
                params = {'client': 'local', 'fun': 'test.ping', 'tgt': '*'}
                json_data = client.get_allhostname(params)
                data = dict(json.loads(json_data)['return'][0])

                hostname_list = []

                [hostname_list.append(i) for i in data.keys()]
                #print hostname_list
                for host in hostname_list:
                    if not Hostinfo.query.filter_by(hostname=host).first():

                        all_host_info = dict(client.get_minions(host).items())
                        print all_host_info
                        host_record = Hostinfo(
                            hostname=all_host_info['hostname'],
                            private_ip=all_host_info['private_ip'],
                            public_ip=all_host_info['public_ip'],
                            mem_total=all_host_info['mem_total'],
                            cpu_type=all_host_info['cpu_type'],
                            num_cpus=all_host_info['num_cpus'],
                            os_release=all_host_info['os_release'],
                            kernelrelease=all_host_info['kernelrelease']
                        )
                        db.session.add(host_record)
                        db.session.commit()

                result = {"result": True, "message": u'刷新完毕！'}
                return jsonify(result)

            except Exception, e:
                print e
                result = {"result": False, "message": u'刷新出错！'}
                return jsonify(result)
