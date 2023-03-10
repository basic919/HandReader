import os


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Config:
    SECRET_KEY = '879ccaa5b99955672caef715DFEHR'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, 'database.db')
    DEBUG = True
    SQLALCHEMY_ECHO = True

    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_SENDER_ADDRESS = 'basic919@hotmail.com'
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = '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'

    FRONTEND_URL = 'http://localhost:4200/#/'   # IMPORTANT: This will depend on the actual frontend deployment URL
