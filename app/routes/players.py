from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.player import Player
from app.models.team import Team
from app.models.player_match_stat import PlayerMatchStat


players_bp = Blueprint("players", __name__, url_prefix="/api/players")


def team_brief(team):
    if not team:
        return None
    return {
        "id": team.id,
        "name": team.name,
        "short_name": team.short_name,
        "logo": team.logo,
    }


def player_to_dict(player):
    return {
        "id": player.id,
        "team_id": player.team_id,
        "name": player.name,
        "position": player.position,
        "shirt_number": player.shirt_number,
        "nationality": player.nationality,
        "photo": player.photo,
        "team": team_brief(player.team),
    }


@players_bp.route("", methods=["GET"])
def get_players():
    query = Player.query

    team_id = request.args.get("team_id")
    if team_id:
        try:
            query = query.filter(Player.team_id == int(team_id))
        except ValueError:
            return jsonify({"error": "team_id must be an integer"}), 400

    q = request.args.get("q")
    if q:
        query = query.filter(Player.name.ilike(f"%{q.strip()}%"))

    players = query.order_by(Player.name).all()
    return jsonify({"players": [player_to_dict(p) for p in players]}), 200


@players_bp.route("/<int:player_id>", methods=["GET"])
def get_player(player_id):
    player = db.session.get(Player, player_id)
    if not player:
        return jsonify({"error": "Player not found"}), 404

    stats = (
        PlayerMatchStat.query.filter_by(player_id=player_id)
        .order_by(PlayerMatchStat.id.desc())
        .limit(20)
        .all()
    )
    recent_stats = [
        {
            "id": s.id,
            "match_id": s.match_id,
            "minutes_played": s.minutes_played,
            "started": s.started,
            "goals": s.goals,
            "assists": s.assists,
            "yellow_cards": s.yellow_cards,
            "red_cards": s.red_cards,
            "shots": s.shots,
            "shots_on_target": s.shots_on_target,
            "passes": s.passes,
            "pass_accuracy": s.pass_accuracy,
            "tackles": s.tackles,
        }
        for s in stats
    ]

    data = player_to_dict(player)
    data["recent_stats"] = recent_stats
    return jsonify(data), 200


@players_bp.route("/<int:player_id>", methods=["PATCH"])
def update_player(player_id):
    player = db.session.get(Player, player_id)
    if not player:
        return jsonify({"error": "Player not found"}), 404

    data = request.get_json() or {}
    if "name" in data:
        player.name = data["name"]
    if "team_id" in data:
        team = db.session.get(Team, data["team_id"])
        if not team:
            return jsonify({"error": "Team not found"}), 404
        player.team_id = data["team_id"]
    if "position" in data:
        player.position = data["position"]
    if "shirt_number" in data:
        player.shirt_number = data["shirt_number"]
    if "nationality" in data:
        player.nationality = data["nationality"]
    if "photo" in data:
        player.photo = data["photo"]

    db.session.commit()
    return jsonify({
        "message": "Player updated successfully",
        "player": player_to_dict(player),
    }), 200


@players_bp.route("/<int:player_id>", methods=["DELETE"])
def delete_player(player_id):
    player = db.session.get(Player, player_id)
    if not player:
        return jsonify({"error": "Player not found"}), 404
    db.session.delete(player)
    db.session.commit()
    return jsonify({"message": "Player deleted successfully"}), 200


@players_bp.route("", methods=["POST"])
def create_player():
    data = request.get_json() or {}
    if not data.get("name") or not data.get("team_id"):
        return jsonify({"error": "Player name and team_id are required"}), 400

    team = db.session.get(Team, data["team_id"])
    if not team:
        return jsonify({"error": "Team not found"}), 404

    player = Player(
        team_id=data["team_id"],
        name=data["name"],
        position=data.get("position") or "Midfielder",
        shirt_number=data.get("shirt_number"),
        nationality=data.get("nationality"),
        photo=data.get("photo"),
    )
    db.session.add(player)
    db.session.commit()

    return jsonify({
        "message": "Player created successfully",
        "player": player_to_dict(player),
    }), 201
