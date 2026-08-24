"""Entidades de domínio para eventos espaciais.

Entidades de negócio puras representando eventos táticos dinâmicos (PassEvent, OffBallRunEvent).
Camada de Domínio da Clean Architecture - Zero dependências de I/O externo ou bibliotecas de terceiros.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PassEvent:
    """Representa um evento de passe com contexto espacial e tático completo."""
    event_id: str
    match_id: int
    frame_start: int
    frame_end: int
    period: int
    player_id: int
    team_id: int
    x_start: float
    y_start: float
    x_end: float
    y_end: float
    pass_distance: float
    pass_angle: float
    pass_outcome: str  # ex: 'successful', 'unsuccessful', 'completed'
    
    # Metadados opcionais e informações do atleta
    time_start: Optional[str] = None
    time_end: Optional[str] = None
    minute_start: Optional[int] = None
    second_start: Optional[int] = None
    player_name: Optional[str] = None
    player_position: Optional[str] = None
    player_targeted_id: Optional[int] = None
    player_targeted_name: Optional[str] = None
    
    # Pressão defensiva e contexto espacial
    separation_start: Optional[float] = None
    separation_end: Optional[float] = None
    separation_gain: Optional[float] = None
    last_defensive_line_x_start: Optional[float] = None
    last_defensive_line_x_end: Optional[float] = None
    delta_to_last_defensive_line_start: Optional[float] = None
    interplayer_distance_start: Optional[float] = None
    angle_of_engagement: Optional[float] = None
    inside_defensive_shape_start: Optional[bool] = None
    
    # Ruptura de linhas e desfecho da jogada
    first_line_break: Optional[bool] = None
    last_line_break: Optional[bool] = None
    lead_to_shot: bool = False
    lead_to_goal: bool = False
    
    # Métricas avançadas de perigo e expectativa
    xthreat: Optional[float] = None
    xpass_completion: Optional[float] = None
    passing_option_score: Optional[float] = None

    @property
    def is_completed(self) -> bool:
        """Verifica se o passe foi concluído com sucesso."""
        return self.pass_outcome.lower() in ("completed", "successful", "complete", "true", "1")


@dataclass(frozen=True)
class OffBallRunEvent:
    """Representa um evento de corrida sem a posse da bola (desmarque/criação de espaço)."""
    event_id: str
    match_id: int
    frame_start: int
    frame_end: int
    period: int
    player_id: int
    team_id: int
    x_start: float
    y_start: float
    x_end: float
    y_end: float
    
    # Contexto temporal e físico
    time_start: Optional[str] = None
    time_end: Optional[str] = None
    minute_start: Optional[int] = None
    second_start: Optional[int] = None
    player_name: Optional[str] = None
    player_position: Optional[str] = None
    distance_covered: Optional[float] = None
    speed_avg: Optional[float] = None
    
    # Separação espacial e contexto da linha defensiva
    separation_start: Optional[float] = None
    separation_end: Optional[float] = None
    separation_gain: Optional[float] = None
    last_defensive_line_x_start: Optional[float] = None
    last_defensive_line_x_end: Optional[float] = None
    delta_to_last_defensive_line_start: Optional[float] = None
    delta_to_last_defensive_line_gain: Optional[float] = None
    inside_defensive_shape_start: Optional[bool] = None
    inside_defensive_shape_end: Optional[bool] = None
    
    # Recepção e contexto de perigo
    targeted: Optional[bool] = None
    received: Optional[bool] = None
    received_in_space: Optional[bool] = None
    dangerous: Optional[bool] = None
    lead_to_shot: bool = False
    lead_to_goal: bool = False
    
    # Métricas de ameaça gerada
    xthreat: Optional[float] = None

    @property
    def net_separation_gain(self) -> float:
        """Calcula ou retorna o ganho líquido de separação gerado pelo desmarque."""
        if self.separation_gain is not None:
            return self.separation_gain
        if self.separation_start is not None and self.separation_end is not None:
            return self.separation_end - self.separation_start
        return 0.0
