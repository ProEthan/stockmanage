from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class ManagerSystem(db.Model):#管理员订购量表
    __tablename__='managerSystem'
    id=db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    order_volume=db.Column(db.INTEGER,default=0)#订购量

    manager_id=db.Column(db.INTEGER,db.ForeignKey('user.id'))
    product_id=db.Column(db.INTEGER,db.ForeignKey('product.id'))

    create_time=db.Column(db.DateTime,default=datetime.now)

    manager=db.relationship('User',backref=db.backref('manageItems',order_by=id.desc()))#订购的人是谁
    product=db.relationship('Product',backref=db.backref('manageItems',order_by=id.desc()))#订购的产品是什么



class BuyerSystem(db.Model):#采购员采购量表
    __tablename__='buyerSystem'
    id=db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    purchasing_volume=db.Column(db.INTEGER,default=0)#采购量
    wether_or_not=db.Column(db.INTEGER,default=1)

    buyer_id=db.Column(db.INTEGER,db.ForeignKey('user.id'))
    product_id=db.Column(db.INTEGER,db.ForeignKey('product.id'))

    create_time=db.Column(db.DateTime,default=datetime.now)

    buyer=db.relationship('User',backref=db.backref('buyItems',order_by=id.desc()))#采购的人是谁
    product=db.relationship('Product',backref=db.backref('buyItems',order_by=id.desc()))#采购的产品是什么




class WorkerSystem(db.Model):#工人提取量表
    __tablename__='workerSystem'
    id=db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    take_volume=db.Column(db.INTEGER,default=0)#提取量

    worker_id=db.Column(db.INTEGER,db.ForeignKey('user.id'))
    product_id=db.Column(db.INTEGER,db.ForeignKey('product.id'))

    create_time=db.Column(db.DateTime,default=datetime.now)

    worker=db.relationship('User',backref=db.backref('takeItems',order_by=id.desc()))#提取的工人是谁
    product=db.relationship('Product',backref=db.backref('takeItems',order_by=id.desc()))#提取的产品是什么


class Product(db.Model):#产品库存量表
    __tablename__='product'
    id=db.Column(db.INTEGER,primary_key=True,autoincrement=True)#id
    product_name=db.Column(db.String(100),nullable=False)#零件名称
    inventory=db.Column(db.INTEGER,default=0)#目前库存量


class Edge(db.Model):
    __tablename__='edge'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)  # id
    edge=db.Column(db.INTEGER,default=2000)
    create_time = db.Column(db.DateTime, default=datetime.now)

class User(db.Model):#用户
    __tablename__='user'
    id=db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    
    username=db.Column(db.String(100),nullable=False)#用户名
    telephone=db.Column(db.String(11),nullable=False)#手机号
    password=db.Column(db.String(100),nullable=False)#密码
    occupation=db.Column(db.String(100),nullable=False)#职业


    def __init__(self, *args, **kwargs):
        telephone = kwargs.get('telephone')
        username = kwargs.get('username')
        occupation=kwargs.get('occupation')
        password = kwargs.get('password')

        self.telephone = telephone
        self.username = username
        self.occupation=occupation
        self.password = generate_password_hash(password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result