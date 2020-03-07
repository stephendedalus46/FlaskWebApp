# cut/paste from __init__ (app.config['SECRET_KEY']... etc
import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')  # will protect against modifying cookies, cross-site request forgery attacks
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')  # /// are relative path from the current file, site.db will be in our directory
    MAIL_SERVER = 'smtp.googlemail.com'  # 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')  # setting email as an environment variable
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')  # setting password as an environment variable
