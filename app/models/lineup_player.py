from app.extensions import db


class LineupPlayer(db.Model):
    """
    Represents a player's position within a specific match lineup.

    This allows MatchPulse to know not only which players started,
    but also where each player was positioned on the pitch.
    """

    __tablename__ = "lineup_players"

    # Unique identifier for this lineup entry.
    id = db.Column(db.Integer, primary_key=True)

    # The lineup this player belongs to.
    lineup_id = db.Column(
        db.Integer,
        db.ForeignKey("lineups.id"),
        nullable=False
    )

    # The player included in the lineup.
    player_id = db.Column(
        db.Integer,
        db.ForeignKey("players.id"),
        nullable=False
    )

    # Position displayed on the pitch.
    # Examples: GK, LB, CB, RB, CM, LW, ST.
    position = db.Column(
        db.String(20),
        nullable=False
    )

    # Horizontal position on the pitch.
    # Used later by React to visually position the player.
    position_x = db.Column(
        db.Float,
        nullable=True
    )

    # Vertical position on the pitch.
    # Used later by React to visually position the player.
    position_y = db.Column(
        db.Float,
        nullable=True
    )

    # Whether the player was part of the starting XI.
    starter = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    # Shirt number used in this match.
    shirt_number = db.Column(
        db.Integer,
        nullable=True
    )

    # Relationship back to the lineup.
    lineup = db.relationship(
        "Lineup",
        back_populates="lineup_players"
    )

    # Relationship back to the player.
    player = db.relationship(
        "Player",
        back_populates="lineup_entries"
    )

    def __repr__(self):
        return f"<LineupPlayer player={self.player_id} position={self.position}>"