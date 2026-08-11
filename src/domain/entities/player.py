"""Player domain entities.

Pure business entities representing football players, roles, and playing time.
Clean Architecture Domain layer - Zero external I/O or database dependencies.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class PlayerRole:
    """Represents a player's tactical position/role."""
    id: int
    name: str
    acronym: str
    position_group: str


@dataclass(frozen=True)
class PlayerPlayingTime:
    """Represents playing time statistics for a player in a match."""
    minutes_played: float = 0.0
    minutes_tip: float = 0.0  # Team In Possession
    minutes_otip: float = 0.0  # Opponent Team In Possession
    start_frame: Optional[int] = None
    end_frame: Optional[int] = None


@dataclass
class Player:
    """Represents a football player entity."""
    id: int
    short_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthday: Optional[str] = None
    gender: Optional[str] = "male"
    trackable_object: Optional[int] = None
    number: Optional[int] = None
    role: Optional[PlayerRole] = None
    team_id: Optional[int] = None
    team_player_id: Optional[int] = None
    yellow_card: int = 0
    red_card: int = 0
    injured: bool = False
    goal: int = 0
    own_goal: int = 0
    playing_time: PlayerPlayingTime = field(default_factory=PlayerPlayingTime)

    @property
    def full_name(self) -> str:
        """Get player's full name or short name fallback."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.short_name
