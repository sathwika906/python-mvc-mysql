from app import app
from flask import render_template
from flask import render_template
from cgitb import html
import collections
from flask import Flask, redirect, url_for, render_template, request, session


from flask_mysqldb import MySQL
import MySQLdb.cursors

import random


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'pymsql'

mysql = MySQL(app)






def bio():
    return ' Name: '+pname+'   Email: '+pemail+'   Gender: ' + pgender+' D.O.B: '+pdob+'  PIN: '+ppin+' '
  
@app.context_processor
def context_processor():
   
    return dict(bio=bio)


def home():
    
    return redirect(url_for('welcome'))




def makeadharglob(adh):
    global adhar
    adhar = adh


def making_global_info(name, mail, pin, gender, dob, id):

    global pemail, pdob, pgender, ppin, pname, gpid
    pname = name
    pemail = mail
    pdob = dob
    pgender = gender
    ppin = pin
    gpid = id


def randomPat_id(digits):
    lower = 10**(digits-1)
    upper = 10**digits - 1
    return random.randint(lower, upper)



@app.route('/signup/', methods=['POST', 'GET'])
def signup():
    msg = " "
    
    pat_id=" "
    name1 = " "
    email1 = " "
    gen1 = " "
    phno = " "
    adhar = " "
    pin = " "
    dob = " "
    sc = " "
    res = " "

    
    if request.method == 'POST':
        pat_id= str(randomPat_id(14))
        name1 = request.form['fname']
        fname=name1
        lname=request.form['lname']

        
        name1 += " "
        name1 += request.form['lname']

        gen1 = request.form['gender']
        phno = request.form['pno']
        adhar = request.form['adhar']
        dob = request.form['birthday']
        email1 = request.form['email']
        pin = request.form['pincode']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    

    cursor.execute('INSERT INTO pat_info VALUES (% s, % s, % s, % s, % s, % s, % s, % s, % s,% s,% s)',
                   (pat_id,fname,lname, email1, gen1, dob, adhar, phno, pin, sc, res ))
    mysql.connection.commit()
    msg = 'You have successfully registered !'

    making_global_info(name1, email1, pin, gen1, dob,pat_id)
   
    makeadharglob(adhar)
    return render_template('table.html',id=pat_id, nm=name1, gen=gen1, pin=pin, dob=dob, email=email1,msg=msg)

@app.route('/success/<int:score>')
def success(score):
    res = ""
    print(score)

    if score >= 4:
        res = "NEED TO CHECHK UP"
    else:
        res = "NO NEED TO CHECHK UP"

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    k=str(score)
    cursor.execute(
        'UPDATE pat_info SET score =% s,result =% s WHERE adhar =% s', (k, res, adhar,))
    mysql.connection.commit()

    return render_template('result.html', result=res, sc=score, id=gpid)


@app.route('/fail/<string:s>')
def fail(s):
    return s+"     please enter the valid input as written in the webpage"


@app.route('/submit', methods=['POST', 'GET'])
def submit():
   
    total_score = 0

    c = 0
    a1=-1

    if request.method == 'POST':


        a1 = int(request.form['age'])
        if (a1 > 3 or a1 < 0 or a1 == -1 ):
            return redirect(url_for('fail', s="invalid input"))
        p2 = int(request.form['2pp'])
        if (p2 > 2 or p2 < 0):
            return redirect(url_for('fail', s="invalid input"))
        p3 = int(request.form['3pp'])
        if (p3 > 1 or p3 < 0):
            return redirect(url_for('fail', s="invalid input"))
        p4 = int(request.form['4pp'])
        if (p4 > 3 or p4 < 0):
            return redirect(url_for('fail', s="invalid input"))
        p5 = int(request.form['5pp'])
        if (p5 > 2 or p5 < 0):
            return redirect(url_for('fail', s="invalid input"))
        p6 = int(request.form['6pp'])
        if (p6 > 2 or p6 < 0):
            return redirect(url_for('fail', s="invalid input"))

        total_score = (a1+p2+p3+p4+p5+p6)

    # sendind the total score to success function
    return redirect(url_for('success', score=total_score))

    

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        pdata=(request.form['primary_key']).lower()
        idata=(request.form['inp']).lower()
        print(pdata)
        print(idata)
    
     
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute("SELECT * from pat_info WHERE id LIKE '"+idata+"%' or lname LIKE '"+idata+"%' or fname LIKE '"+idata+"%'; ")
        result=list(cursor.fetchall())
        print(result)
        return render_template('searchpage.html',parent_list=result)



@app.route('/all_data', methods=['POST', 'GET'])
def all_data():
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pat_info')
        result=list(cursor.fetchall())
        print("heelo")
        print(result)
        print(type(result))
        print(result[0]['id'])
        
        return render_template('searchpage.html',parent_list=result)


