# -*- coding:utf-8 -*-
from flask import render_template,redirect,request,Response,flash
from . import main
from flask_login import current_user, login_required
import json,commands,datetime,sys,os


reload(sys)
sys.setdefaultencoding("utf-8")

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
