from flask import Flask, render_template, request, redirect, flash,url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user

import model
import logging
from logging.handlers import RotatingFileHandler
# create the app
app = Flask(__name__)

# Enable logging
app.logger.setLevel(logging.DEBUG)

# Log a message
app.logger.debug('This is a debug message')

# Create a rotating file handler that will save the last 10 log files
handler = RotatingFileHandler('logs/myapp.log', maxBytes=10000, backupCount=10)
handler.setLevel(logging.DEBUG)

# Add the handler to the logger
app.logger.addHandler(handler)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///demo.db"

app.config['SECRET_KEY'] = 'thisissecret'

# create the extension
db = SQLAlchemy(app)
# initialize the app with the extension
migrate = Migrate(app, db)

login_manager = LoginManager()

login_manager.init_app(app)
                
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    email = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    fname = db.Column(db.String(80), unique=False, nullable=False)
    lname = db.Column(db.String(80), unique=False, nullable=False)
    
    # def __repr__(self):
    #     return '<User %r>' % self.email
    
    def get_id(self):
        return str(self.id)
    
    
    # here we are not going to store any prediction data. just have created model schema
class Predictions(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
   
    rooms_count = db.Column(db.String(80), unique=False, nullable=False)
    
    pt_ratio = db.Column(db.String(80), unique=False, nullable=False)
    lstat = db.Column(db.String(80), unique=False, nullable=False)
    

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/predict', methods = ['GET', 'POST'])
@login_required
def predict():
    
        if request.method == 'POST':
            try:
                rooms_count = float(request.form['rooms_count'])
                ptratio = float(request.form['ptratio'])
                lstat = float(request.form['rooms_count'])
            except:
                rooms_count = request.form['rooms_count']
                ptratio = request.form['ptratio']
                lstat = request.form['rooms_count']
                if rooms_count=="" or ptratio=="" or lstat=="":
                    return render_template("predict.html", error="Oops...some input value is missing, pls try again :)")
            else:
                predicted_price = model.Predict([rooms_count, ptratio, lstat])
                print("predicted price is:", predicted_price)
                return render_template("predict.html", Predicted_price="Predicated Price is: {} $ ".format(round(predicted_price, 2)))
        return render_template("predict.html")
        
   
    
    
        
    # return render_template("index.html", predicted_price="Price of house is predicted as : {}".format(predicted_price))   
    
    
    

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        lst=[]
        email = request.form.get('email')
        password = request.form.get('password')
        fname = request.form.get('first_name')
        lname = request.form.get('last_name')
        emailids = User.query.all()
        print(fname,lname,email,password)
        for nm in emailids:
            lst.append(nm.email)
            
        if (email=='' or password=='' or fname=='' or lname==''):
            flash("Error: All fields are required", "danger")
            print("Error: All fields are required")
            return redirect('/register')
        # elif email in lst:
        #     flash("Oops...This email ID is already registered with us.","danger")
        #     print("Oops...This email ID is already registered with us.")
        #     return redirect('/register')
        else:
            form = User(email=email, password=password, fname=fname, lname=lname)
            db.session.add(form)
            db.session.commit()

            flash("User registered successfully","success")
            print("User is registered")
            return redirect('/login')
            
    return render_template("register.html")
        
        
        
        


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        # if user == "" or user.password == "":
            
        #     print("Incomplete credentials")
        #     return redirect('/login')
        if user and password==user.password:
            login_user(user)
            session['id'] = user.id
            print("user logged in")
            return redirect(url_for('predict'))
       
        else:
            print("invalid credentials")
            return redirect('/login')
    
    
    else:    
    
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
     # clear the session and redirect the user to the login page
    session.clear()
    return redirect('/')
    
if __name__ == '__main__':  
    app.run(host = '0.0.0.0', port=81, debug = False) 
    
  