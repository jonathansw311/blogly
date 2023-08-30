from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

    
class Blog(db.Model):
     __tablename__ = "blogger"

     def __repr__(self):
        u = self
        return f"<Pet id={u.id} first name={u.first_name} last name={u.last_name} image url={u.image_url}>"


     id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
     first_name = db.Column(db.String(20),
                     nullable=False)
     
     last_name = db.Column(db.String(30),
                     nullable=False)

     image_url = db.Column(db.String(80),
                     nullable=True) 
    
     def update(self, fname, lname, url):
         self.first_name=fname
         self.last_name=lname
         self.image_url=url

     def get_full_name(self):
         return f"{self.first_name} {self.last_name}"
        