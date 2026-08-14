from flask import Blueprint, request, jsonify

from app.extensions import db
from app.models import MatchEvent


match_events_bp = Blueprint(
    "match_events",
    __name__,
    url_prefix="/api/match-events"
)


def event_to_dict(event):
    """Convert a MatchEvent into a JSON-friendly dictionary."""

    return {
        "id": event.id,
        "match_id": event.match_id,
        "team_id": event.team_id,
        "player_id": event.player_id,
        "assist_player_id": event.assist_player_id,
        "event_type": event.event_type,
        "minute": event.minute,
        "added_time": event.added_time,
        "substitution_in_player_id": event.substitution_in_player_id,
        "substitution_out_player_id": event.substitution_out_player_id,
        "description": event.description
    }


# GET all match events.
@match_events_bp.route("", methods=["GET"])
def get_match_events():
    events = MatchEvent.query.all()

    return jsonify({
        "match_events": [
            event_to_dict(event)
            for event in events
        ]
    })


# GET one match event.
@match_events_bp.route("/<int:event_id>", methods=["GET"])
def get_match_event(event_id):
    event = db.session.get(MatchEvent, event_id)

    if not event:
        return jsonify({
            "error": "Match event not found"
        }), 404

    return jsonify(event_to_dict(event))


# POST a new match event.
@match_events_bp.route("", methods=["POST"])
def create_match_event():
    data = request.get_json()

    event = MatchEvent(
        match_id=data["match_id"],
        team_id=data["team_id"],
        player_id=data.get("player_id"),
        assist_player_id=data.get("assist_player_id"),
        event_type=data["event_type"],
        minute=data["minute"],
        added_time=data.get("added_time"),
        substitution_in_player_id=data.get("substitution_in_player_id"),
        substitution_out_player_id=data.get("substitution_out_player_id"),
        description=data.get("description")
    )

    db.session.add(event)
    db.session.commit()

    return jsonify({
        "message": "Match event created successfully",
        "match_event": event_to_dict(event)
    }), 201


# PATCH an existing match event.
@match_events_bp.route("/<int:event_id>", methods=["PATCH"])
def update_match_event(event_id):
    event = db.session.get(MatchEvent, event_id)

    if not event:
        return jsonify({
            "error": "Match event not found"
        }), 404

    data = request.get_json()

    if "team_id" in data:
        event.team_id = data["team_id"]

    if "player_id" in data:
        event.player_id = data["player_id"]

    if "assist_player_id" in data:
        event.assist_player_id = data["assist_player_id"]

    if "event_type" in data:
        event.event_type = data["event_type"]

    if "minute" in data:
        event.minute = data["minute"]

    if "added_time" in data:
        event.added_time = data["added_time"]

    if "substitution_in_player_id" in data:
        event.substitution_in_player_id = data["substitution_in_player_id"]

    if "substitution_out_player_id" in data:
        event.substitution_out_player_id = data["substitution_out_player_id"]

    if "description" in data:
        event.description = data["description"]

    db.session.commit()

    return jsonify({
        "message": "Match event updated successfully",
        "match_event": event_to_dict(event)
    })


# DELETE a match event.
@match_events_bp.route("/<int:event_id>", methods=["DELETE"])
def delete_match_event(event_id):
    event = db.session.get(MatchEvent, event_id)

    if not event:
        return jsonify({
            "error": "Match event not found"
        }), 404

    db.session.delete(event)
    db.session.commit()

    return jsonify({
        "message": "Match event deleted successfully"
    })