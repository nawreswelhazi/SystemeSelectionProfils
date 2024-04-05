# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 17:14:38 2023

@author: NAWRESS
"""


from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import engine
from LoginDB import *
from UsersGestion import *
from Filtre import *
import os
app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
        
    else:
        return render_template('Selection.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
        #récupérer le role de l'utilisateur
        output = s.execute("SELECT isAdmin FROM users where username = '"+POST_USERNAME+"' and password = '"+POST_PASSWORD +"'")
        res = (output.fetchone())[0]
        if res == 0:
            return SearchCandidates()
        else:
            return addRecruter(res)
    else:
        flash('wrong password!')
        return home()

@app.route('/signup')
def signup():
   return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def addAccount():
   POST_USERNAME = str(request.form['username'])
   POST_NAME = str(request.form['name'])
   POST_FAMILYNAME = str(request.form['familyname'])
   POST_PASSWORD = str(request.form['password'])
   POST_PASSWORDCONFIRMED = str(request.form['passwordConfirmed'])
   Session = sessionmaker(bind=engine)
   s = Session()
   query = s.query(User).filter(User.username.in_([POST_USERNAME]))
   result = query.first()
   if result:
       flash('this username already exists!')
       return signup()
   elif POST_PASSWORDCONFIRMED != POST_PASSWORD:
       flash('Check your password!')
       return signup()
   else:
       AddUser(POST_USERNAME, POST_NAME, POST_FAMILYNAME, POST_PASSWORD)
       flash('Accound added')
       session['logged_in'] = True
       output = s.execute("SELECT isAdmin FROM users where username = '"+POST_USERNAME+"' and password = '"+POST_PASSWORD +"'")
       res = (output.fetchone())[0]
       return addRecruter(res)   

@app.route('/addRecruter')
def addRecruter(res=0):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if res == 0:
            return SearchCandidates()
        else:
            return render_template('Selection.html')
        
        
        
@app.route("/Selectskills",methods=["POST"])
def selectskill():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        skills = request.form.getlist("skill[]")
        skillsMinis = list((map(lambda x: x.lower(), skills)))
        scores= list(map(int, request.form.getlist('score[]')))
        exigences = dict(zip(skillsMinis, scores))
        AllScores = FindAllScores(exigences)
        return Selection(AllScores)


@app.route('/Affichage')
def Selection(AllScores):
   return render_template('affichage.html', Scores=AllScores)

@app.route('/pdf', methods=["GET"])
def GetPDF():
    name = str(request.get('pdf'))
    pdf_dir = glob('C:/Users/NAWRESS/python/CVS/*.pdf')
    for pdf_file in pdf_dir:
        nomProfil = pdf_file.split('\\')[-1]
        nomProfil = nomProfil.split('.pdf')[0]
        if name in pdf_file:
            webbrowser.open(f'{pdf_file}')
        
    
@app.route('/SearchCandidates')
def SearchCandidates():
    if not session.get('logged_in') :
        return render_template('login.html')
    else:
        return "Hello Recruter! <a href='/logout'>Logout</a>"


@app.route('/back')
def goback():
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

    
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=False)
