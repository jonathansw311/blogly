from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, Blog


app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY']= "Fooster2023"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
app.config['SQLALCHEMY_ECHO']=True

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    return redirect('/bloggers')

@app.route('/bloggers')
def bloggers():
    """Shows list of all db"""
    blogger = Blog.query.order_by(Blog.first_name, Blog.last_name).all()
   
    return render_template('list.html', blogger=blogger )

@app.route('/bloggers/new')
def create():
    return render_template('create.html')

@app.route('/bloggers/new', methods=['POST'])
def add():
    fname= request.form['first_name']
    lname=request.form['last_name']
    url = request.form['url']

    new_user = Blog(first_name=fname, last_name=lname, image_url=url)

    db.session.add(new_user)
    db.session.commit()
    return redirect('/')

@app.route('/bloggers/users/<int:user_id>')
def user_info(user_id):
    user =  Blog.query.get(user_id)
    return render_template('user_info.html', user=user)    

@app.route('/bloggers/<int:user_id>/edit')
def edit_info(user_id):
    user = Blog.query.get(user_id)
    return render_template('edit_user.html', user=user )


@app.route('/bloggers/<int:user_id>/edit', methods=['POST'])
def edit_into(user_id):
    fname= request.form['first_name']
    lname=request.form['last_name']
    url = request.form['url']

    update_user = Blog.query.get(user_id)
    update_user.update(fname, lname, url)

    db.session.add(update_user)
    db.session.commit()
    return redirect('/')


@app.route('/bloggers/<int:user_id>/delete', methods=['POST'])
def remove(user_id):
    remove_user = Blog.query.get(user_id)
    db.session.delete(remove_user)
    db.session.commit()
    return redirect('/')
    