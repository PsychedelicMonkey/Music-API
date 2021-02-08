import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'create-a-secret-key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'create-a-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ITEMS_PER_PAGE = 10
    MAX_ITEMS_PER_PAGE = 30
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(basedir, 'uploads')
    ALLOWED_FILE_EXTENSIONS = ['png', 'jpg', 'jpeg']

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'