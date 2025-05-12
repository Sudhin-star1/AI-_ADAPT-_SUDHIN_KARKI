from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

# Initialize the SQLAlchemy extension instance.
# This will be used to define models and interact with the database.
db = SQLAlchemy()

def create_app():
    """
    Factory function to create and configure the Flask app.
    """
    # Initialize the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize SQLAlchemy with the Flask app
    db.init_app(app)

    # Import the Blueprints for different routes (web, api, test)
    from .routes.web import web_bp
    from .routes.api import api_bp
    from .routes.test import test_bp

    # Register the Blueprints with the Flask app
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(test_bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
