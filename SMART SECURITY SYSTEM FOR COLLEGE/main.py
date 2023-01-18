import sqlite3
import os
conn = sqlite3.connect('college_database')
cur = conn.cursor()
try:
 cur.execute('''CREATE TABLE Student (
 id integer Primary key AUTOINCREMENT,
 Student_name varchar(20),
 email varchar(50),
 password varchar(20),
 Mobile_No int(10),
 Register_No varchar(50),
 Branch varchar(50),
 address varchar(100),
 year varchar(60))''')
except:
 pass
import requests
import math, random
from flask import Flask, render_template, url_for,request, flash, redirect, session
saved_otp =0
app = Flask(__name__)
@app.route('/user_login',methods = ['POST', 'GET'])
def user_login():
 conn = sqlite3.connect('college_database')
 cur = conn.cursor() 
 if request.method == 'POST':
 Register_No = request.form['Register_No']
 password = request.form['psw']
 count = cur.execute('SELECT * FROM Student WHERE Register_No = "%s" AND password = 
"%s"' % (Register_No, password))
 conn.commit()
 #cur.close()
 print(count)
 if len(cur.fetchall()) == 1:
 print(count)
 flash('{} You have been logged in!'.format(Register_No), 'success')
 session['logged_in_d'] = True
 # cur.execute("update Student set avaliability='true' where Roll_No='%s'" %Roll_No)
 # print("""update Student set avaliability='true' where Roll_No='%s'" %Roll_No""")
 conn.commit()
 cur.execute('select * from Student where Register_No="%s"' % Register_No)
 s = cur.fetchall()
 print(s)
 return render_template('user_account.html', a=Register_No,b=s)
 else:
 flash('invalid register Number and password')
 return redirect(url_for('user_login'))
 return render_template('user_login.html')
@app.route('/enter_mobile')
def enter_mobile():
 return render_template('enter_mobile.html')
@app.route('/user_register',methods = ['POST', 'GET'])
def user_register():
 conn = sqlite3.connect('college_database')
 cur = conn.cursor()
 if request.method == 'POST':
 Student_name = request.form['Student_name']
 email = request.form['email']
 password = request.form['psw']
 Register_No = request.form['Register_No']
 Branch = request.form['Branch']
 address = request.form['address']
 year = request.form['year']
 Mobile_No = request.form['Mobile_No']
 cur.execute("insert into 
Student(Student_name,email,password,Register_No,Branch,address,year,Mobile_No)values('%s','%s'
,'%s','%s','%s','%s',%s,%s)" % (Student_name, email, password, 
Register_No,Branch,address,year,Mobile_No))
 conn.commit()
 # cur.close()
 return redirect(url_for('user_login'))
 return render_template('user_register.html')
@app.route('/server')
def server():
 import pythonchat.pyserve
@app.route('/user_account',methods = ['POST', 'GET'])
def user_account():
 if request.method == 'POST':
 Register_No = request.form['Register_No']
 return render_template('user_account_edit.html', em = Register_No)
 @app.route('/')
@app.route('/home')
def home():
 if not session.get('logged_in'):
 return render_template('home.html')
 else:
 return redirect(url_for('user_account'))
@app.route('/about')
def about():
 return render_template('about.html')
@app.route('/enter_mobile' ,methods = ['POST', 'GET'])
def otp():
 global saved_otp
 conn = sqlite3.connect('college_database')
 cur = conn.cursor()
 if request.method == 'POST':
 number = request.form['number']
 saved_otp = random.randint(1111,9999)
 print("IN otp functin",saved_otp,number)
 url = "https://www.fast2sms.com/dev/bulkV2"
 payload = "sender_id=TXTIND&message=ur otp is {} 
&route=v3&numbers={}".format(saved_otp, number)
 headers = {
 'authorization': 
"hYTK1cSdW6R8iJMLVvyOu9Pn37tG0QgaIFqDreUzfABkpXslZHJeUnIigMSyYGX7Kc4Nr25u9j
Bo1fTZ",
 'Content-Type': "application/x-www-form-urlencoded",
 'Cache-Control': "no-cache"
 }
response = requests.request("POST", url, data=payload, headers=headers)
 print(response.text)
 return render_template('verify.html')
 return render_template('enter_mobile.html')
@app.route('/validateOTP',methods = ['POST','GET'])
def validateOTP():
 global saved_otp
 entered_otp = int(request.form['otp'])
 print("in validate OTP fun",saved_otp,entered_otp,type(saved_otp),type(entered_otp))
 if(entered_otp == saved_otp):
 print('otp matched')
 #flash('otp matched')
 return render_template('allow.html')
 else:
 print('otp wrong')
 flash('you have entered wrong otp')
 return render_template('user_login.html')
@app.route("/logoutd", methods = ['POST','GET'])
def logoutd():
 session['logged_in_d'] = False
 return home()
@app.route("/logout")
def logout():
 session['logged_in'] = False
 return home()
if __name__ == '__main__':
 app.secret_key = os.urandom(12)
 app.run(debug=True)
 