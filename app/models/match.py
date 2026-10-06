from app.extensions import db


class Match(db.Model):
    """
    Represents a football match between two teams.

    A match belongs to a league and has one home team
    and one away team.
    """

    __tablename__ = "matches"

    # Unique identifier for the match.
    id = db.Column(db.Integer, primary_key=True)

    # League in which the match is played.
    league_id = db.Column(
        db.Integer,
        db.ForeignKey("leagues.id"),
        nullable=False
    )

    # Team playing at home.
    home_team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )

    # Team playing away.
    away_team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )

    # Date and time when the match starts.
    match_date = db.Column(
        db.DateTime,
        nullable=False
    )

    # Stadium where the match is played.
    venue = db.Column(
        db.String(150),
        nullable=True
    )

    # Current status of the match.
    # Examples: scheduled, live, finished, postponed.
    status = db.Column(
        db.String(20),
        nullable=False,
        default="scheduled"
    )

    # Goals scored by the home team.
    home_score = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    # Goals scored by the away team.
    away_score = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    # Relationship to the league.
    league = db.relationship(
        "League",
        back_populates="matches"
    )

    # Relationship to the home team.
    home_team = db.relationship(
        "Team",
        foreign_keys=[home_team_id],
        back_populates="home_matches"
    )

    # Relationship to the away team.
    away_team = db.relationship(
        "Team",
        foreign_keys=[away_team_id],
        back_populates="away_matches"
    )

    # All player performance stats for this match.
    player_stats = db.relationship(
        "PlayerMatchStat",
        back_populates="match",
        cascade="all, delete-orphan"
    )

    # Team-level statistics for this match.
    team_stats = db.relationship(
        "MatchTeamStats",
        back_populates="match",
        cascade="all, delete-orphan"
    )

    # Two lineups for this match, one for each team.
    lineups = db.relationship(
        "Lineup",
        back_populates="match",
        cascade="all, delete-orphan"
    )

    # All events that occurred during this match.
    events = db.relationship(
        "MatchEvent",
        back_populates="match",
        cascade="all, delete-orphan"
    )

    def update_score_from_events(self):
        """
        Recalculate the match score from its goal events.

        Only goal events affect the score.
        """

        home_score = 0
        away_score = 0

        for event in self.events:

            # Ignore cards, substitutions, etc.
            if event.event_type != "goal":
                continue

            # Goal scored by the home team.
            if event.team_id == self.home_team_id:
                home_score += 1

            # Goal scored by the away team.
            elif event.team_id == self.away_team_id:
                away_score += 1

        self.home_score = home_score
        self.away_score = away_score

    def __repr__(self):
        return f"<Match {self.home_team_id} vs {self.away_team_id}>"
