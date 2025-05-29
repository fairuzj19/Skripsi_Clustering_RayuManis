from flask import Flask
from app.config import Config
from app.main import main as main_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Import and register blueprints
    
    app.register_blueprint(main_blueprint)

    return app