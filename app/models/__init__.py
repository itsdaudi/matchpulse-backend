# Import all database models here so SQLAlchemy and Flask-Migrate
# can discover them when creating and updating database tables.

from app.models.league import League
from app.models.team import Team
from app.models.player import Player
from app.models.match import Match
from app.models.player_match_stat import PlayerMatchStat  
from app.models.lineup import Lineup
from app.models.lineup_player import LineupPlayer
from app.models.match_team_stats import MatchTeamStats