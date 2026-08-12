from app.extensions import db


class PlayerMatchStat(db.Model):
    """
    Stores a player's performance in one particular match.

    A player can have many PlayerMatchStat records because
    they can participate in many different matches.
    """

    __tablename__ = "player_match_stats"

    # Unique identifier for this performance record.
    id = db.Column(db.Integer, primary_key=True)

    # The match in which the player participated.
    match_id = db.Column(
        db.Integer,
        db.ForeignKey("matches.id"),
        nullable=False
    )

    # The player whose performance is being recorded.
    player_id = db.Column(
        db.Integer,
        db.ForeignKey("players.id"),
        nullable=False
    )

    # Number of minutes the player was on the pitch.
    minutes_played = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    # Whether the player started the match.
    started = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    # Number of goals scored.
    goals = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    # Number of assists provided.
    assists = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    # Yellow cards received.
    yellow_cards = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    # Red cards received.
    red_cards = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    # Whether the player kept a clean sheet.
    #
    # This will normally be relevant to defenders and goalkeepers.
    clean_sheet = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    # Number of saves made.
    #
    # Primarily useful for goalkeepers.
    saves = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    #Goals conceded by the player.
    #for goalkeepers
    goals_conceded = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    #number of passes made by the player.
    passes = db.Column(
        db.Integer,
        nullable= False,
        default = 0
    )

    #percentage of passes completed by the player.
    pass_accuracy = db.Column(
        db.Float,
        nullable=True
    )

    #number of tackles made by the player.
    tackles = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    #number of interceptions made by the player.
    interceptions = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    #number of clearances made by the player.
    clearances = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    #number of blocked attempts
    blocks = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    #number of fouls commited
    fouls = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    #number of times player was offside
    offsides = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    


    # Total shots attempted.
    shots = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    # Shots that were on target.
    shots_on_target = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    # Relationship to the match.
    match = db.relationship(
        "Match",
        back_populates="player_stats"
    )

    # Relationship to the player.
    player = db.relationship(
        "Player",
        back_populates="match_stats"
    )

    def __repr__(self):
        return f"<PlayerMatchStat player={self.player_id} match={self.match_id}>"