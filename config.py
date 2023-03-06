from decouple import config
import os


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Config:
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, 'database.db')
    DEBUG = True
    SQLALCHEMY_ECHO = True

    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = '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'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_SENDER_ADDRESS = 'basic919@hotmail.com'
