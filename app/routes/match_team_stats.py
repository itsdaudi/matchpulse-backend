from flask import Blueprint, request, jsonify

from app.extensions import db
from app.models import MatchTeamStats


# Blueprint for match team statistics endpoints.
match_team_stats_bp = Blueprint(
    "match_team_stats",
    __name__,
    url_prefix="/api/match-stats"
)


# GET all match team statistics.
@match_team_stats_bp.route("", methods=["GET"])
def get_match_team_stats():
    stats = MatchTeamStats.query.all()

    return jsonify({
        "match_team_stats": [
            {
                "id": stat.id,
                "match_id": stat.match_id,
                "team_id": stat.team_id,
                "possession": stat.possession,
                "shots": stat.shots,
                "shots_on_target": stat.shots_on_target,
                "shots_off_target": stat.shots_off_target,
                "corners": stat.corners,
                "fouls": stat.fouls,
                "offsides": stat.offsides,
                "yellow_cards": stat.yellow_cards,
                "red_cards": stat.red_cards,
                "passes": stat.passes,
                "pass_accuracy": stat.pass_accuracy
            }
            for stat in stats
        ]
    })


# GET one match team statistics record.
@match_team_stats_bp.route("/<int:stats_id>", methods=["GET"])
def get_match_team_stat(stats_id):
    stat = db.session.get(MatchTeamStats, stats_id)

    if not stat:
        return jsonify({"error": "Match team statistics not found"}), 404

    return jsonify({
        "id": stat.id,
        "match_id": stat.match_id,
        "team_id": stat.team_id,
        "possession": stat.possession,
        "shots": stat.shots,
        "shots_on_target": stat.shots_on_target,
        "shots_off_target": stat.shots_off_target,
        "corners": stat.corners,
        "fouls": stat.fouls,
        "offsides": stat.offsides,
        "yellow_cards": stat.yellow_cards,
        "red_cards": stat.red_cards,
        "passes": stat.passes,
        "pass_accuracy": stat.pass_accuracy
    })


# POST a new match team statistics record.
@match_team_stats_bp.route("", methods=["POST"])
def create_match_team_stats():
    data = request.get_json()

    stat = MatchTeamStats(
        match_id=data["match_id"],
        team_id=data["team_id"],
        possession=data.get("possession"),
        shots=data.get("shots"),
        shots_on_target=data.get("shots_on_target"),
        shots_off_target=data.get("shots_off_target"),
        corners=data.get("corners"),
        fouls=data.get("fouls"),
        offsides=data.get("offsides"),
        yellow_cards=data.get("yellow_cards"),
        red_cards=data.get("red_cards"),
        passes=data.get("passes"),
        pass_accuracy=data.get("pass_accuracy")
    )

    db.session.add(stat)
    db.session.commit()

    return jsonify({
        "message": "Match team statistics created successfully",
        "id": stat.id
    }), 201


# PATCH an existing match team statistics record.
@match_team_stats_bp.route("/<int:stats_id>", methods=["PATCH"])
def update_match_team_stats(stats_id):
    stat = db.session.get(MatchTeamStats, stats_id)

    if not stat:
        return jsonify({
            "error": "Match team statistics not found"
        }), 404

    data = request.get_json()

    # Update only fields supplied by the client.
    if "match_id" in data:
        stat.match_id = data["match_id"]

    if "team_id" in data:
        stat.team_id = data["team_id"]

    if "possession" in data:
        stat.possession = data["possession"]

    if "shots" in data:
        stat.shots = data["shots"]

    if "shots_on_target" in data:
        stat.shots_on_target = data["shots_on_target"]

    if "shots_off_target" in data:
        stat.shots_off_target = data["shots_off_target"]

    if "corners" in data:
        stat.corners = data["corners"]

    if "fouls" in data:
        stat.fouls = data["fouls"]

    if "offsides" in data:
        stat.offsides = data["offsides"]

    if "yellow_cards" in data:
        stat.yellow_cards = data["yellow_cards"]

    if "red_cards" in data:
        stat.red_cards = data["red_cards"]

    if "passes" in data:
        stat.passes = data["passes"]

    if "pass_accuracy" in data:
        stat.pass_accuracy = data["pass_accuracy"]

    db.session.commit()

    return jsonify({
        "message": "Match team statistics updated successfully",
        "id": stat.id
    })


# DELETE a match team statistics record.
@match_team_stats_bp.route("/<int:stats_id>", methods=["DELETE"])
def delete_match_team_stats(stats_id):
    stat = db.session.get(MatchTeamStats, stats_id)

    if not stat:
        return jsonify({
            "error": "Match team statistics not found"
        }), 404

    db.session.delete(stat)
    db.session.commit()

    return jsonify({
        "message": "Match team statistics deleted successfully"
    })