from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

    
class Blog(db.Model):
     __tablename__ = "blogger"

     def __repr__(self):
        u = self
        return f"<User id={u.id} first name={u.first_name} last name={u.last_name} image url={u.image_url}>"


     id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
     first_name = db.Column(db.String(20),
                     nullable=False)
     
     last_name = db.Column(db.String(30),
                     nullable=False)

     image_url = db.Column(db.String(80),
                     nullable=True) 
     
     po = db.relationship("Posts", back_populates="blogger", cascade="all, delete-orphan")
     
    
     def update(self, fname, lname, url):
         self.first_name=fname
         self.last_name=lname
         self.image_url=url

     def get_full_name(self):
         return f"{self.first_name} {self.last_name}"
     

class Posts(db.Model):
    __tablename__ = "posts"

    post_id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String(20))

    content = db.Column(db.String(300))

    created_at = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('blogger.id'))

    blogger = db.relationship('Blog', backref='posts' )            
    
    tags = db.relationship('Tag', secondary='post_tag', backref='posts')
 
   

    def update(self, title, content):
         self.title=title
         self.content=content

class Tag(db.Model):
    __tablename__='tags'
    t_id =db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    t_name = db.Column(db.Text)

    

    def update(self, name):
       self.t_name=name


class PostTag(db.Model):
    __tablename__='post_tag'

    post_id= db.Column(db.Integer, db.ForeignKey('posts.post_id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.t_id'), primary_key=True)
   
    

