from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
from flask_migrate import Migrate
import os
import urllib.parse
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jfdcbgfcxdgfddfgbgffhdhsjdf'
CORS(app, supports_credentials=True, origins="http://localhost:5173")
DATABASE_URL = os.getenv("supabase_url")

if DATABASE_URL:
    # Extract the password from the URL
    password_start = DATABASE_URL.find(':', DATABASE_URL.find('://') + 3) + 1
    password_end = DATABASE_URL.find('@', password_start)
    password = DATABASE_URL[password_start:password_end]

    # URL-encode the password to handle special characters
    encoded_password = urllib.parse.quote(password)

    # Rebuild the DATABASE_URL with the encoded password
    DATABASE_URL = DATABASE_URL[:password_start] + encoded_password + DATABASE_URL[password_end:]

    # Set the SQLAlchemy database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
    print("DATABASE_URL not set in environment")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

#login_manager.login_view = ('login')
#login_manager.login_message_category = 'info'
from server import models
with app.app_context():
    db.create_all()

from server import routes