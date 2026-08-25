"""Parser concreto para metadados e elencos de partidas da SkillCorner.

Implementa o protocolo IMatchRepository da camada de domínio.
Lê e converte arquivos matches.json e <match_id>_match.json em entidades puras.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from src.domain.entities.match import Match, MatchPeriod, PitchDimensions, Stadium, Team
from src.domain.entities.player import Player, PlayerPlayingTime, PlayerRole
from src.domain.protocols.repository import IMatchRepository


class SkillCornerMatchParser:
    """Implementação concreta de IMatchRepository para leitura de JSONs locais da SkillCorner."""

    def __init__(self, data_dir: Union[str, Path]):
        """Inicializa o parser com o diretório raiz de dados.

        Args:
            data_dir: Caminho base para a pasta de dados (ex: 'data/opendata').
        """
        self.data_dir = Path(data_dir)

    def _find_matches_index_file(self) -> Optional[Path]:
        """Localiza o arquivo matches.json no diretório de dados."""
        # Tenta data/matches.json, matches.json ou busca recursiva
        direct = self.data_dir / "data" / "matches.json"
        if direct.exists():
            return direct
        root_matches = self.data_dir / "matches.json"
        if root_matches.exists():
            return root_matches
        found = list(self.data_dir.glob("**/matches.json"))
        return found[0] if found else None

    def _find_match_file(self, match_id: int) -> Optional[Path]:
        """Localiza o arquivo JSON detalhado de uma partida específica (<match_id>_match.json).

        Args:
            match_id: Identificador numérico da partida.

        Returns:
            Caminho do arquivo se encontrado, caso contrário None.
        """
        filename = f"{match_id}_match.json"
        # Tenta estrutura padrão data/matches/<id>/<id>_match.json
        direct = self.data_dir / "data" / "matches" / str(match_id) / filename
        if direct.exists():
            return direct
        direct_alt = self.data_dir / "matches" / str(match_id) / filename
        if direct_alt.exists():
            return direct_alt
        # Busca recursiva como fallback
        found = list(self.data_dir.glob(f"**/{filename}"))
        return found[0] if found else None

    def _parse_team(self, team_data: Optional[Dict[str, Any]], kit_data: Optional[Dict[str, Any]] = None) -> Team:
        """Converte dicionário de equipe para a entidade de domínio Team."""
        if not team_data:
            return Team(id=0, name="Desconhecido", short_name="DESC")
        
        jersey_color = None
        if kit_data and isinstance(kit_data, dict):
            jersey_color = kit_data.get("jersey_color")

        return Team(
            id=team_data.get("id", 0),
            name=team_data.get("name", team_data.get("short_name", "Desconhecido")),
            short_name=team_data.get("short_name", team_data.get("name", "DESC")),
            acronym=team_data.get("acronym"),
            jersey_color=jersey_color
        )

    def _parse_stadium(self, stadium_data: Optional[Dict[str, Any]]) -> Optional[Stadium]:
        """Converte dicionário de estádio para a entidade de domínio Stadium."""
        if not stadium_data or not isinstance(stadium_data, dict):
            return None
        return Stadium(
            id=stadium_data.get("id", 0),
            name=stadium_data.get("name", "Estádio Padrão"),
            city=stadium_data.get("city"),
            capacity=stadium_data.get("capacity")
        )

    def _parse_pitch(self, match_data: Dict[str, Any]) -> PitchDimensions:
        """Extrai as dimensões do gramado ou aplica o padrão FIFA (105m x 68m)."""
        length = match_data.get("pitch_length")
        width = match_data.get("pitch_width")

        length_val = float(length) if length is not None else 105.0
        width_val = float(width) if width is not None else 68.0

        return PitchDimensions(length=length_val, width=width_val)

    def _parse_periods(self, periods_data: Optional[List[Dict[str, Any]]]) -> List[MatchPeriod]:
        """Converte lista de períodos para instâncias de MatchPeriod."""
        if not periods_data or not isinstance(periods_data, list):
            return []
        
        periods = []
        for p in periods_data:
            if not isinstance(p, dict):
                continue
            periods.append(
                MatchPeriod(
                    period=p.get("period", 1),
                    name=p.get("name", f"Período {p.get('period', 1)}"),
                    start_frame=p.get("start_frame", 0),
                    end_frame=p.get("end_frame", 0),
                    duration_frames=p.get("duration_frames", 0),
                    duration_minutes=float(p.get("duration_minutes", 0.0))
                )
            )
        return periods

    def _parse_player(self, p_data: Dict[str, Any]) -> Player:
        """Converte dicionário de jogador do JSON para a entidade Player."""
        # Papel tático do jogador
        role_obj = None
        role_data = p_data.get("player_role")
        if role_data and isinstance(role_data, dict):
            role_obj = PlayerRole(
                id=role_data.get("id", 0),
                name=role_data.get("name", "Jogador"),
                acronym=role_data.get("acronym", "JOG"),
                position_group=role_data.get("position_group", "Indefinido")
            )

        # Minutagem e tempo de jogo
        playing_time_obj = PlayerPlayingTime()
        pt_data = p_data.get("playing_time")
        if pt_data and isinstance(pt_data, dict):
            total_pt = pt_data.get("total", {})
            if isinstance(total_pt, dict):
                playing_time_obj = PlayerPlayingTime(
                    minutes_played=float(total_pt.get("minutes_played", 0.0) or 0.0),
                    minutes_tip=float(total_pt.get("minutes_tip", 0.0) or 0.0),
                    minutes_otip=float(total_pt.get("minutes_otip", 0.0) or 0.0),
                    start_frame=total_pt.get("start_frame"),
                    end_frame=total_pt.get("end_frame")
                )

        return Player(
            id=p_data.get("id", 0),
            short_name=p_data.get("short_name", "Jogador"),
            first_name=p_data.get("first_name"),
            last_name=p_data.get("last_name"),
            birthday=p_data.get("birthday"),
            gender=p_data.get("gender", "male"),
            trackable_object=p_data.get("trackable_object"),
            number=p_data.get("number"),
            role=role_obj,
            team_id=p_data.get("team_id"),
            team_player_id=p_data.get("team_player_id"),
            yellow_card=p_data.get("yellow_card", 0) or 0,
            red_card=p_data.get("red_card", 0) or 0,
            injured=bool(p_data.get("injured", False)),
            goal=p_data.get("goal", 0) or 0,
            own_goal=p_data.get("own_goal", 0) or 0,
            playing_time=playing_time_obj
        )

    def get_match(self, match_id: int) -> Optional[Match]:
        """Recupera os detalhes completos de uma partida incluindo elenco e gramado.

        Args:
            match_id: Identificador numérico da partida.

        Returns:
            Entidade Match se o arquivo for encontrado e parseado, caso contrário None.
        """
        match_file = self._find_match_file(match_id)
        if not match_file or not match_file.exists():
            return None

        try:
            with open(match_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            home_team = self._parse_team(data.get("home_team"), data.get("home_team_kit"))
            away_team = self._parse_team(data.get("away_team"), data.get("away_team_kit"))
            pitch = self._parse_pitch(data)
            stadium = self._parse_stadium(data.get("stadium"))
            periods = self._parse_periods(data.get("match_periods"))

            # Parseia lista de jogadores
            players_list = []
            for p_dict in data.get("players", []):
                if isinstance(p_dict, dict):
                    players_list.append(self._parse_player(p_dict))

            # Constrói entidade Match de domínio
            return Match(
                id=data.get("id", match_id),
                date_time=data.get("date_time", ""),
                home_team=home_team,
                away_team=away_team,
                status=data.get("status", "closed"),
                competition_id=data.get("competition_edition", {}).get("competition", {}).get("id")
                if isinstance(data.get("competition_edition"), dict) else None,
                season_id=data.get("competition_edition", {}).get("season", {}).get("id")
                if isinstance(data.get("competition_edition"), dict) else None,
                home_team_score=data.get("home_team_score"),
                away_team_score=data.get("away_team_score"),
                pitch_dimensions=pitch,
                stadium=stadium,
                periods=periods,
                players=players_list
            )
        except Exception:
            return None

    def list_matches(self) -> List[Match]:
        """Lista todas as partidas registradas no índice matches.json da base.

        Returns:
            Lista de entidades Match carregadas.
        """
        index_file = self._find_matches_index_file()
        if not index_file or not index_file.exists():
            return []

        matches = []
        try:
            with open(index_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list):
                for item in data:
                    if not isinstance(item, dict):
                        continue
                    m_id = item.get("id")
                    if m_id is None:
                        continue
                    # Tenta carregar detalhado se existir arquivo individual, senão constrói básico
                    detailed_match = self.get_match(m_id)
                    if detailed_match:
                        matches.append(detailed_match)
                    else:
                        home_team = self._parse_team(item.get("home_team"))
                        away_team = self._parse_team(item.get("away_team"))
                        basic_match = Match(
                            id=m_id,
                            date_time=item.get("date_time", ""),
                            home_team=home_team,
                            away_team=away_team,
                            status=item.get("status", "closed"),
                            competition_id=item.get("competition_id"),
                            season_id=item.get("season_id")
                        )
                        matches.append(basic_match)
        except Exception:
            pass

        return matches
