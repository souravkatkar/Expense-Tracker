from flask import Flask,render_template,request,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'HalaMadrid'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.sqlite'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    amount = db.Column(db.Float)
    expense = db.Column(db.String)
    date = db.Column(db.Date)
    
    

db.create_all()
db.session.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        data = {
            'error' : ""
        }
        return render_template('login.html',data=data)

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:

            if password == user.password:
                session['user_id'] = user.id
                return render_template('index.html')

            else:
                data = {
                    'error': "Invalid Credentials"
                }
                return render_template('login.html',data=data)

        else:
            data = {
                    'error': "Invalid Credentials"
                }
            return render_template('login.html',data=data)

@app.route('/index')
def index():
    return render_template('index.html')
     

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'GET':
        data = {
                'name' : "",
                'lastname' : "",
                'email' : "",
                "error" : ""
                
            }
        return render_template('signup.html',data=data)

    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        if len(password) < 6:
            data = {
                'name' : name,
                'lastname' : lastname,
                'email' : email,
                'error' : "Password too short",
            }
            
            return render_template('signup.html',data = data)
            

        user = User.query.filter_by(email=email).first()
        print(user)
        if user:
            data = {
                'name' : name,
                'lastname' : lastname,
                'error' : "Email already registered"
            }
            
            return render_template('signup.html',data = data)
        else:
            db.session.add(User(name=name,lastname=lastname,email=email,password=password))
            db.session.commit()
            user = User.query.filter_by(email=email).first()
            session['user_id'] = user.id
            return render_template('index.html')
        

@app.route('/logout')
def logout():
    session.clear()
    return render_template('home.html')

@app.route('/addexpenses',methods=['POST','GET'])
def addexpenses():

    if request.method == 'GET':
        data={
            'message' : ""
        }
        return render_template('addexpenses.html',data= data)

    if request.method == 'POST':
        print("In post function")
        amount = request.form['amount']
        expense = request.form['expense']
        
        a = request.form['date']
        date = datetime.strptime(a,'%Y-%m-%d')
        date = date.date()

        print(date)
        print(amount,expense)
        user_id = session['user_id']
        db.session.add(Expenses(user_id=user_id,amount=amount,expense=expense,date=date))
        db.session.commit()
        data ={
            'message' : "Expense Added" 
        }
        return render_template('addexpenses.html',data = data)


@app.route('/viewexpenses')
def viewexpenses():
    user_id = session['user_id']
    expenses = Expenses.query.filter_by(user_id=user_id).all()
    return render_template('viewexpenses.html',data = expenses)


if __name__ == '__main__':
    app.run()
