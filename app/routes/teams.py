from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.team import Team
from app.models.league import League
from app.models.player import Player


teams_bp = Blueprint("teams", __name__, url_prefix="/api/teams")


def team_to_dict(team):
    return {
        "id": team.id,
        "league_id": team.league_id,
        "name": team.name,
        "short_name": team.short_name,
        "logo": team.logo,
        "stadium": team.stadium,
    }


def player_to_dict(player, include_team=False):
    data = {
        "id": player.id,
        "team_id": player.team_id,
        "name": player.name,
        "position": player.position,
        "shirt_number": player.shirt_number,
        "nationality": player.nationality,
        "photo": player.photo,
    }
    if include_team and player.team:
        data["team"] = {
            "id": player.team.id,
            "name": player.team.name,
            "short_name": player.team.short_name,
            "logo": player.team.logo,
        }
    return data


@teams_bp.route("", methods=["GET"])
def get_teams():
    teams = Team.query.all()
    return jsonify({"teams": [team_to_dict(t) for t in teams]}), 200


@teams_bp.route("/<int:team_id>", methods=["GET"])
def get_team(team_id):
    team = db.session.get(Team, team_id)
    if not team:
        return jsonify({"error": "Team not found"}), 404
    return jsonify(team_to_dict(team)), 200


@teams_bp.route("/<int:team_id>/players", methods=["GET"])
def get_team_players(team_id):
    team = db.session.get(Team, team_id)
    if not team:
        return jsonify({"error": "Team not found"}), 404

    players = (
        Player.query.filter_by(team_id=team_id)
        .order_by(Player.position, Player.shirt_number, Player.name)
        .all()
    )
    return jsonify({
        "team": team_to_dict(team),
        "players": [player_to_dict(p) for p in players],
    }), 200


@teams_bp.route("", methods=["POST"])
def create_team():
    data = request.get_json()
    if not data or not data.get("name") or not data.get("league_id"):
        return jsonify({"error": "Team name and league_id are required"}), 400

    league = db.session.get(League, data["league_id"])
    if not league:
        return jsonify({"error": "League not found"}), 404

    team = Team(
        league_id=data["league_id"],
        name=data["name"],
        short_name=data.get("short_name"),
        logo=data.get("logo"),
        stadium=data.get("stadium"),
    )
    db.session.add(team)
    db.session.commit()

    return jsonify({
        "message": "Team created successfully",
        "team": team_to_dict(team),
    }), 201
