from flask import Flask,render_template,redirect,url_for,request,session,g
from models import ManagerSystem,BuyerSystem,WorkerSystem,Product,User,Edge
import config
from exts import db
from sqlalchemy import or_

app=Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        telephone=request.form.get('telephone')
        password=request.form.get('password')
        user=User.query.filter(User.telephone==telephone).first()
        occupation=request.form.get('occupation')
        if user and user.occupation==occupation and user.check_password(password):
            session['user_id']=user.id
            session.permanent=True
            if user.occupation=='manager':
                return redirect(url_for('managerSystem'))
            elif user.occupation=='buyer':
                return redirect(url_for('buyerSystem'))
            elif user.occupation=='worker':
                return redirect(url_for('workerSystem'))
        else:
            return '用户名或者密码错误（请确认所选职业）'

@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method=='GET':
        return render_template('regist.html')
    else:
        telephone=request.form.get('telephone')
        username=request.form.get('username')
        occupation=request.form.get('occupation')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        user=User.query.filter(User.telephone==telephone).first()
        if user:
            return '此号码已经注册过，请更换'
        else:
            if password1!=password2:
                return '两次密码不相同，请重新输入'
            else:
                user=User(telephone=telephone,username=username,occupation=occupation,password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/manager_system/make_edge/',methods=['GET','POST'])
def makeEdge():
    if request.method=='GET':
        return render_template('makeEdge.html')
    else:
        edgeNum = request.form.get('edge')
        edgeOb = Edge(edge=edgeNum)
        db.session.add(edgeOb)
        db.session.commit()
        contexts = {
            'products': Product.query.all(),
            'edgeOb': Edge.query.filter(Edge.id!=-1).order_by(Edge.id.desc()).first()
        }
        return render_template('manager.html',**contexts)

@app.route('/manager_system/',methods=['GET','POST'])
def managerSystem():
    if request.method=='GET':
        contexts = {
            'products': Product.query.all(),
            'edgeOb': Edge.query.filter(Edge.id!=-1).order_by(Edge.id.desc()).first()
        }
        return render_template('manager.html',**contexts)
    else:
        product_name = request.form.get('product_name')
        order_volume = request.form.get('make_order_volume')
        product = Product.query.filter(Product.product_name == product_name).first()
        manager = g.user
        ms = ManagerSystem(order_volume=order_volume)
        ms.manager = manager
        ms.product = product
        db.session.add(ms)
        db.session.commit()
        contexts = {
            'products': Product.query.all(),
            'edgeOb':Edge.query.filter(Edge.id!=-1).order_by(Edge.id.desc()).first()
        }
        return render_template('manager.html',**contexts)
        

@app.route('/manager_system/addItem/',methods=['GET','POST'])
def addItem():
    if request.method=='GET':
        return render_template('addItem.html')
    else:
        product_name=request.form.get('product_name')
        inventory=request.form.get('inventory')
        product=Product(product_name=product_name,inventory=inventory)
        db.session.add(product)
        db.session.commit()
        contexts = {
            'products': Product.query.all(),
            'edgeOb': Edge.query.filter(Edge.id != -1).order_by(Edge.id.desc()).first()
        }
        return render_template('manager.html',**contexts)


@app.route('/buyer_system/',methods=['GET','POST'])
def buyerSystem():
    if request.method=='GET':
        contexts = {
            'buyerSystems': BuyerSystem.query.filter(BuyerSystem.wether_or_not == 0).all(),
        }
        return render_template('buyer.html',**contexts)
    else:
        for bs in BuyerSystem.query.all():
            if bs.wether_or_not==0:
                bs.wether_or_not=1
                product=Product.query.filter(Product.id==bs.product_id).first()
                product.inventory=product.inventory+bs.purchasing_volume
                ms=ManagerSystem.query.filter(ManagerSystem.product_id==product.id).order_by(ManagerSystem.id.desc()).first()
                ms.order_volume=0
                buyer=g.user
                bs.buyer=buyer
                db.session.commit()
        contexts = {
            'buyerSystems': BuyerSystem.query.filter(BuyerSystem.wether_or_not == 0).all(),
        }
        return render_template('buyer.html',**contexts)


@app.route('/worker_system/',methods=['GET','POST'])
def workerSystem():
    if request.method=='GET':
        contexts = {
            'products': Product.query.all(),
        }
        return render_template('worker.html',**contexts)
    else:
        product_name=request.form.get('product_name')
        take_volume=request.form.get('take_volume')
        product=Product.query.filter(Product.product_name==product_name).first()
        product.inventory=product.inventory-int(take_volume)
        worker=g.user
        ws=WorkerSystem(take_volume=take_volume,worker=worker,product=product)
        db.session.add(ws)
        edgeOb=Edge.query.filter(Edge.id!=-1).order_by(Edge.id.desc()).first()
        if product.inventory < edgeOb.edge:
            manager=ManagerSystem.query.filter(ManagerSystem.product_id==product.id).order_by(ManagerSystem.id.desc()).first()
            purchasing_volume=manager.order_volume
            bs=BuyerSystem(purchasing_volume=purchasing_volume,wether_or_not=0)
            bs.product=product
            db.session.add(bs)
        db.session.commit()
        contexts = {
            'products': Product.query.all(),
        }
        return render_template('worker.html',**contexts)


@app.route('/logout/')
def logout():#注销
    session.clear()
    return redirect(url_for('login'))

@app.before_request
def my_before_request():
    user_id=session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user=user

@app.context_processor
def my_context_proceeor():
    if hasattr(g,'user'):
        return {'user':g.user}
    else:
        return {}

if __name__ == '__main__':
    app.run()

            


