from app import app
from app import models
from flask import render_template
from cgitb import html
import collections
from flask import Flask, redirect, url_for, render_template, request, session
# import pymongo

from flask_mysqldb import MySQL
@app.route('/')
def index():
    return render_template('initial.html')

@app.route('/signuppage')
def signuppage():
    return render_template('signup.html')


@app.route('/searchpage')
def searchpage():
    return render_template('searchpage.html')

@app.route('/link')
def link():
    return render_template('link.html')


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/back', methods=['POST', 'GET'])
def back():
    if request.method == 'POST':
        return render_template('signup.html')

