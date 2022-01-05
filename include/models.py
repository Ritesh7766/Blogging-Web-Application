from include import db, bcrypt
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(length = 40), nullable = False, unique = True)
    image_file = db.Column(db.String(length = 80), nullable = False, default = 'default.jpg')
    email = db.Column(db.String(length = 50), nullable = False, unique = True)
    password = db.Column(db.String(length = 80), nullable = False)
    posts = db.relationship('Post', backref = 'author', lazy = True)

    def __repr__(self):
        return f'{self.username}, {self.image_file}, {self.email}'

    @property
    def password(self):
        return self.password

    @password.setter
    def passoword(self, plain_text_password):
        self.password = bcrypt(plain_text_password).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(length = 1024), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f'{self.title}, {self.date_posted}'