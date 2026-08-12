from flask import Blueprint, request, jsonify

from app.extensions import db
from app.models import Match


# Blueprint for match endpoints.
matches_bp = Blueprint(
    "matches",
    __name__,
    url_prefix="/api/matches"
)


def match_to_dict(match):
    """Convert a Match object into a JSON-friendly dictionary."""
    return {
        "id": match.id,
        "league_id": match.league_id,
        "home_team_id": match.home_team_id,
        "away_team_id": match.away_team_id,
        "match_date": match.match_date.isoformat(),
        "venue": match.venue,
        "status": match.status,
        "home_score": match.home_score,
        "away_score": match.away_score
    }


# GET all matches.
@matches_bp.route("", methods=["GET"])
def get_matches():
    matches = Match.query.all()

    return jsonify({
        "matches": [match_to_dict(match) for match in matches]
    })


# GET one match by ID.
@matches_bp.route("/<int:match_id>", methods=["GET"])
def get_match(match_id):
    match = db.session.get(Match, match_id)

    if not match:
        return jsonify({
            "error": "Match not found"
        }), 404

    return jsonify(match_to_dict(match))


# POST a new match.
@matches_bp.route("", methods=["POST"])
def create_match():
    data = request.get_json()

    match = Match(
        league_id=data["league_id"],
        home_team_id=data["home_team_id"],
        away_team_id=data["away_team_id"],
        match_date=data["match_date"],
        venue=data.get("venue"),
        status=data.get("status", "scheduled"),
        home_score=data.get("home_score", 0),
        away_score=data.get("away_score", 0)
    )

    db.session.add(match)
    db.session.commit()

    return jsonify({
        "message": "Match created successfully",
        "match": match_to_dict(match)
    }), 201


# PATCH an existing match.
@matches_bp.route("/<int:match_id>", methods=["PATCH"])
def update_match(match_id):
    match = db.session.get(Match, match_id)

    if not match:
        return jsonify({
            "error": "Match not found"
        }), 404

    data = request.get_json()

    # Update only the fields supplied by the client.
    if "league_id" in data:
        match.league_id = data["league_id"]

    if "home_team_id" in data:
        match.home_team_id = data["home_team_id"]

    if "away_team_id" in data:
        match.away_team_id = data["away_team_id"]

    if "match_date" in data:
        match.match_date = data["match_date"]

    if "venue" in data:
        match.venue = data["venue"]

    if "status" in data:
        match.status = data["status"]

    if "home_score" in data:
        match.home_score = data["home_score"]

    if "away_score" in data:
        match.away_score = data["away_score"]

    db.session.commit()

    return jsonify({
        "message": "Match updated successfully",
        "match": match_to_dict(match)
    })


# DELETE a match.
@matches_bp.route("/<int:match_id>", methods=["DELETE"])
def delete_match(match_id):
    match = db.session.get(Match, match_id)

    if not match:
        return jsonify({
            "error": "Match not found"
        }), 404

    db.session.delete(match)
    db.session.commit()

    return jsonify({
        "message": "Match deleted successfully"
    })