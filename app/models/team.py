from app.extensions import db


class Team(db.Model):
    """
    Represents a football team participating in a league.

    Each team belongs to one league, while a league can contain
    many teams.
    """

    __tablename__ = "teams"

    # Unique identifier for the team.
    id = db.Column(db.Integer, primary_key=True)

    # Connects this team to its league.
    # The foreign key references the primary key of the leagues table.
    league_id = db.Column(
        db.Integer,
        db.ForeignKey("leagues.id"),
        nullable=False
    )

    # Official team name.
    name = db.Column(db.String(100), nullable=False)

    # Short name or abbreviation used in compact displays.
    short_name = db.Column(db.String(20), nullable=True)

    # URL/path to the team's logo.
    logo = db.Column(db.String(255), nullable=True)

    # Name of the team's home stadium.
    stadium = db.Column(db.String(150), nullable=True)

    # Relationship allowing us to access the league from a team.
    league = db.relationship("League", back_populates="teams")

    # Relationship allowing us to access the players belonging to this team.
    players = db.relationship("Player", back_populates="team", cascade="all, delete-orphan")

    home_matches = db.relationship(
        "Match",
        foreign_keys="Match.home_team_id",
        back_populates="home_team",
    )

    away_matches = db.relationship(
        "Match",
        foreign_keys="Match.away_team_id",
        back_populates="away_team",
    )

    #all lineups for this team.
    lineups = db.relationship(
        "Lineup",
        back_populates="team",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Team {self.name}>"