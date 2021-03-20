from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(64))
 
    def __init__(self, email, password):
        self.email = email
        self.password = password
