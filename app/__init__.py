from flask import Flask

from app.config import Config
from app.extensions import db, migrate

from app.models import League, Team
def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/")
    def home():
        return {
            "message": "Welcome to MatchPulse API",
            "status": "running"
        }

    @app.route("/db-test")
    def db_test():
        try:
            db.session.execute(db.text("SELECT 1"))
            return {
                "database": "connected",
                "status": "success"
            }
        except Exception as e:
            return {
                "database": "connection failed",
                "error": str(e)
            }, 500

    return app