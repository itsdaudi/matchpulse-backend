from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.player import Player
from app.models.team import Team


# Blueprint containing all player-related API endpoints.
players_bp = Blueprint(
    "players",
    __name__,
    url_prefix="/api/players"
)


@players_bp.route("", methods=["GET"])
def get_players():
    """
    Return all players stored in the database.
    """

    players = Player.query.all()

    return jsonify({
        "players": [
            {
                "id": player.id,
                "team_id": player.team_id,
                "name": player.name,
                "position": player.position,
                "shirt_number": player.shirt_number,
                "nationality": player.nationality,
                "photo": player.photo
            }
            for player in players
        ]
    }), 200


@players_bp.route("/<int:player_id>", methods=["GET"])
def get_player(player_id):
    """
    Return one player using their ID.
    """

    player = db.session.get(Player, player_id)

    if not player:
        return jsonify({
            "error": "Player not found"
        }), 404

    return jsonify({
        "id": player.id,
        "team_id": player.team_id,
        "name": player.name,
        "position": player.position,
        "shirt_number": player.shirt_number,
        "nationality": player.nationality,
        "photo": player.photo
    }), 200


@players_bp.route("", methods=["POST"])
def create_player():
    """
    Create a new player and associate them with a team.
    """

    data = request.get_json()

    # Check that the required information was provided.
    if not data or not data.get("name") or not data.get("team_id"):
        return jsonify({
            "error": "Player name and team_id are required"
        }), 400

    # Make sure the team exists before creating the player.
    team = db.session.get(Team, data["team_id"])

    if not team:
        return jsonify({
            "error": "Team not found"
        }), 404

    # Create the player.
    player = Player(
        team_id=data["team_id"],
        name=data["name"],
        position=data.get("position"),
        shirt_number=data.get("shirt_number"),
        nationality=data.get("nationality"),
        photo=data.get("photo")
    )

    db.session.add(player)
    db.session.commit()

    return jsonify({
        "message": "Player created successfully",
        "player": {
            "id": player.id,
            "team_id": player.team_id,
            "name": player.name,
            "position": player.position,
            "shirt_number": player.shirt_number,
            "nationality": player.nationality,
            "photo": player.photo
        }
    }), 201