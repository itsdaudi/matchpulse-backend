from app.extensions import db


class MatchTeamStats(db.Model):
    """
    Stores the performance statistics of one team
    during one specific football match.
    """

    __tablename__ = "match_team_stats"

    # Unique identifier for the statistics record.
    id = db.Column(db.Integer, primary_key=True)

    # The match these statistics belong to.
    match_id = db.Column(
        db.Integer,
        db.ForeignKey("matches.id"),
        nullable=False
    )

    # The team whose performance is being recorded.
    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )

    # Percentage of possession held by the team.
    possession = db.Column(
        db.Float,
        nullable=True
    )

    # Total number of shots.
    shots = db.Column(
        db.Integer,
        nullable=True
    )

    # Shots that were on target.
    shots_on_target = db.Column(
        db.Integer,
        nullable=True
    )

    # Shots that were off target.
    shots_off_target = db.Column(
        db.Integer,
        nullable=True
    )

    # Number of corners won.
    corners = db.Column(
        db.Integer,
        nullable=True
    )

    # Number of fouls committed.
    fouls = db.Column(
        db.Integer,
        nullable=True
    )

    # Number of times the team was caught offside.
    offsides = db.Column(
        db.Integer,
        nullable=True
    )

    # Number of yellow cards received.
    yellow_cards = db.Column(
        db.Integer,
        nullable=True
    )

    # Number of red cards received.
    red_cards = db.Column(
        db.Integer,
        nullable=True
    )

    # Total completed and attempted passes recorded for the team.
    passes = db.Column(
        db.Integer,
        nullable=True
    )

    # Percentage of passes completed successfully.
    pass_accuracy = db.Column(
        db.Float,
        nullable=True
    )

    # Relationship back to the match.
    match = db.relationship(
        "Match",
        back_populates="team_stats"
    )

    # Relationship back to the team.
    team = db.relationship(
        "Team",
        back_populates="match_stats"
    )

    def __repr__(self):
        return f"<MatchTeamStats match={self.match_id} team={self.team_id}>"