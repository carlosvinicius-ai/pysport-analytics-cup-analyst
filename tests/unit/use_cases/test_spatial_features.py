"""Testes unitários para o use case de extração de features espaciais."""

import pytest
import polars as pl
from src.domain.entities.event import PassEvent
from src.domain.protocols.repository import IEventRepository
from src.use_cases.feature_extraction.spatial_features import (
    ComputeSpatialFeaturesUseCase,
    SpatialPassFeatures,
)


class MockEventRepository(IEventRepository):
    """Mock de repositório para testes unitários de casos de uso."""

    def __init__(self, passes=None, runs=None):
        self._passes = passes or []
        self._runs = runs or []

    def get_pass_events(self, match_id: int):
        return [p for p in self._passes if p.match_id == match_id]

    def get_off_ball_run_events(self, match_id: int):
        return [r for r in self._runs if r.match_id == match_id]


def test_compute_for_single_pass_geometry_and_goal():
    """Valida o cálculo exato de progressão, deslocamento lateral e distâncias ao gol."""
    pass_evt = PassEvent(
        event_id="pass_001",
        match_id=1886347,
        frame_start=100,
        frame_end=140,
        period=1,
        player_id=10,
        team_id=1,
        x_start=0.0,
        y_start=0.0,
        x_end=20.0,
        y_end=15.0,
        pass_distance=25.0,
        pass_angle=0.6435,
        pass_outcome="successful",
        interplayer_distance_start=2.5,  # Menor que 3m -> Pressão True
        separation_start=3.0,
        separation_end=5.0,
        separation_gain=2.0,
        xthreat=0.035
    )

    use_case = ComputeSpatialFeaturesUseCase(pitch_length=105.0, pitch_width=68.0)
    feat = use_case.compute_for_pass(pass_evt)

    assert isinstance(feat, SpatialPassFeatures)
    assert feat.event_id == "pass_001"
    assert feat.progression_x == 20.0  # 20.0 - 0.0
    assert feat.lateral_displacement == 15.0  # |15.0 - 0.0|
    assert feat.pass_distance == 25.0
    assert feat.is_completed == 1

    # Distância ao gol (alvo em x = 52.5, y = 0.0)
    # Start: (0, 0) -> distância = 52.5
    assert pytest.approx(feat.distance_to_goal_start, 0.01) == 52.5
    # End: (20, 15) -> dx = 32.5, dy = 15 -> sqrt(32.5^2 + 15^2) = sqrt(1056.25 + 225) = 35.794
    assert pytest.approx(feat.distance_to_goal_end, 0.01) == 35.794

    # Pressão defensiva
    assert feat.interplayer_distance_start == 2.5
    assert feat.has_defensive_pressure is True
    assert feat.separation_gain == 2.0


def test_compute_for_pass_imputation_free_space():
    """Valida a imputação segura quando não há oponente próximo (espaço livre)."""
    pass_evt = PassEvent(
        event_id="pass_002",
        match_id=1886347,
        frame_start=200,
        frame_end=240,
        period=1,
        player_id=4,
        team_id=1,
        x_start=-30.0,
        y_start=10.0,
        x_end=-10.0,
        y_end=10.0,
        pass_distance=20.0,
        pass_angle=0.0,
        pass_outcome="incomplete",
        interplayer_distance_start=None,  # Ausente
        separation_start=None
    )

    use_case = ComputeSpatialFeaturesUseCase()
    feat = use_case.compute_for_pass(pass_evt)

    assert feat.is_completed == 0
    assert feat.interplayer_distance_start == 15.0  # Imputação neutra
    assert feat.has_defensive_pressure is False
    assert feat.separation_start == 5.0  # Default neutro


def test_compute_for_match_and_to_dataframe():
    """Valida a extração em lote por partida e a conversão para DataFrame Polars."""
    p1 = PassEvent(
        event_id="p1",
        match_id=100,
        frame_start=10,
        frame_end=30,
        period=1,
        player_id=7,
        team_id=1,
        x_start=0.0,
        y_start=0.0,
        x_end=10.0,
        y_end=0.0,
        pass_distance=10.0,
        pass_angle=0.0,
        pass_outcome="completed"
    )
    p2 = PassEvent(
        event_id="p2",
        match_id=100,
        frame_start=40,
        frame_end=60,
        period=1,
        player_id=8,
        team_id=1,
        x_start=10.0,
        y_start=0.0,
        x_end=20.0,
        y_end=5.0,
        pass_distance=11.18,
        pass_angle=0.46,
        pass_outcome="unsuccessful"
    )

    mock_repo = MockEventRepository(passes=[p1, p2])
    use_case = ComputeSpatialFeaturesUseCase(event_repository=mock_repo)

    features = use_case.compute_for_match(100)
    assert len(features) == 2

    # Conversão para Polars DataFrame
    df = use_case.to_dataframe(features)
    assert isinstance(df, pl.DataFrame)
    assert df.height == 2
    assert "progression_x" in df.columns
    assert "lateral_displacement" in df.columns
    assert "distance_to_goal_start" in df.columns
    assert "is_completed" in df.columns
    assert df["is_completed"].to_list() == [1, 0]


def test_to_dataframe_empty():
    """Valida que to_dataframe com lista vazia retorna um DataFrame vazio sem erros."""
    use_case = ComputeSpatialFeaturesUseCase()
    df = use_case.to_dataframe([])
    assert isinstance(df, pl.DataFrame)
    assert df.height == 0
