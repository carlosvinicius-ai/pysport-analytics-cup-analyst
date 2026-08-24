"""Testes unitários para validação de conformidade dos protocolos de repositório."""

from typing import List, Optional
import pytest
from src.domain.entities.event import OffBallRunEvent, PassEvent
from src.domain.entities.frame import TrackingFrame
from src.domain.entities.match import Match, Team
from src.domain.protocols.repository import (
    IDatasetRepository,
    IEventRepository,
    IMatchRepository,
    ITrackingRepository,
)


class FakeMatchRepository:
    """Implementação Fake/Mock para testes de IMatchRepository."""

    def __init__(self, matches: Optional[List[Match]] = None):
        self._matches = matches or []

    def get_match(self, match_id: int) -> Optional[Match]:
        for m in self._matches:
            if m.id == match_id:
                return m
        return None

    def list_matches(self) -> List[Match]:
        return list(self._matches)


class FakeEventRepository:
    """Implementação Fake/Mock para testes de IEventRepository."""

    def __init__(
        self,
        passes: Optional[List[PassEvent]] = None,
        runs: Optional[List[OffBallRunEvent]] = None,
    ):
        self._passes = passes or []
        self._runs = runs or []

    def get_pass_events(self, match_id: int) -> List[PassEvent]:
        return [p for p in self._passes if p.match_id == match_id]

    def get_off_ball_run_events(self, match_id: int) -> List[OffBallRunEvent]:
        return [r for r in self._runs if r.match_id == match_id]


class FakeTrackingRepository:
    """Implementação Fake/Mock para testes de ITrackingRepository."""

    def __init__(self, frames: Optional[List[TrackingFrame]] = None):
        self._frames = frames or []

    def get_tracking_frames(self, match_id: int) -> List[TrackingFrame]:
        return list(self._frames)

    def get_frame_count(self, match_id: int) -> int:
        return len(self._frames)


class FakeFullDatasetRepository:
    """Implementação Fake completa que satisfaz IDatasetRepository."""

    def __init__(self):
        self.match_repo = FakeMatchRepository()
        self.event_repo = FakeEventRepository()
        self.tracking_repo = FakeTrackingRepository()

    def get_match(self, match_id: int) -> Optional[Match]:
        return self.match_repo.get_match(match_id)

    def list_matches(self) -> List[Match]:
        return self.match_repo.list_matches()

    def get_pass_events(self, match_id: int) -> List[PassEvent]:
        return self.event_repo.get_pass_events(match_id)

    def get_off_ball_run_events(self, match_id: int) -> List[OffBallRunEvent]:
        return self.event_repo.get_off_ball_run_events(match_id)

    def get_tracking_frames(self, match_id: int) -> List[TrackingFrame]:
        return self.tracking_repo.get_tracking_frames(match_id)

    def get_frame_count(self, match_id: int) -> int:
        return self.tracking_repo.get_frame_count(match_id)


class IncompleteRepository:
    """Classe que não implementa todos os métodos exigidos por IMatchRepository."""
    def get_match(self, match_id: int) -> Optional[Match]:
        return None


def test_match_repository_protocol_conformance():
    """Valida a conformidade de runtime_checkable do protocolo IMatchRepository."""
    repo = FakeMatchRepository()
    assert isinstance(repo, IMatchRepository)

    incomplete = IncompleteRepository()
    assert not isinstance(incomplete, IMatchRepository)


def test_event_repository_protocol_conformance():
    """Valida a conformidade do protocolo IEventRepository."""
    repo = FakeEventRepository()
    assert isinstance(repo, IEventRepository)


def test_tracking_repository_protocol_conformance():
    """Valida a conformidade do protocolo ITrackingRepository."""
    repo = FakeTrackingRepository()
    assert isinstance(repo, ITrackingRepository)


def test_full_dataset_repository_protocol_conformance():
    """Valida a conformidade do protocolo composto IDatasetRepository."""
    full_repo = FakeFullDatasetRepository()
    assert isinstance(full_repo, IDatasetRepository)
    assert isinstance(full_repo, IMatchRepository)
    assert isinstance(full_repo, IEventRepository)
    assert isinstance(full_repo, ITrackingRepository)
