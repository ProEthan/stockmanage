#encoding: utf-8
#配置文件

#有许多参数可以放在配置文件中，比如操作数据库的：
#SECRET_KEY
#SQLALCHEMY

#debug模式，保存即可刷新
DEBUG=True

#数据库的配置
#dialect+driver://username:password@host:port/database
DIALECT='mysql'
DRIVER='pymysql'
USERNAME='root'
PASSWORD='542005gaoyu'
HOST='127.0.0.1'
PORT='3306'
DATABASE='myStockManage2'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:dzd123@localhost/你的数据库名'

SQLALCHEMY_DATABASE_URI="{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS=False

import os
SECRET_KEY=os.urandom(24)

#设定session过期时间
from datetime import timedelta
PERMANENT_SESSION_LIFETIME=timedelta(days=7)