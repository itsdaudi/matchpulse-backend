from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.league import League


# Blueprint containing all league-related API endpoints.
leagues_bp = Blueprint("leagues", __name__, url_prefix="/api/leagues")


@leagues_bp.route("", methods=["GET"])
def get_leagues():
    """
    Return all leagues stored in the database.
    """

    leagues = League.query.all()

    return jsonify({
        "leagues": [
            {
                "id": league.id,
                "name": league.name,
                "country": league.country,
                "logo": league.logo
            }
            for league in leagues
        ]
    }), 200


@leagues_bp.route("/<int:league_id>", methods=["GET"])
def get_league(league_id):
    """
    Return one league using its ID.
    """

    league = db.session.get(League, league_id)

    if not league:
        return jsonify({
            "error": "League not found"
        }), 404

    return jsonify({
        "id": league.id,
        "name": league.name,
        "country": league.country,
        "logo": league.logo
    }), 200


@leagues_bp.route("", methods=["POST"])
def create_league():
    """
    Create a new league.
    """

    data = request.get_json()

    if not data or not data.get("name"):
        return jsonify({
            "error": "League name is required"
        }), 400

    league = League(
        name=data["name"],
        country=data.get("country"),
        logo=data.get("logo")
    )

    db.session.add(league)
    db.session.commit()

    return jsonify({
        "message": "League created successfully",
        "league": {
            "id": league.id,
            "name": league.name,
            "country": league.country,
            "logo": league.logo
        }
    }), 201