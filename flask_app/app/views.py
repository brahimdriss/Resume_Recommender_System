# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

# Python modules
import os, logging 

# Flask modules
from flask               import render_template, request, url_for, redirect, send_from_directory
from flask_login         import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort

# App modules
from app        import app, lm, db, bc
from app.models import User
from app.forms  import LoginForm, RegisterForm


import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
import pickle as pkl
from sklearn.neighbors import NearestNeighbors
import numpy as np
from json2html import *
from VFR import *
from RAG import *

# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Logout user
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Register a new user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    
    # declare the Registration Form
    form = RegisterForm(request.form)

    msg = None

    if request.method == 'GET': 

        return render_template( 'pages/register.html', form=form, msg=msg )

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 
        email    = request.form.get('email'   , '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'
        
        else:         

            pw_hash = password #bc.generate_password_hash(password)

            user = User(username, email, pw_hash)

            user.save()

            msg = 'User created, please <a href="' + url_for('login') + '">login</a>'     

    else:
        msg = 'Input error'     

    return render_template( 'pages/register.html', form=form, msg=msg )

# Authenticate user
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    
    # Declare the login form
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        if user:
            
            #if bc.check_password_hash(user.password, password):
            if user.password == password:
                login_user(user)
                


                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unknown user"

    return render_template( 'pages/login.html', form=form, msg=msg )





@app.route('/predict',methods=['POST'])
def predict():
                    ####
    model = Mods()
    with open(r"finaldf_2.pkl", "rb") as input_file:
        data = pkl.load(input_file)
    model.fit(data=data)
    ####
    

    switcher={
                "web_back_end": model.backend,
                "Developpeur Front-End":model.frontend,
                'embarque':model.embarque,
                'tech_jee':model.tech_jee,
                'fullstack':model.fullstack,
                'jee':model.jee,
                'symfony':model.symfony,
                'drupal':model.drupal,
                'product_owner':model.product_owner
        
             }
    
    
    
    if request.method == 'POST':
        comment = request.form['comment']
        people = request.form.getlist('hello')
        print(people)
        print(switcher.get(comment,"Invalid day of week"))
        model.extract_profile(switcher.get(comment,"Invalid day of week"),people)
        model.k_best(switcher.get(comment,"Invalid day of week"),int(request.form['number_p']),people)
		#vect = cv.transform(data).toarray()
	    

    return render_template('pages/resultaa.html',ps=model)


@app.route('/tabb',methods=['POST'])
def tabb():
    model = Mods()
    with open(r"finaldf_2.pkl", "rb") as input_file:
        data = pkl.load(input_file)
    
    model.fit(data=data)
    if request.method == 'POST':
        commentx = request.form['ccc']
        ss=model.get_profile_clean(int(commentx))
    
        l = []
        for i in ss.keys():
            i = i[7:]
            l.append(i)
        l = np.array(l)
        ll = []
        for i in ss.keys():
            ll.append(ss[i])
        d = {'Profile': l, 'Score': ll}
        df = pd.DataFrame(data=d).sort_values(by=["Score"], ascending=False)

    return render_template('pages/tabbb.html',ps=df,cc=int(commentx))


@app.route('/prof/<id>')
def prof(id=None):
    ids = int(id)

    model = Mods()
    with open(r"finaldf_2.pkl", "rb") as input_file:
        data = pkl.load(input_file)
    model.fit(data=data)
    
    commentx = ids
    ss = model.get_profile_clean(int(commentx))

    l = []
    for i in ss.keys():
        i = i[7:]
        l.append(i)
    l = np.array(l)
    ll = []
    for i in ss.keys():
        ll.append(ss[i])
    d = {'Profile': l, 'Score': ll}
    df = pd.DataFrame(data=d).sort_values(by=["Score"], ascending=False)

    return render_template('pages/tabbb.html', ps=df, cc=int(commentx))



@app.route('/tables.html')
def tables():
    model = Mods()
    with open(r"finaldf_2.pkl", "rb") as input_file:
        data = pkl.load(input_file)
    model.fit(data=data)    
    return render_template('pages/tables.html',ps=model)


@app.route('/displ/<id>')
def displ(id=None):
    with open(r"dummy.pkl", "rb") as input_file:
        data = pkl.load(input_file)
    ss = data.iloc[int(id)]
    name = ss["personal_info"]["name"]
    url = ss["url"]
    p_info = json2html.convert(
        json=ss["personal_info"], table_attributes="id=\"table\" class=\"table striped\"")
    skills = json2html.convert(
        json=ss["skills"], table_attributes="id=\"table\" class=\"table striped\"")
    exp = json2html.convert(
        json=ss["experiences"], table_attributes="id=\"table\" class=\"table striped\"")
    inter = json2html.convert(
        json=ss["interests"], table_attributes="id=\"table\" class=\"table striped\"")
    acc = json2html.convert(
        json=ss["accomplishments"], table_attributes="id=\"table\" class=\"table striped\"")
    # model = Mods()
    # with open(r"finaldf_2.pkl", "rb") as input_file:
    #     data = pkl.load(input_file)

    # model.fit(data=data)
    # if request.method == 'POST':
    #     commentx = request.form['ccc']
    #     tt = model.get_profile(int(commentx))
    return render_template('pages/displ.html',ids=id,
                                            url = url,
                                            p_info=p_info,
                                            skills=skills,
                                            exp=exp,
                                            inter=inter,
                                            acc=acc,
                                            name= name)

    
    
    
    
# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    content = None

    try:

        # try to match the pages defined in -> pages/<input file>
        return render_template( 'pages/'+path )
    
    except:
        
        return render_template( 'pages/error-404.html' )

# Return sitemap 
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')
