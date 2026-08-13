from flask import Blueprint, request, jsonify

from app.extensions import db
from app.models import Lineup, LineupPlayer


lineups_bp = Blueprint(
    "lineups",
    __name__,
    url_prefix="/api/lineups"
)


def lineup_player_to_dict(lineup_player):
    """Convert a LineupPlayer into a JSON-friendly dictionary."""
    return {
        "id": lineup_player.id,
        "player": {
            "id": lineup_player.player.id,
            "name": lineup_player.player.name,
            "nationality": lineup_player.player.nationality,
            "position": lineup_player.player.position,
            "photo": lineup_player.player.photo
        },
        "position": lineup_player.position,
        "position_x": lineup_player.position_x,
        "position_y": lineup_player.position_y,
        "starter": lineup_player.starter,
        "shirt_number": lineup_player.shirt_number
    }


def lineup_to_dict(lineup):
    """Convert a Lineup into a JSON-friendly dictionary."""
    return {
        "id": lineup.id,
        "match_id": lineup.match_id,

        "team": {
            "id": lineup.team.id,
            "name": lineup.team.name,
            "short_name": lineup.team.short_name,
            "logo": lineup.team.logo
        },

        "formation": lineup.formation,

        "players": [
            lineup_player_to_dict(player)
            for player in lineup.lineup_players
        ]
    }


# GET all lineups
@lineups_bp.route("", methods=["GET"])
def get_lineups():
    lineups = Lineup.query.all()

    return jsonify({
        "lineups": [
            lineup_to_dict(lineup)
            for lineup in lineups
        ]
    })


# GET one lineup
@lineups_bp.route("/<int:lineup_id>", methods=["GET"])
def get_lineup(lineup_id):
    lineup = db.session.get(Lineup, lineup_id)

    if not lineup:
        return jsonify({
            "error": "Lineup not found"
        }), 404

    return jsonify(lineup_to_dict(lineup))


# POST a lineup
@lineups_bp.route("", methods=["POST"])
def create_lineup():
    data = request.get_json()

    lineup = Lineup(
        match_id=data["match_id"],
        team_id=data["team_id"],
        formation=data["formation"]
    )

    db.session.add(lineup)
    db.session.commit()

    return jsonify({
        "message": "Lineup created successfully",
        "lineup": lineup_to_dict(lineup)
    }), 201


# POST a player into a lineup
@lineups_bp.route("/<int:lineup_id>/players", methods=["POST"])
def add_player_to_lineup(lineup_id):
    lineup = db.session.get(Lineup, lineup_id)

    if not lineup:
        return jsonify({
            "error": "Lineup not found"
        }), 404

    data = request.get_json()

    lineup_player = LineupPlayer(
        lineup_id=lineup_id,
        player_id=data["player_id"],
        position=data["position"],
        position_x=data.get("position_x"),
        position_y=data.get("position_y"),
        starter=data.get("starter", True),
        shirt_number=data.get("shirt_number")
    )

    db.session.add(lineup_player)
    db.session.commit()

    return jsonify({
        "message": "Player added to lineup successfully",
        "player": lineup_player_to_dict(lineup_player)
    }), 201