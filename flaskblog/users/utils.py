import os  # to grab file extension in save_picture function
import secrets  # to hash pic name, to get a unique name
from PIL import Image  # to resize pics to 125px
from flask import url_for  # if there is a change in the root URL then you have to change it in every page where the link is present
from flask import current_app  # instead of app from flaskblog
from flask_mail import Message  # necessary class to provide mail sending functionality
from flaskblog import mail  # variables(instances of classes) from __init__


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)  # form_picture: data from the field that the user submits
    picture_fn = random_hex + f_ext                     # _ is variable that you don't gonna use in your program
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)  # safe method to create path

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)
# there must be no indentation (it will display the same way on screen, _external=True -> in order to get absolut url, not relative url (link in an email needs to have full domain)