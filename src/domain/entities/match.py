"""Match domain entities.

Pure business entities representing matches, teams, stadiums, pitch dimensions, and periods.
Clean Architecture Domain layer - Zero external I/O or database dependencies.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Union
from src.domain.entities.player import Player


@dataclass(frozen=True)
class PitchDimensions:
    """Represents the pitch length and width in meters."""
    length: float
    width: float

    @property
    def area(self) -> float:
        """Calculate total pitch area in square meters."""
        return self.length * self.width


@dataclass(frozen=True)
class Team:
    """Represents a football club/team entity."""
    id: int
    name: str
    short_name: str
    acronym: Optional[str] = None
    jersey_color: Optional[str] = None


@dataclass(frozen=True)
class Stadium:
    """Represents a stadium entity."""
    id: int
    name: str
    city: Optional[str] = None
    capacity: Optional[int] = None


@dataclass(frozen=True)
class MatchPeriod:
    """Represents a period of play (1st half, 2nd half, overtime)."""
    period: int
    name: str
    start_frame: int
    end_frame: int
    duration_frames: int
    duration_minutes: float


@dataclass
class Match:
    """Represents a football match entity."""
    id: int
    date_time: Union[str, datetime]
    home_team: Team
    away_team: Team
    status: str = "closed"
    competition_id: Optional[int] = None
    season_id: Optional[int] = None
    competition_edition_id: Optional[int] = None
    home_team_score: Optional[int] = None
    away_team_score: Optional[int] = None
    pitch_dimensions: Optional[PitchDimensions] = None
    stadium: Optional[Stadium] = None
    periods: List[MatchPeriod] = field(default_factory=list)
    players: List[Player] = field(default_factory=list)

    def get_player(self, player_id: int) -> Optional[Player]:
        """Find a player by ID in the match roster."""
        for p in self.players:
            if p.id == player_id:
                return p
        return None

    def get_team_players(self, team_id: int) -> List[Player]:
        """Get list of players belonging to a specific team ID."""
        return [p for p in self.players if p.team_id == team_id]
