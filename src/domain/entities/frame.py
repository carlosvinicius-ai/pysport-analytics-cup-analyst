"""Entidades de domínio para frames de tracking espacial.

Entidades de negócio puras representando snapshots de tracking e coordenadas de atletas.
Camada de Domínio da Clean Architecture - Zero dependências de I/O externo ou bibliotecas de terceiros.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass(frozen=True)
class PlayerPosition:
    """Representa as coordenadas instantâneas e a cinemática de um atleta."""
    player_id: int
    team_id: int
    x: float
    y: float
    trackable_object: Optional[int] = None
    speed: Optional[float] = None
    acceleration: Optional[float] = None
    distance_to_ball: Optional[float] = None
    distance_to_nearest_opponent: Optional[float] = None
    nearest_opponent_id: Optional[int] = None


@dataclass(frozen=True)
class BallPosition:
    """Representa as coordenadas 3D instantâneas da bola."""
    x: float
    y: float
    z: float = 0.0
    trackable_object: Optional[int] = None
    is_detected: bool = True
    speed: Optional[float] = None


@dataclass(frozen=True)
class TrackingFrame:
    """Representa um snapshot temporal discreto do campo de jogo."""
    frame_idx: int
    period: int
    time_seconds: float
    player_positions: Tuple[PlayerPosition, ...] = field(default_factory=tuple)
    ball: Optional[BallPosition] = None

    def get_player_position(self, player_id: int) -> Optional[PlayerPosition]:
        """Busca a posição instantânea de um jogador por ID neste frame."""
        for p in self.player_positions:
            if p.player_id == player_id:
                return p
        return None

    def get_team_positions(self, team_id: int) -> List[PlayerPosition]:
        """Retorna todas as posições dos jogadores pertencentes a uma equipe."""
        return [p for p in self.player_positions if p.team_id == team_id]

    @property
    def total_players_detected(self) -> int:
        """Contagem total de jogadores detectados neste frame."""
        return len(self.player_positions)
