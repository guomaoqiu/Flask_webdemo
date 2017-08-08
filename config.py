# -*- coding:utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1qaz2wsx'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    BABEL_DEFAULT_LOCALE = 'zh'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    db_host = '127.0.0.1'
    db_user = 'flask'
    db_pass = 'flask'
    db_name = 'flask'
    SQLALCHEMY_DATABASE_URI = 'mysql://' + db_user + ':' + db_pass + '@' + db_host + '/' + db_name
    SQLALCHEMY_ECHO=False #用于显式地禁用或启用查询记录

    #SQLALCHEMY_DATABASE_URI = 'mysql://flask1:flask1@127.0.0.1/flask1'
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    #google 验证码
    #RECAPTCHA_PUBLIC_KEY = '1qaz2wsx3edc'
    #RECAPTCHA_PRIVATE_KEY = '1dfdewdf3dsfdsa'


class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'mysql://flask:flask@127.0.0.1/flask-test'
    WTF_CSRF_ENABLED = False


class Production(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = 'mysql://flask:flask@127.0.0.1/flask-pro'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': Production,
    'default': DevelopmentConfig
}
