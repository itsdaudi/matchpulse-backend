from app.extensions import db


class MatchEvent(db.Model):
    """
    Represents an important event that happens during a football match.

    Examples include goals, yellow cards, red cards, and substitutions.
    """

    __tablename__ = "match_events"

    # Unique identifier for the event.
    id = db.Column(db.Integer, primary_key=True)

    # The match in which the event occurred.
    match_id = db.Column(
        db.Integer,
        db.ForeignKey("matches.id"),
        nullable=False
    )

    # The team involved in the event.
    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )

    # The player directly involved in the event.
    player_id = db.Column(
        db.Integer,
        db.ForeignKey("players.id"),
        nullable=True
    )

    # Player who provided the assist.
    # Only relevant for goals.
    assist_player_id = db.Column(
        db.Integer,
        db.ForeignKey("players.id"),
        nullable=True
    )

    # Type of event.
    # Examples: goal, yellow_card, red_card, substitution.
    event_type = db.Column(
        db.String(30),
        nullable=False
    )

    # Match minute when the event happened.
    minute = db.Column(
        db.Integer,
        nullable=False
    )

    # Additional stoppage-time minute.
    # Example: 90+3 -> minute = 90, added_time = 3.
    added_time = db.Column(
        db.Integer,
        nullable=True
    )

    # Player coming onto the pitch during a substitution.
    substitution_in_player_id = db.Column(
        db.Integer,
        db.ForeignKey("players.id"),
        nullable=True
    )

    # Player leaving the pitch during a substitution.
    substitution_out_player_id = db.Column(
        db.Integer,
        db.ForeignKey("players.id"),
        nullable=True
    )

    # Optional description of the event.
    description = db.Column(
        db.String(255),
        nullable=True
    )

    # Relationships.
    match = db.relationship(
        "Match",
        back_populates="events"
    )

    team = db.relationship(
        "Team",
        back_populates="events"
    )

    player = db.relationship(
        "Player",
        foreign_keys=[player_id],
        back_populates="events"
    )

    assist_player = db.relationship(
        "Player",
        foreign_keys=[assist_player_id]
    )

    substitution_in_player = db.relationship(
        "Player",
        foreign_keys=[substitution_in_player_id]
    )

    substitution_out_player = db.relationship(
        "Player",
        foreign_keys=[substitution_out_player_id]
    )

    def __repr__(self):
        return (
            f"<MatchEvent match={self.match_id} "
            f"type={self.event_type} minute={self.minute}>"
        )