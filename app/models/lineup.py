from app.extensions import db


class Lineup(db.Model):
    """
    Represents a team's lineup for a particular match.

    Each match has one lineup for the home team and one
    lineup for the away team.
    """

    __tablename__ = "lineups"

    # Unique identifier for the lineup.
    id = db.Column(db.Integer, primary_key=True)

    # The match this lineup belongs to.
    match_id = db.Column(
        db.Integer,
        db.ForeignKey("matches.id"),
        nullable=False
    )

    # The team using this lineup.
    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )

    # Formation used by the team.
    # Examples: "4-3-3", "4-2-3-1", "3-5-2".
    formation = db.Column(
        db.String(20),
        nullable=False
    )

    # Relationship to the match.
    match = db.relationship(
        "Match",
        back_populates="lineups"
    )

    # Relationship to the team.
    team = db.relationship(
        "Team",
        back_populates="lineups"
    )

    # Players included in this lineup.
    lineup_players = db.relationship(
        "LineupPlayer",
        back_populates="lineup",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Lineup team={self.team_id} formation={self.formation}>"