"""Testes de integração para o SkillCornerTrackingParser."""

from pathlib import Path
import pytest
from src.domain.entities.event import OffBallRunEvent, PassEvent
from src.domain.protocols.repository import IEventRepository
from src.infrastructure.parsers.tracking_parser import SkillCornerTrackingParser


@pytest.fixture
def opendata_dir() -> Path:
    """Retorna o caminho raiz para os dados da SkillCorner Open Data."""
    project_root = Path(__file__).resolve().parents[3]
    return project_root / "data" / "opendata"


def test_tracking_parser_protocol_conformance(opendata_dir: Path):
    """Valida se o SkillCornerTrackingParser respeita o protocolo IEventRepository."""
    parser = SkillCornerTrackingParser(data_dir=opendata_dir)
    assert isinstance(parser, IEventRepository)


def test_get_pass_events_real_data(opendata_dir: Path):
    """Valida a extração de eventos de passe a partir dos dados reais da partida 1886347."""
    parser = SkillCornerTrackingParser(data_dir=opendata_dir)
    match_id = 1886347
    passes = parser.get_pass_events(match_id)

    assert isinstance(passes, list)
    assert len(passes) > 0

    sample_pass = passes[0]
    assert isinstance(sample_pass, PassEvent)
    assert sample_pass.match_id == match_id
    assert sample_pass.event_id is not None
    assert isinstance(sample_pass.x_start, float)
    assert isinstance(sample_pass.y_start, float)
    assert isinstance(sample_pass.pass_distance, float)
    assert sample_pass.pass_distance >= 0.0

    # Verifica ordenação temporal por frame_start
    for i in range(len(passes) - 1):
        assert passes[i].frame_start <= passes[i + 1].frame_start


def test_get_off_ball_run_events_real_data(opendata_dir: Path):
    """Valida a extração de corridas de desmarque da partida 1886347."""
    parser = SkillCornerTrackingParser(data_dir=opendata_dir)
    match_id = 1886347
    runs = parser.get_off_ball_run_events(match_id)

    assert isinstance(runs, list)
    assert len(runs) > 0

    sample_run = runs[0]
    assert isinstance(sample_run, OffBallRunEvent)
    assert sample_run.match_id == match_id
    assert sample_run.event_id is not None
    assert isinstance(sample_run.distance_covered, float)
    assert sample_run.distance_covered >= 0.0
    assert isinstance(sample_run.net_separation_gain, float)


def test_get_events_nonexistent_match(opendata_dir: Path):
    """Valida que uma partida inexistente retorna listas vazias sem exceção."""
    parser = SkillCornerTrackingParser(data_dir=opendata_dir)
    passes = parser.get_pass_events(99999999)
    runs = parser.get_off_ball_run_events(99999999)

    assert passes == []
    assert runs == []
