"""Caso de uso para cálculo e extração de atributos espaciais de passes.

Orquestra a transformação de entidades PassEvent em vetores de features e tabelas Polars
contendo métricas geométricas, pressão defensiva, contexto de linhas e progressão territorial.
"""

from dataclasses import asdict, dataclass
import math
from typing import Any, Dict, List, Optional
import polars as pl
from src.domain.entities.event import PassEvent
from src.domain.protocols.repository import IEventRepository


@dataclass(frozen=True)
class SpatialPassFeatures:
    """Dataclass estruturada contendo o conjunto de features espaciais de um passe."""
    # Identificadores e contexto da partida
    event_id: str
    match_id: int
    player_id: int
    team_id: int
    period: int
    minute_start: Optional[int]
    second_start: Optional[int]
    
    # Coordenadas do passe
    x_start: float
    y_start: float
    x_end: float
    y_end: float
    
    # Geometria do passe
    pass_distance: float
    pass_angle: float
    progression_x: float
    lateral_displacement: float
    
    # Relação espacial com o gol adversário (alvo em x = pitch_length / 2, y = 0)
    distance_to_goal_start: float
    distance_to_goal_end: float
    angle_to_goal_start: float
    angle_to_goal_end: float
    
    # Pressão defensiva e separação espacial
    separation_start: float
    separation_end: float
    separation_gain: float
    interplayer_distance_start: float
    has_defensive_pressure: bool
    last_defensive_line_x_start: Optional[float]
    delta_to_last_defensive_line_start: Optional[float]
    inside_defensive_shape_start: bool
    
    # Ruptura de linhas e desfecho
    first_line_break: bool
    last_line_break: bool
    lead_to_shot: bool
    lead_to_goal: bool
    
    # Target / Rótulo supervisionado
    pass_outcome: str
    is_completed: int  # 1 para completado, 0 para incompleto
    
    # Métricas de benchmark da SkillCorner
    xthreat: Optional[float] = None
    xpass_completion: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância para um dicionário serializável."""
        return asdict(self)


class ComputeSpatialFeaturesUseCase:
    """Caso de uso para extração de atributos espaciais e geométricos de eventos de futebol."""

    def __init__(
        self,
        event_repository: Optional[IEventRepository] = None,
        pitch_length: float = 105.0,
        pitch_width: float = 68.0
    ):
        """Inicializa o use case com repositório opcional e dimensões do campo.

        Args:
            event_repository: Instância opcional de IEventRepository para carregamento por partida.
            pitch_length: Comprimento total do gramado em metros (padrão 105.0m).
            pitch_width: Largura total do gramado em metros (padrão 68.0m).
        """
        self.event_repository = event_repository
        self.pitch_length = pitch_length
        self.pitch_width = pitch_width
        self.goal_x = pitch_length / 2.0  # Coordenada x do gol adversário (+52.5m)

    def compute_for_pass(self, pass_event: PassEvent) -> SpatialPassFeatures:
        """Calcula o vetor completo de atributos espaciais para um único evento de passe.

        Args:
            pass_event: Instância de PassEvent da camada de domínio.

        Returns:
            Instância de SpatialPassFeatures calculada.
        """
        # 1. Geometria territorial do passe
        progression_x = pass_event.x_end - pass_event.x_start
        lateral_displacement = abs(pass_event.y_end - pass_event.y_start)
        pass_distance = pass_event.pass_distance if pass_event.pass_distance > 0.0 else math.hypot(progression_x, lateral_displacement)
        pass_angle = pass_event.pass_angle if pass_event.pass_angle != 0.0 else math.atan2(pass_event.y_end - pass_event.y_start, progression_x)

        # 2. Distâncias e ângulos em relação ao gol adversário
        dx_start = self.goal_x - pass_event.x_start
        dy_start = -pass_event.y_start
        distance_to_goal_start = math.hypot(dx_start, dy_start)
        angle_to_goal_start = math.atan2(abs(dy_start), max(0.1, dx_start))

        dx_end = self.goal_x - pass_event.x_end
        dy_end = -pass_event.y_end
        distance_to_goal_end = math.hypot(dx_end, dy_end)
        angle_to_goal_end = math.atan2(abs(dy_end), max(0.1, dx_end))

        # 3. Pressão defensiva e separação espacial
        if pass_event.interplayer_distance_start is not None:
            interplayer_dist = pass_event.interplayer_distance_start
            has_pressure = interplayer_dist <= 3.0  # Pressão alta a menos de 3 metros
        else:
            interplayer_dist = 15.0  # Imputação neutra (espaço livre)
            has_pressure = False

        sep_start = pass_event.separation_start if pass_event.separation_start is not None else 5.0
        sep_end = pass_event.separation_end if pass_event.separation_end is not None else sep_start
        sep_gain = pass_event.separation_gain if pass_event.separation_gain is not None else (sep_end - sep_start)

        # 4. Construção da feature set
        return SpatialPassFeatures(
            event_id=pass_event.event_id,
            match_id=pass_event.match_id,
            player_id=pass_event.player_id,
            team_id=pass_event.team_id,
            period=pass_event.period,
            minute_start=pass_event.minute_start,
            second_start=pass_event.second_start,
            x_start=pass_event.x_start,
            y_start=pass_event.y_start,
            x_end=pass_event.x_end,
            y_end=pass_event.y_end,
            pass_distance=pass_distance,
            pass_angle=pass_angle,
            progression_x=progression_x,
            lateral_displacement=lateral_displacement,
            distance_to_goal_start=distance_to_goal_start,
            distance_to_goal_end=distance_to_goal_end,
            angle_to_goal_start=angle_to_goal_start,
            angle_to_goal_end=angle_to_goal_end,
            separation_start=sep_start,
            separation_end=sep_end,
            separation_gain=sep_gain,
            interplayer_distance_start=interplayer_dist,
            has_defensive_pressure=has_pressure,
            last_defensive_line_x_start=pass_event.last_defensive_line_x_start,
            delta_to_last_defensive_line_start=pass_event.delta_to_last_defensive_line_start,
            inside_defensive_shape_start=bool(pass_event.inside_defensive_shape_start),
            first_line_break=bool(pass_event.first_line_break),
            last_line_break=bool(pass_event.last_line_break),
            lead_to_shot=pass_event.lead_to_shot,
            lead_to_goal=pass_event.lead_to_goal,
            pass_outcome=pass_event.pass_outcome,
            is_completed=1 if pass_event.is_completed else 0,
            xthreat=pass_event.xthreat,
            xpass_completion=pass_event.xpass_completion
        )

    def compute_for_match(self, match_id: int) -> List[SpatialPassFeatures]:
        """Carrega os passes de uma partida via repositório e calcula suas features espaciais.

        Args:
            match_id: Identificador numérico da partida.

        Returns:
            Lista de instâncias de SpatialPassFeatures.
        """
        if not self.event_repository:
            raise ValueError("IEventRepository não foi fornecido no construtor do use case.")

        passes = self.event_repository.get_pass_events(match_id)
        return [self.compute_for_pass(p) for p in passes]

    def to_dataframe(self, features: List[SpatialPassFeatures]) -> pl.DataFrame:
        """Converte uma lista de features espaciais em um DataFrame Polars otimizado.

        Args:
            features: Lista de instâncias de SpatialPassFeatures.

        Returns:
            DataFrame Polars com esquema tipado pronto para modelagem.
        """
        if not features:
            return pl.DataFrame()
        
        data_dicts = [f.to_dict() for f in features]
        return pl.DataFrame(data_dicts)
