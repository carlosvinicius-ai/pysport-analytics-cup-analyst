"""Protocolos e contratos de repositório da camada de domínio.

Define abstrações puras para acesso aos dados de partidas, eventos espaciais e tracking.
Clean Architecture - Inversão de Dependência (DIP) e Segregação de Interfaces (ISP).
"""

from typing import List, Optional, Protocol, runtime_checkable
from src.domain.entities.event import OffBallRunEvent, PassEvent
from src.domain.entities.frame import TrackingFrame
from src.domain.entities.match import Match


@runtime_checkable
class IMatchRepository(Protocol):
    """Contrato abstrato para consulta e recuperação de metadados de partidas e elencos."""

    def get_match(self, match_id: int) -> Optional[Match]:
        """Recupera os detalhes completos de uma partida pelo seu identificador.

        Args:
            match_id: Identificador numérico da partida.

        Returns:
            Entidade Match se encontrada, caso contrário None.
        """
        ...

    def list_matches(self) -> List[Match]:
        """Lista todas as partidas disponíveis na base histórica.

        Returns:
            Lista de entidades Match carregadas.
        """
        ...


@runtime_checkable
class IEventRepository(Protocol):
    """Contrato abstrato para recuperação de eventos dinâmicos e espaciais."""

    def get_pass_events(self, match_id: int) -> List[PassEvent]:
        """Recupera todos os eventos de passe registrados para uma partida.

        Args:
            match_id: Identificador numérico da partida.

        Returns:
            Lista de entidades PassEvent ordenadas cronologicamente.
        """
        ...

    def get_off_ball_run_events(self, match_id: int) -> List[OffBallRunEvent]:
        """Recupera todas as corridas de desmarque sem bola de uma partida.

        Args:
            match_id: Identificador numérico da partida.

        Returns:
            Lista de entidades OffBallRunEvent ordenadas cronologicamente.
        """
        ...


@runtime_checkable
class ITrackingRepository(Protocol):
    """Contrato abstrato para recuperação de frames de tracking espacial."""

    def get_tracking_frames(self, match_id: int) -> List[TrackingFrame]:
        """Recupera a sequência completa de frames de tracking de uma partida.

        Args:
            match_id: Identificador numérico da partida.

        Returns:
            Lista sequencial de instâncias de TrackingFrame.
        """
        ...

    def get_frame_count(self, match_id: int) -> int:
        """Retorna o volume total de frames disponíveis para a partida especificada.

        Args:
            match_id: Identificador numérico da partida.

        Returns:
            Número total de frames registrados.
        """
        ...


@runtime_checkable
class IDatasetRepository(IMatchRepository, IEventRepository, ITrackingRepository, Protocol):
    """Contrato unificado agregando todas as operações de dados da plataforma."""
    ...
