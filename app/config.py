from flask import Flask
import os
from flask import Flask, session

class Config:
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/static/files')
    SECRET_KEY = 'supersecretkey'

def start_app():
    app = Flask(__name__)

    # Application configuration
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'files')

    # Create the upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register Blueprints
    from app.main.routes import main
    app.register_blueprint(main)

