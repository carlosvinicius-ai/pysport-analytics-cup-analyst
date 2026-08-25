"""Parser concreto para eventos dinâmicos e espaciais da SkillCorner utilizando Polars.

Implementa o protocolo IEventRepository da camada de domínio.
Lê arquivos <match_id>_dynamic_events.csv e constrói instâncias de PassEvent e OffBallRunEvent.
"""

import math
from pathlib import Path
from typing import Any, List, Optional, Union
import polars as pl
from src.domain.entities.event import OffBallRunEvent, PassEvent
from src.domain.protocols.repository import IEventRepository


def _safe_float(val: Any) -> Optional[float]:
    """Converte valor para float seguro, retornando None para nulos ou NaNs."""
    if val is None:
        return None
    try:
        f_val = float(val)
        return None if math.isnan(f_val) else f_val
    except (ValueError, TypeError):
        return None


def _safe_int(val: Any) -> Optional[int]:
    """Converte valor para int seguro, retornando None para nulos ou NaNs."""
    if val is None:
        return None
    try:
        if isinstance(val, float) and math.isnan(val):
            return None
        return int(val)
    except (ValueError, TypeError):
        return None


def _safe_str(val: Any) -> Optional[str]:
    """Converte valor para string segura, retornando None para nulos."""
    if val is None:
        return None
    s = str(val).strip()
    return None if s.lower() in ("", "none", "nan", "null") else s


def _safe_bool(val: Any) -> bool:
    """Converte valor para booleano seguro."""
    if val is None:
        return False
    if isinstance(val, bool):
        return val
    s = str(val).strip().lower()
    return s in ("true", "1", "yes", "t")


