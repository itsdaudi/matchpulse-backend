from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.team import Team
from app.models.league import League


# Blueprint containing all team-related API endpoints.
teams_bp = Blueprint("teams", __name__, url_prefix="/api/teams")


@teams_bp.route("", methods=["GET"])
def get_teams():
    """
    Return all teams stored in the database.
    """

    teams = Team.query.all()

    return jsonify({
        "teams": [
            {
                "id": team.id,
                "league_id": team.league_id,
                "name": team.name,
                "short_name": team.short_name,
                "logo": team.logo,
                "stadium": team.stadium
            }
            for team in teams
        ]
    }), 200


@teams_bp.route("/<int:team_id>", methods=["GET"])
def get_team(team_id):
    """
    Return one team using its ID.
    """

    team = db.session.get(Team, team_id)

    if not team:
        return jsonify({
            "error": "Team not found"
        }), 404

    return jsonify({
        "id": team.id,
        "league_id": team.league_id,
        "name": team.name,
        "short_name": team.short_name,
        "logo": team.logo,
        "stadium": team.stadium
    }), 200


@teams_bp.route("", methods=["POST"])
def create_team():
    """
    Create a new team and associate it with a league.
    """

    data = request.get_json()

    # Make sure the request contains the required fields.
    if not data or not data.get("name") or not data.get("league_id"):
        return jsonify({
            "error": "Team name and league_id are required"
        }), 400

    # Check that the requested league actually exists.
    league = db.session.get(League, data["league_id"])

    if not league:
        return jsonify({
            "error": "League not found"
        }), 404

    # Create the new team.
    team = Team(
        league_id=data["league_id"],
        name=data["name"],
        short_name=data.get("short_name"),
        logo=data.get("logo"),
        stadium=data.get("stadium")
    )

    db.session.add(team)
    db.session.commit()

    return jsonify({
        "message": "Team created successfully",
        "team": {
            "id": team.id,
            "league_id": team.league_id,
            "name": team.name,
            "short_name": team.short_name,
            "logo": team.logo,
            "stadium": team.stadium
        }
    }), 201