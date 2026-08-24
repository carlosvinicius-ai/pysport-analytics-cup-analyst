"""Testes unitários para as entidades de eventos espaciais e frames de tracking."""

from dataclasses import FrozenInstanceError
import pytest
from src.domain.entities.event import PassEvent, OffBallRunEvent
from src.domain.entities.frame import PlayerPosition, BallPosition, TrackingFrame


def test_pass_event_creation_and_completion_property():
    """Testa a criação do PassEvent e o funcionamento da propriedade is_completed."""
    pass_evt = PassEvent(
        event_id="evt_101",
        match_id=1886347,
        frame_start=1000,
        frame_end=1050,
        period=1,
        player_id=10,
        team_id=1,
        x_start=-10.5,
        y_start=5.0,
        x_end=15.0,
        y_end=12.0,
        pass_distance=26.43,
        pass_angle=0.26,
        pass_outcome="successful",
        separation_start=3.5,
        last_defensive_line_x_start=20.0,
        xthreat=0.045,
        xpass_completion=0.82
    )

    assert pass_evt.event_id == "evt_101"
    assert pass_evt.is_completed is True
    assert pass_evt.xthreat == 0.045
    assert pass_evt.xpass_completion == 0.82
    assert pass_evt.x_start == -10.5
    assert pass_evt.pass_distance == 26.43


def test_pass_event_immutability():
    """Valida que o PassEvent é estritamente imutável (frozen=True)."""
    pass_evt = PassEvent(
        event_id="evt_102",
        match_id=1886347,
        frame_start=200,
        frame_end=240,
        period=1,
        player_id=5,
        team_id=1,
        x_start=0.0,
        y_start=0.0,
        x_end=10.0,
        y_end=0.0,
        pass_distance=10.0,
        pass_angle=0.0,
        pass_outcome="unsuccessful"
    )
    assert pass_evt.is_completed is False

    with pytest.raises(FrozenInstanceError):
        pass_evt.x_start = 5.0  # type: ignore


def test_off_ball_run_event_and_separation_gain():
    """Valida a criação do OffBallRunEvent e o ganho de separação."""
    run_evt = OffBallRunEvent(
        event_id="run_201",
        match_id=1886347,
        frame_start=500,
        frame_end=580,
        period=1,
        player_id=9,
        team_id=1,
        x_start=10.0,
        y_start=-15.0,
        x_end=25.0,
        y_end=-10.0,
        distance_covered=15.81,
        speed_avg=6.2,
        separation_start=2.0,
        separation_end=5.5,
        separation_gain=3.5,
        inside_defensive_shape_start=True,
        delta_to_last_defensive_line_start=5.0,
        targeted=True,
        received=True
    )

    assert run_evt.event_id == "run_201"
    assert run_evt.net_separation_gain == 3.5
    assert run_evt.targeted is True
    assert run_evt.inside_defensive_shape_start is True

    with pytest.raises(FrozenInstanceError):
        run_evt.separation_end = 6.0  # type: ignore


def test_off_ball_run_fallback_separation_calculation():
    """Valida o cálculo dinâmico de ganho de separação quando separation_gain é nulo."""
    run_evt = OffBallRunEvent(
        event_id="run_202",
        match_id=1886347,
        frame_start=600,
        frame_end=650,
        period=1,
        player_id=11,
        team_id=2,
        x_start=0.0,
        y_start=0.0,
        x_end=10.0,
        y_end=5.0,
        separation_start=1.5,
        separation_end=4.0,
        separation_gain=None
    )
    assert run_evt.net_separation_gain == 2.5


def test_tracking_frame_and_positions():
    """Valida a criação de TrackingFrame e métodos de busca de jogadores e equipes."""
    p1 = PlayerPosition(player_id=1, team_id=10, x=-20.0, y=10.0, speed=3.5)
    p2 = PlayerPosition(player_id=2, team_id=10, x=-15.0, y=-5.0, speed=4.2)
    p3 = PlayerPosition(player_id=15, team_id=20, x=-18.0, y=8.0, speed=5.0)
    ball = BallPosition(x=-19.0, y=9.0, z=0.2, is_detected=True)

    frame = TrackingFrame(
        frame_idx=1500,
        period=1,
        time_seconds=60.0,
        player_positions=(p1, p2, p3),
        ball=ball
    )

    assert frame.frame_idx == 1500
    assert frame.total_players_detected == 3
    assert frame.ball is not None
    assert frame.ball.z == 0.2

    # Helpers de consulta
    found = frame.get_player_position(2)
    assert found is not None
    assert found.x == -15.0

    not_found = frame.get_player_position(99)
    assert not_found is None

    team_10_players = frame.get_team_positions(10)
    assert len(team_10_players) == 2
    assert p1 in team_10_players and p2 in team_10_players

    with pytest.raises(FrozenInstanceError):
        frame.frame_idx = 1501  # type: ignore
