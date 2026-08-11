from app.extensions import db


class Player(db.Model):
    """
    Represents a football player belonging to a team.

    Player information is kept separate from match statistics.
    This allows the same player to have many performances across
    different matches and seasons.
    """

    __tablename__ = "players"

    # Unique identifier for the player.
    id = db.Column(db.Integer, primary_key=True)

    # The team the player currently belongs to.
    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )

    # Player's full name.
    name = db.Column(db.String(100), nullable=False)

    # Player's shirt number.
    shirt_number = db.Column(db.Integer, nullable=True)

    # Player's main position.
    # Examples: Goalkeeper, Defender, Midfielder, Forward.
    position = db.Column(db.String(30), nullable=False)

    # URL/path to the player's profile image.
    photo = db.Column(db.String(255), nullable=True)

    # Relationship allowing us to access the player's team.
    team = db.relationship(
        "Team",
        back_populates="players"
    )

    def __repr__(self):
        return f"<Player {self.name}>"