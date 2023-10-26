from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from notesfromkatieland import db, loginManager

@loginManager.user_loader
def loadUser(userID):
    return User.query.get(int(userID))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    imageFile = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def getToken(self, expiresSeconds=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expiresSeconds)
        return s.dumps({'userID': self.id}).decode('utf-8')
    
    @staticmethod
    def verifyToken(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            userID = s.loads(token)['userID']
        except:
            return None
        return User.query.get(userID)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.imageFile}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    datePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.datePosted}')"
    
class AllowedUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"AllowedUser('{self.name}', '{self.email}')"
