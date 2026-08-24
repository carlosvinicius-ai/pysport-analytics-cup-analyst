"""Entidades de domínio para partidas de futebol.

Entidades de negócio puras representando partidas, equipes, estádios, dimensões do gramado e períodos.
Camada de Domínio da Clean Architecture - Zero dependências de I/O externo ou bibliotecas de terceiros.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Union
from src.domain.entities.player import Player


@dataclass(frozen=True)
class PitchDimensions:
    """Representa o comprimento e a largura do gramado em metros."""
    length: float
    width: float

    @property
    def area(self) -> float:
        """Calcula a área total do campo em metros quadrados."""
        return self.length * self.width


@dataclass(frozen=True)
class Team:
    """Representa uma equipe/clube de futebol."""
    id: int
    name: str
    short_name: str
    acronym: Optional[str] = None
    jersey_color: Optional[str] = None


@dataclass(frozen=True)
class Stadium:
    """Representa um estádio de futebol."""
    id: int
    name: str
    city: Optional[str] = None
    capacity: Optional[int] = None


@dataclass(frozen=True)
class MatchPeriod:
    """Representa um período de jogo (1º tempo, 2º tempo, prorrogação)."""
    period: int
    name: str
    start_frame: int
    end_frame: int
    duration_frames: int
    duration_minutes: float


@dataclass
class Match:
    """Representa a entidade de uma partida de futebol."""
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
        """Busca um jogador pelo ID no elenco escalado na partida."""
        for p in self.players:
            if p.id == player_id:
                return p
        return None

    def get_team_players(self, team_id: int) -> List[Player]:
        """Retorna a lista de jogadores de uma determinada equipe na partida."""
        return [p for p in self.players if p.team_id == team_id]
