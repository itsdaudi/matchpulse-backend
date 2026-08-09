from app.extensions import db


class League(db.Model):
    """
    Represents a football league or competition.

    Examples:
    - Premier League
    - La Liga
    - Bundesliga
    - Serie A
    """

    __tablename__ = "leagues"

    # Unique identifier for each league.
    id = db.Column(db.Integer, primary_key=True)

    # Official name of the league.
    name = db.Column(db.String(100), nullable=False)

    # Country or region associated with the league.
    country = db.Column(db.String(100), nullable=True)

    # URL/path for the league's logo.
    logo = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<League {self.name}>"