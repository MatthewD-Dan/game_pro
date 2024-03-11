from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            "id": self.id,
            "username": self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('regular_user.id'), nullable = False)
    text = db.Column(db.String(250), nullable = False)
    done = db.Column(db.Boolean, default = False)

    def __init__(self, text):
        self.text = text

    def toggle(self):
        self.done = not self.done
        db.session.add(self)
        db.session.commit()

    def toJSON(self):
        return{
            "id" : self.id,
            "text" : self.text,
            "done" : self.done
        }

class Category(db.Model):
    id =  db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(120), db.ForeignKey('regular_user.id'), nullable = False)
    text = db.Column(db.String(255), nullable =False)
    user = db.relationship('RegularUser', backref = db.backref('categories', lazy = 'joined'))
    chats = db.relationship('Chat', secondary = 'chat_category', backref = db.backref('categories', lazy = True))

    def __init__(self, user_id, text):
        self.user_id = user_id
        self.text = text

    def __repr__(self):
        return f'<Category user: {self.user.username} - {self.text}>'

    def toJSON(self):
        return{
            "id" : self.id,
            "user_id" : self.user_id,
            "user" : self.user.username,
            "text" : self.text
        }

class ChatCategory(db.Model):
    __tablename__='chat_category'
    id = db.Column(db.Integer, primary_key = True)
    chat_id = db.Column(db.String)


class RegularUser(User):
    __tablename__='regular_user'
    chats=db.relationship('Chat', backref = 'user', lazy = True)

    def add_chat(self, text):
        new_chat = Chat(text=text)
        new_chat.user_id = self.id
        self.chats.


class Admin(User):
    __tablename__='Admin'
    admin_id = db.Column(db.String(120), unique = True, nullable = False)

    def get_all_chats(self):
