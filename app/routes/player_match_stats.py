from flask import Blueprint, request, jsonify

from app.extensions import db
from app.models.player_match_stat import PlayerMatchStat

player_match_stats_bp = Blueprint(
    "player_match_stats",
    __name__,
    url_prefix="/api/player-match-stats"
)


def stats_to_dict(stats):
    """Convert a PlayerMatchStat object into JSON."""
    return {
        "id": stats.id,
        "match_id": stats.match_id,
        "player_id": stats.player_id,
        "minutes_played": stats.minutes_played,
        "started": stats.started,
        "goals": stats.goals,
        "assists": stats.assists,
        "yellow_cards": stats.yellow_cards,
        "red_cards": stats.red_cards,
        "clean_sheet": stats.clean_sheet,
        "saves": stats.saves,
        "goals_conceded": stats.goals_conceded,
        "shots": stats.shots,
        "shots_on_target": stats.shots_on_target,
        "passes": stats.passes,
        "pass_accuracy": stats.pass_accuracy,
        "tackles": stats.tackles,
        "interceptions": stats.interceptions,
        "clearances": stats.clearances,
        "blocks": stats.blocks,
        "fouls": stats.fouls,
        "offsides": stats.offsides
    }


# GET all player match statistics
@player_match_stats_bp.route("", methods=["GET"])
def get_player_match_stats():
    stats = PlayerMatchStat.query.all()

    return jsonify({
        "player_match_stats": [
            stats_to_dict(stat)
            for stat in stats
        ]
    })


# GET one player match statistic
@player_match_stats_bp.route("/<int:stat_id>", methods=["GET"])
def get_player_match_stat(stat_id):
    stat = db.session.get(PlayerMatchStat, stat_id)

    if not stat:
        return jsonify({
            "error": "Player match statistic not found"
        }), 404

    return jsonify(stats_to_dict(stat))


# POST player match statistics
@player_match_stats_bp.route("", methods=["POST"])
def create_player_match_stat():
    data = request.get_json()

    stat = PlayerMatchStat(
        match_id=data["match_id"],
        player_id=data["player_id"],
        minutes_played=data.get("minutes_played", 0),
        started=data.get("started", False),
        goals=data.get("goals", 0),
        assists=data.get("assists", 0),
        yellow_cards=data.get("yellow_cards", 0),
        red_cards=data.get("red_cards", 0),
        clean_sheet=data.get("clean_sheet", False),
        saves=data.get("saves", 0),
        goals_conceded=data.get("goals_conceded", 0),
        shots=data.get("shots", 0),
        shots_on_target=data.get("shots_on_target", 0),
        passes=data.get("passes", 0),
        pass_accuracy=data.get("pass_accuracy"),
        tackles=data.get("tackles", 0),
        interceptions=data.get("interceptions", 0),
        clearances=data.get("clearances", 0),
        blocks=data.get("blocks", 0),
        fouls=data.get("fouls", 0),
        offsides=data.get("offsides", 0)
    )

    db.session.add(stat)
    db.session.commit()

    return jsonify({
        "message": "Player match statistics created successfully",
        "player_match_stats": stats_to_dict(stat)
    }), 201