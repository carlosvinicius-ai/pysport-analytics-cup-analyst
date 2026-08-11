"""Unit tests for domain entities (Player, Team, PitchDimensions, Match)."""

import pytest
from src.domain.entities.player import Player, PlayerRole, PlayerPlayingTime
from src.domain.entities.match import Match, Team, PitchDimensions, Stadium, MatchPeriod


def test_player_role_creation():
    role = PlayerRole(id=1, name="Center Back", acronym="CB", position_group="Defender")
    assert role.id == 1
    assert role.name == "Center Back"
    assert role.acronym == "CB"
    assert role.position_group == "Defender"


def test_player_full_name_and_defaults():
    player = Player(
        id=10,
        short_name="C. Ronaldo",
        first_name="Cristiano",
        last_name="Ronaldo",
        number=7,
        team_id=100
    )
    assert player.full_name == "Cristiano Ronaldo"
    assert player.short_name == "C. Ronaldo"
    assert player.number == 7
    assert player.yellow_card == 0
    assert player.injured is False


def test_player_fallback_full_name():
    player = Player(id=20, short_name="Pelé")
    assert player.full_name == "Pelé"


def test_pitch_dimensions_area():
    pitch = PitchDimensions(length=105.0, width=68.0)
    assert pitch.length == 105.0
    assert pitch.width == 68.0
    assert pitch.area == 7140.0


def test_match_entity_and_roster_methods():
    home_team = Team(id=1, name="Home Club", short_name="HOM", acronym="HOM")
    away_team = Team(id=2, name="Away Club", short_name="AWY", acronym="AWY")
    pitch = PitchDimensions(length=100.0, width=64.0)

    p1 = Player(id=101, short_name="Player 1", team_id=1)
    p2 = Player(id=102, short_name="Player 2", team_id=1)
    p3 = Player(id=201, short_name="Player 3", team_id=2)

    match = Match(
        id=1886347,
        date_time="2024-10-15T15:00:00Z",
        home_team=home_team,
        away_team=away_team,
        pitch_dimensions=pitch,
        players=[p1, p2, p3]
    )

    assert match.id == 1886347
    assert match.home_team.short_name == "HOM"
    assert match.away_team.short_name == "AWY"
    assert len(match.players) == 3

    # Test roster helper methods
    found_player = match.get_player(102)
    assert found_player is not None
    assert found_player.short_name == "Player 2"

    not_found = match.get_player(999)
    assert not_found is None

    home_players = match.get_team_players(1)
    assert len(home_players) == 2
    assert p1 in home_players and p2 in home_players

    away_players = match.get_team_players(2)
    assert len(away_players) == 1
    assert p3 in away_players
