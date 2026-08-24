"""Entidades de domínio para jogadores de futebol.

Entidades de negócio puras representando atletas, posições táticas e minutagem.
Camada de Domínio da Clean Architecture - Zero dependências de I/O externo ou bibliotecas de terceiros.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class PlayerRole:
    """Representa a posição e o papel tático do atleta."""
    id: int
    name: str
    acronym: str
    position_group: str


@dataclass(frozen=True)
class PlayerPlayingTime:
    """Estatísticas de tempo de jogo de um atleta em uma partida."""
    minutes_played: float = 0.0
    minutes_tip: float = 0.0  # Tempo em posse da equipe (Team In Possession)
    minutes_otip: float = 0.0  # Tempo sem a posse da equipe (Opponent Team In Possession)
    start_frame: Optional[int] = None
    end_frame: Optional[int] = None


@dataclass
class Player:
    """Representa a entidade de um jogador de futebol."""
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
        """Retorna o nome completo do atleta ou o nome abreviado como fallback."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.short_name
