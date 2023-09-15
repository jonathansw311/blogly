from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, Blog, Posts, Tag, PostTag
import datetime



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
    posts = Posts.query.order_by(Posts.post_id.desc()).limit(5).all()
    return render_template('list.html', blogger=blogger, posts=posts )

@app.route('/bloggers/new')
def create():
    """Loads the create.html to create a new blogger"""
    return render_template('create.html')

@app.route('/bloggers/new', methods=['POST'])
def add():
    """receives the post information to create a new blogger and creates it, and commits it to the db"""
    fname= request.form['first_name']
    lname=request.form['last_name']
    url = request.form['url']

    new_user = Blog(first_name=fname, last_name=lname, image_url=url)

    db.session.add(new_user)
    db.session.commit()
    return redirect('/')

@app.route('/bloggers/<int:users_id>')
def user_info(users_id):
    """retreives the specifed user and their post to show what posts a user has created"""
    user =  Blog.query.get(users_id)
    posts= Posts.query.filter(Posts.user_id==users_id)
    return render_template('user_info.html', user=user, posts=posts)    

@app.route('/bloggers/<int:users_id>/post/new')
def addPost(users_id):
    """creates an add post form for a specified blogger"""
    user = Blog.query.get(users_id)
    tags = Tag.query.all()
    return render_template('add_post.html', user=user, tags=tags)


@app.route('/bloggers/<int:user_id>/edit')
def edit_info(user_id):
    """creates a edit blogger form for the requested blogger"""
    user = Blog.query.get(user_id)
    return render_template('edit_user.html', user=user )

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Edits a specific  post based on the passed in post_id"""
    post = Posts.query.get(post_id)
    tags = Tag.query.all()
    p= []
    for post in post.tags:
         p.append(post.t_id)
    post = Posts.query.get(post_id)
    return render_template('edit_post.html', tags = tags, post=post, p=p )


@app.route('/bloggers/<int:user_id>/edit', methods=['POST'])
def edit_into(user_id):
    """Updates a users information that has been posted in from a form"""
    fname= request.form['first_name']
    lname=request.form['last_name']
    url = request.form['url']
    
    update_user = Blog.query.get(user_id)
    update_user.update(fname, lname, url)
    
    app.logger.info('hello')
    db.session.add(update_user)
    db.session.commit()
    return redirect('/')

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def editspost(post_id):
    """Edits a post based on a post id that has been passed in from a form"""
    """it also removes old tags and adds in new ones based on what is selected"""
    delete_post = Posts.query.get(post_id)
    delete_post.tags.clear()
         
        
    title = request.form['Title']
    content = request.form['Content']
    selected_options = request.form.getlist('selected_options')
    update_post = Posts.query.get(post_id)
    update_post.update(title, content)
    db.session.add(update_post)
    db.session.commit()
    #many to many loop.  Is this the best way to do this?
    for tags in selected_options:
        new_join = PostTag(post_id=post_id, tag_id=tags)
        db.session.add(new_join)
        db.session.commit()
    return redirect(f'/posts/{post_id}')


@app.route('/bloggers/<int:users_id>/post/new', methods=['POST'])
def addtodb(users_id):
    """creates a new post and inserts the users id into the post FK and also formats the time it was created.  the post info has been passed from a form in a post request"""
    """You can also select tags when adding the post"""
    title= request.form['Title']
    content=request.form['Post Content']
    now= datetime.datetime.now()
    ftime = now.strftime("%-m-%-d-%Y %-I:%M%p")
    new_post = Posts(title=title, content=content, created_at= ftime, user_id=users_id)
    selected_options = request.form.getlist('selected_options')
    db.session.add(new_post)
    db.session.commit()
    #many to many loop.  Is this the best way to do this?
    for tags in selected_options:
        new_join = PostTag(post_id=new_post.post_id, tag_id=tags)
        db.session.add(new_join)
        db.session.commit()
    return redirect(f'/bloggers/{users_id}')    

@app.route('/bloggers/<int:user_id>/delete', methods=['POST'])
def remove(user_id):
    """Deletes a user based on a passed in from a button from a form"""
    remove_user = Blog.query.get(user_id)
    db.session.delete(remove_user)
    db.session.commit()
    return redirect('/')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def removePost(post_id):
    """removes a post based on a post id passed in from a button from a form"""
    remove_post = Posts.query.get(post_id)
    user_id = remove_post.user_id
    db.session.delete(remove_post)
    db.session.commit()
    return redirect(f'/bloggers/{user_id}')

@app.route('/posts/<int:post_id>')
def getPost(post_id):
    """displays a post id.  It can also get the blogger as the blogger id is joined in the post fk"""
    """It also gets the tags that are stored in POSTS as they are backref through PostTag relationship"""
    post = Posts.query.get(post_id)
        
    return render_template('post.html', post=post)   

@app.route('/tags')
def displayTags():
    """Displays all availaable tags"""
    tags = Tag.query.all() 
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:t_id>')
def edittag(t_id):
    """Displays the tag information in the edit tag page"""
    tag= Tag.query.get(t_id)
    return render_template('edit_tag.html', tag = tag)

@app.route('/tags/new', methods=['GET', 'POST'])
def CreateTags():
    """if it a get request it renders the add tag page"""
    """The add tag page lets you crate a Tag and you can assign it to any post"""
    if request.method == 'GET':
     post = Posts.query.all()
     return render_template('add_tags.html', posts=post)
     """If it is a post request it creates the tag and the logic for """
     """Adding the tag to other posts and redirects to the tag page"""
    else:
        newTag = request.form['new_tag']
        selected_options = request.form.getlist('selected_options')
        new = Tag(t_name=newTag)
        db.session.add(new)
        db.session.commit()
        
        for titles in selected_options:
         new_join = PostTag(post_id=titles, tag_id=new.t_id)
         db.session.add(new_join)
         db.session.commit()
        


        return redirect('/tags')
    
@app.route('/tags/<int:t_id>/edit', methods=['POST'])
def editlgc(t_id):
    """Logic for updating a tag route"""
    new_tag = request.form['Tag']
    update_tag = Tag.query.get(t_id)
    update_tag.update(new_tag)
    db.session.add(update_tag)
    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<int:t_id>/delete')
def deltag(t_id):
    """Deletes the selected tag from the database"""
    del_tag = Tag.query.get(t_id)
    db.session.delete(del_tag)
    db.session.commit()
    return redirect('/tags')

