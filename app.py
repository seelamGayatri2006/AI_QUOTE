import requests
import os
import mysql.connector
from flask import Flask,render_template,request,redirect
from dotenv import load_dotenv
load_dotenv()

apikey= os.getenv("APIKEY")
con = mysql.connector.connect(
    host = os.getenv("DB_HOST"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    database = os.getenv("DB_DATABASE")
    )
cursor = con.cursor()
url="https://api.api-ninjas.com/v1/quotes"
headers={'X-Api-Key': apikey}
def get_quote():
    response=requests.get(url,headers)
    data=response.json()
    if isinstance(data,list) and len(data)>0:
        quote_value = data[0]['quote']
        author_value = data[0]['author']
        category_value = data[0]['category']
        return quote_value, author_value, category_value
    else:
        return "No quote found"

app = Flask(__name__)
app.config['SECRETKEY'] = os.getenv("SECRETKEY")
@app.route('/')
def home():
    quote,author,category=get_quote()
    return render_template('ai_quote.html',quote1=quote,author1=author, category1=category)


@app.route('/login',methods=['GET','POST'])
# def login():
#      if request.method== 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s",(username, password))
#         user = cursor.fetchone()
#         return render_template('login.html')
#      return render_template('login.html')
def login():
     if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s",(username, password))
        user = cursor.fetchone()

        if user:
            return redirect('/')
        else:
            return redirect('/login')

     return render_template('login.html')

@app.route('/logout',methods=['GET','POST'])
def logout():
    return render_template('logout.html')
@app.route('/registration',methods=['GET','POST'])
def registration():
    if request.method=='POST':
        user = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        cursor.execute("Insert into users (username,email,password) values(%s,%s,%s)",[user,email,password])
        con.commit()
        # return "values stored"
        return redirect('/login')
    return render_template('registration.html')

@app.route('/house',methods=['GET','POST'])
def house():
    return render_template('house.html')

@app.route('/about',methods=['GET','POST'])
def about():
    return "Welcome back to my channel"

@app.route('/info',methods=['GET','POST'])
def info(): 
    return render_template('index.html')

app.run(use_reloader=True,debug=True)
# app.run(debug=True,use_reloader=True) or app.run()