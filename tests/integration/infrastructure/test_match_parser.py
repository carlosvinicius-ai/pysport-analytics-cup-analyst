"""Testes de integração e unitários para o SkillCornerMatchParser."""

from pathlib import Path
import pytest
from src.domain.entities.match import Match
from src.domain.protocols.repository import IMatchRepository
from src.infrastructure.parsers.match_parser import SkillCornerMatchParser


@pytest.fixture
def opendata_dir() -> Path:
    """Retorna o caminho raiz para os dados da SkillCorner Open Data."""
    # tests/integration/infrastructure/test_match_parser.py -> parents[3] é o root do projeto
    project_root = Path(__file__).resolve().parents[3]
    return project_root / "data" / "opendata"


def test_match_parser_protocol_conformance(opendata_dir: Path):
    """Valida se o SkillCornerMatchParser respeita o protocolo IMatchRepository."""
    parser = SkillCornerMatchParser(data_dir=opendata_dir)
    assert isinstance(parser, IMatchRepository)


def test_get_match_real_data(opendata_dir: Path):
    """Valida a extração detalhada de uma partida real do dataset local (ex: 1886347)."""
    parser = SkillCornerMatchParser(data_dir=opendata_dir)
    match_id = 1886347
    match = parser.get_match(match_id)

    assert match is not None
    assert isinstance(match, Match)
    assert match.id == match_id
    assert match.home_team is not None
    assert match.away_team is not None
    assert len(match.home_team.name) > 0
    assert len(match.away_team.name) > 0

    # Dimensões do gramado
    assert match.pitch_dimensions is not None
    assert match.pitch_dimensions.length > 0
    assert match.pitch_dimensions.width > 0
    assert match.pitch_dimensions.area > 0

    # Elenco e jogadores
    assert len(match.players) > 0
    sample_player = match.players[0]
    assert sample_player.id > 0
    assert sample_player.short_name is not None
    assert sample_player.playing_time is not None

    # Métodos auxiliares de consulta na entidade
    found_player = match.get_player(sample_player.id)
    assert found_player is not None
    assert found_player.id == sample_player.id

    home_players = match.get_team_players(match.home_team.id)
    assert len(home_players) > 0


def test_list_matches_real_data(opendata_dir: Path):
    """Valida a listagem de todas as partidas a partir de matches.json."""
    parser = SkillCornerMatchParser(data_dir=opendata_dir)
    matches = parser.list_matches()

    assert isinstance(matches, list)
    assert len(matches) == 10  # 10 partidas disponíveis no opendata inspecionado
    for m in matches:
        assert isinstance(m, Match)
        assert m.id > 0
        assert m.home_team is not None
        assert m.away_team is not None


def test_get_nonexistent_match(opendata_dir: Path):
    """Valida que uma partida inexistente retorna None sem levantar exceções."""
    parser = SkillCornerMatchParser(data_dir=opendata_dir)
    match = parser.get_match(99999999)
    assert match is None
