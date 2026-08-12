from flask import Flask

from app.config import Config
from app.extensions import db, migrate

from app.models import League, Team, Player, Match, PlayerMatchStat, Lineup, LineupPlayer

#import blueprints for the API endpoints
from app.routes.leagues import leagues_bp
#register team api routes
from app.routes.teams import teams_bp
from app.routes.players import players_bp
from app.routes.match_team_stats import match_team_stats_bp
from app.routes.matches import matches_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints for the API endpoints
    app.register_blueprint(leagues_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(players_bp)
    app.register_blueprint(match_team_stats_bp)
    app.register_blueprint(matches_bp)
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