class SkillCornerTrackingParser:
    """Implementação de IEventRepository para extração vetorizada de eventos via Polars."""

    def __init__(self, data_dir: Union[str, Path]):
        """Inicializa o parser com o diretório raiz de dados.

        Args:
            data_dir: Caminho base para a pasta de dados (ex: 'data/opendata').
        """
        self.data_dir = Path(data_dir)

    def _find_dynamic_events_file(self, match_id: int) -> Optional[Path]:
        """Localiza o arquivo CSV de eventos dinâmicos para a partida informada.

        Args:
            match_id: Identificador numérico da partida.

        Returns:
            Caminho do arquivo CSV se encontrado, caso contrário None.
        """
        filename = f"{match_id}_dynamic_events.csv"
        # Tenta estrutura data/matches/<id>/<id>_dynamic_events.csv
        direct = self.data_dir / "data" / "matches" / str(match_id) / filename
        if direct.exists():
            return direct
        direct_alt = self.data_dir / "matches" / str(match_id) / filename
        if direct_alt.exists():
            return direct_alt
        # Busca recursiva como fallback
        found = list(self.data_dir.glob(f"**/{filename}"))
        return found[0] if found else None

    def get_pass_events(self, match_id: int) -> List[PassEvent]:
        """Recupera e instancia todos os eventos de passe de uma partida.

        Args:
            match_id: Identificador numérico da partida.

        Returns:
            Lista de entidades PassEvent ordenadas por frame de início.
        """
        csv_file = self._find_dynamic_events_file(match_id)
        if not csv_file or not csv_file.exists():
            return []

        try:
            # Carrega e filtra passes usando Polars
            df = pl.read_csv(csv_file, infer_schema_length=10000, ignore_errors=True)

            # Filtro: event_type com 'pass' ou presença de pass_outcome / pass_distance
            pass_filter = (
                (pl.col("event_type").str.to_lowercase().str.contains("pass")) |
                (pl.col("pass_outcome").is_not_null())
            )
            df_passes = df.filter(pass_filter).sort("frame_start")

            pass_events: List[PassEvent] = []
            for row in df_passes.iter_rows(named=True):
                # Coordenadas e distâncias essenciais
                x_start = _safe_float(row.get("x_start")) or 0.0
                y_start = _safe_float(row.get("y_start")) or 0.0
                x_end = _safe_float(row.get("x_end")) or 0.0
                y_end = _safe_float(row.get("y_end")) or 0.0
                pass_distance = _safe_float(row.get("pass_distance")) or math.hypot(x_end - x_start, y_end - y_start)
                pass_angle = _safe_float(row.get("pass_angle")) or 0.0
                pass_outcome = _safe_str(row.get("pass_outcome")) or "unknown"

                evt = PassEvent(
                    event_id=str(row.get("event_id") or f"pass_{row.get('index', 0)}"),
                    match_id=_safe_int(row.get("match_id")) or match_id,
                    frame_start=_safe_int(row.get("frame_start")) or 0,
                    frame_end=_safe_int(row.get("frame_end")) or 0,
                    period=_safe_int(row.get("period")) or 1,
                    player_id=_safe_int(row.get("player_id")) or 0,
                    team_id=_safe_int(row.get("team_id")) or 0,
                    x_start=x_start,
                    y_start=y_start,
                    x_end=x_end,
                    y_end=y_end,
                    pass_distance=pass_distance,
                    pass_angle=pass_angle,
                    pass_outcome=pass_outcome,
                    time_start=_safe_str(row.get("time_start")),
                    time_end=_safe_str(row.get("time_end")),
                    minute_start=_safe_int(row.get("minute_start")),
                    second_start=_safe_int(row.get("second_start")),
                    player_name=_safe_str(row.get("player_name")),
                    player_position=_safe_str(row.get("player_position")),
                    player_targeted_id=_safe_int(row.get("player_targeted_id")),
                    player_targeted_name=_safe_str(row.get("player_targeted_name")),
                    separation_start=_safe_float(row.get("separation_start")),
                    separation_end=_safe_float(row.get("separation_end")),
                    separation_gain=_safe_float(row.get("separation_gain")),
                    last_defensive_line_x_start=_safe_float(row.get("last_defensive_line_x_start")),
                    last_defensive_line_x_end=_safe_float(row.get("last_defensive_line_x_end")),
                    delta_to_last_defensive_line_start=_safe_float(row.get("delta_to_last_defensive_line_start")),
                    interplayer_distance_start=_safe_float(row.get("interplayer_distance_start") or row.get("interplayer_distance")),
                    angle_of_engagement=_safe_float(row.get("angle_of_engagement")),
                    inside_defensive_shape_start=_safe_bool(row.get("inside_defensive_shape_start")) if row.get("inside_defensive_shape_start") is not None else None,
                    first_line_break=_safe_bool(row.get("first_line_break")) if row.get("first_line_break") is not None else None,
                    last_line_break=_safe_bool(row.get("last_line_break")) if row.get("last_line_break") is not None else None,
                    lead_to_shot=_safe_bool(row.get("lead_to_shot")),
                    lead_to_goal=_safe_bool(row.get("lead_to_goal")),
                    xthreat=_safe_float(row.get("xthreat")),
                    xpass_completion=_safe_float(row.get("xpass_completion") or row.get("player_targeted_xpass_completion")),
                    passing_option_score=_safe_float(row.get("passing_option_score"))
                )
                pass_events.append(evt)

            return pass_events
        except Exception:
            return []

    def get_off_ball_run_events(self, match_id: int) -> List[OffBallRunEvent]:
        """Recupera e instancia todas as corridas de desmarque sem bola de uma partida.

        Args:
            match_id: Identificador numérico da partida.

        Returns:
            Lista de entidades OffBallRunEvent ordenadas por frame de início.
        """
        csv_file = self._find_dynamic_events_file(match_id)
        if not csv_file or not csv_file.exists():
            return []

        try:
            df = pl.read_csv(csv_file, infer_schema_length=10000, ignore_errors=True)

            # Filtro: event_type contendo 'off_ball_run' ou 'run' ou presença de associated_off_ball_run_subtype
            run_filter = (
                (pl.col("event_type").str.to_lowercase().str.contains("off_ball_run|run")) |
                (pl.col("associated_off_ball_run_subtype").is_not_null())
            )
            df_runs = df.filter(run_filter).sort("frame_start")

            run_events: List[OffBallRunEvent] = []
            for row in df_runs.iter_rows(named=True):
                x_start = _safe_float(row.get("x_start")) or 0.0
                y_start = _safe_float(row.get("y_start")) or 0.0
                x_end = _safe_float(row.get("x_end")) or 0.0
                y_end = _safe_float(row.get("y_end")) or 0.0
                distance_covered = _safe_float(row.get("distance_covered")) or math.hypot(x_end - x_start, y_end - y_start)

                evt = OffBallRunEvent(
                    event_id=str(row.get("event_id") or f"run_{row.get('index', 0)}"),
                    match_id=_safe_int(row.get("match_id")) or match_id,
                    frame_start=_safe_int(row.get("frame_start")) or 0,
                    frame_end=_safe_int(row.get("frame_end")) or 0,
                    period=_safe_int(row.get("period")) or 1,
                    player_id=_safe_int(row.get("player_id")) or 0,
                    team_id=_safe_int(row.get("team_id")) or 0,
                    x_start=x_start,
                    y_start=y_start,
                    x_end=x_end,
                    y_end=y_end,
                    time_start=_safe_str(row.get("time_start")),
                    time_end=_safe_str(row.get("time_end")),
                    minute_start=_safe_int(row.get("minute_start")),
                    second_start=_safe_int(row.get("second_start")),
                    player_name=_safe_str(row.get("player_name")),
                    player_position=_safe_str(row.get("player_position")),
                    distance_covered=distance_covered,
                    speed_avg=_safe_float(row.get("speed_avg")),
                    separation_start=_safe_float(row.get("separation_start")),
                    separation_end=_safe_float(row.get("separation_end")),
                    separation_gain=_safe_float(row.get("separation_gain")),
                    last_defensive_line_x_start=_safe_float(row.get("last_defensive_line_x_start")),
                    last_defensive_line_x_end=_safe_float(row.get("last_defensive_line_x_end")),
                    delta_to_last_defensive_line_start=_safe_float(row.get("delta_to_last_defensive_line_start")),
                    delta_to_last_defensive_line_gain=_safe_float(row.get("delta_to_last_defensive_line_gain")),
                    inside_defensive_shape_start=_safe_bool(row.get("inside_defensive_shape_start")) if row.get("inside_defensive_shape_start") is not None else None,
                    inside_defensive_shape_end=_safe_bool(row.get("inside_defensive_shape_end")) if row.get("inside_defensive_shape_end") is not None else None,
                    targeted=_safe_bool(row.get("targeted")) if row.get("targeted") is not None else None,
                    received=_safe_bool(row.get("received")) if row.get("received") is not None else None,
                    received_in_space=_safe_bool(row.get("received_in_space")) if row.get("received_in_space") is not None else None,
                    dangerous=_safe_bool(row.get("dangerous")) if row.get("dangerous") is not None else None,
                    lead_to_shot=_safe_bool(row.get("lead_to_shot")),
                    lead_to_goal=_safe_bool(row.get("lead_to_goal")),
                    xthreat=_safe_float(row.get("xthreat"))
                )
                run_events.append(evt)

            return run_events
        except Exception:
            return []
