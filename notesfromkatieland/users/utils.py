import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from notesfromkatieland import mail

def savePicture(formPicture):
    randomHex = secrets.token_hex(8)
    _, fext = os.path.splitext(formPicture.filename)
    fname = randomHex + fext
    fpath = os.path.join(current_app.root_path, 'static', 'profile_pics', fname)

    outputSize = (125, 125)
    img = Image.open(formPicture)
    img.thumbnail(outputSize)
    img.save(fpath)

    return fname

def sendConfEmail(user):
    token = user.getToken()
    msg = Message('Confirm your account on notesfromkatieland.com', sender='noreply@notesfromkatieland.com', recipients=[user.email])
    msg.body = f'''Thank you for registering! To confirm your account, please vist the following link:
{url_for('users.confirm', token=token, _external=True)}

If you did not create an account, ignore this email and no changes will be made.
'''
    mail.send(msg)

def sendResetEmail(user):
    token = user.getToken()
    msg = Message('Password Reset Request for notesfromkatieland.com', sender='noreply@notesfromkatieland.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.resetToken', token=token, _external=True)}

If you did not make this request, ignore this email and no changes will be made.
'''
    mail.send(msg)