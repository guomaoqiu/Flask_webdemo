# -*- coding:utf-8 -*-
from flask import render_template,redirect,request,Response,flash
from . import main
import json,commands
from flask_login import current_user, login_required
import datetime
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

@login_required
@main.route('/')
def index():
    '''
    @note: 当前cbt服务器时间
    '''
    return render_template('index.html')
