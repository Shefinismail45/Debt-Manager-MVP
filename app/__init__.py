from flask import Flask
from .extensions import db
from .routes import bp


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=r"sqlite:///C:/Users/HP/personal-finance-mvp/personal_finance.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)

    # automatically create database + tables on startup
    with app.app_context():
        db.create_all()

    app.register_blueprint(bp)

    return app
