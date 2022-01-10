import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_login import current_user
from include import mail 


def send_reset_email(user):
    print('imhere')
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='riteshsaha004@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link.
{url_for('users.reset_token', token=token, _external=True)}
This link is valid for 30 minutes.
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

def save_picture(profile_pic):
    if current_user.image_file != 'default.jpg':
        os.remove(current_app.root_path + '\static\profilepics\\' + current_user.image_file)
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(profile_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path + '\static\profilepics\\' + picture_fn) 
    img = Image.open(profile_pic)
    img.thumbnail((125, 125))
    img.save(picture_path)
    return picture_fn