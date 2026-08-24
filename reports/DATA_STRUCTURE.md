# Relatório de Descoberta e Estrutura dos Dados — SkillCorner Open Data

Este relatório documenta a estrutura, schemas, relacionamentos entre entidades e volume total de dados da base SkillCorner Open Data.

## 1. Visão Geral e Estatísticas de Volume

> [!NOTE]
> Os volumes abaixo representam o conjunto total de dados abertos inspecionados localmente em `data/opendata`.

| Métrica | Valor |
| :--- | :--- |
| **Total de Partidas Disponíveis** | `10` |
| **Total de Jogadores Únicos** | `309` |
| **Total de Equipes Únicas** | `13` |
| **Total de Eventos Dinâmicos/Tracking (Registros)** | `47,853` |
| **Total de Fases de Jogo (Registros)** | `4,581` |

## 2. Árvore de Arquivos e Categorização dos Dados

### Metadados de Partidas (11 arquivos)
- `data\matches.json`
- `data\matches\1886347\1886347_match.json`
- `data\matches\1899585\1899585_match.json`
- `data\matches\1925299\1925299_match.json`
- `data\matches\1953632\1953632_match.json`
- `data\matches\1996435\1996435_match.json`
- `data\matches\2006229\2006229_match.json`
- `data\matches\2011166\2011166_match.json`
- `data\matches\2013725\2013725_match.json`
- `data\matches\2015213\2015213_match.json`
- `data\matches\2017461\2017461_match.json`

### Métricas Agregadas (3 arquivos)
- `data\aggregates\aus1league_obraggregates_20242025.csv`
- `data\aggregates\aus1league_passingaggregates_20242025.csv`
- `data\aggregates\aus1league_physicalaggregates_20242025.csv`

### Eventos Dinâmicos e Tracking Tático (10 arquivos)
- `data\matches\1886347\1886347_dynamic_events.csv`
- `data\matches\1899585\1899585_dynamic_events.csv`
- `data\matches\1925299\1925299_dynamic_events.csv`
- `data\matches\1953632\1953632_dynamic_events.csv`
- `data\matches\1996435\1996435_dynamic_events.csv`
- `data\matches\2006229\2006229_dynamic_events.csv`
- `data\matches\2011166\2011166_dynamic_events.csv`
- `data\matches\2013725\2013725_dynamic_events.csv`
- `data\matches\2015213\2015213_dynamic_events.csv`
- `data\matches\2017461\2017461_dynamic_events.csv`

### Fases do Jogo (10 arquivos)
- `data\matches\1886347\1886347_phases_of_play.csv`
- `data\matches\1899585\1899585_phases_of_play.csv`
- `data\matches\1925299\1925299_phases_of_play.csv`
- `data\matches\1953632\1953632_phases_of_play.csv`
- `data\matches\1996435\1996435_phases_of_play.csv`
- `data\matches\2006229\2006229_phases_of_play.csv`
- `data\matches\2011166\2011166_phases_of_play.csv`
- `data\matches\2013725\2013725_phases_of_play.csv`
- `data\matches\2015213\2015213_phases_of_play.csv`
- `data\matches\2017461\2017461_phases_of_play.csv`

## 3. Schemas, Tipos de Dados e Níveis de Aninhamento

### Schema de `matches.json` (Metadados Globais das Partidas)
Contém a lista de partidas com informações de data, competição, estádio e placar.
```json
{
  "id": "int",
  "date_time": "str",
  "home_team": {
    "id": "int",
    "short_name": "str"
  },
  "away_team": {
    "id": "int",
    "short_name": "str"
  },
  "status": "str",
  "competition_id": "int",
  "season_id": "int",
  "competition_edition_id": "int"
}
```

### Schema de `<match_id>_match.json` (Detalhes da Partida & Elencos)
Arquivo individual por partida contendo lista completa de jogadores, treinadores, árbitros, dimensões do campo e alinhamento tático.
```json
{
  "id": "int",
  "home_team_score": "int",
  "away_team_score": "int",
  "date_time": "str",
  "stadium": {
    "id": "int",
    "name": "str",
    "city": "str",
    "capacity": "int"
  },
  "home_team": {
    "id": "int",
    "name": "str",
    "short_name": "str",
    "acronym": "str"
  },
  "home_team_kit": {
    "id": "int",
    "team_id": "int",
    "season": {
      "id": "int",
      "start_year": "int",
      "end_year": "int",
      "name": "str"
    },
    "name": "str",
    "jersey_color": "str",
    "number_color": "str"
  },
  "away_team": {
    "id": "int",
    "name": "str",
    "short_name": "str",
    "acronym": "str"
  },
  "away_team_kit": {
    "id": "int",
    "team_id": "int",
    "season": {
      "id": "int",
      "start_year": "int",
      "end_year": "int",
      "name": "str"
    },
    "name": "str",
    "jersey_color": "str",
    "number_color": "str"
  },
  "home_team_coach": "NoneType",
  "away_team_coach": "NoneType",
  "home_team_playing_time": {
    "minutes_tip": "float",
    "minutes_otip": "float"
  },
  "away_team_playing_time": {
    "minutes_tip": "float",
    "minutes_otip": "float"
  },
  "competition_edition": {
    "id": "int",
    "competition": {
      "id": "int",
      "area": "str",
      "name": "str",
      "gender": "str",
      "age_group": "str"
    },
    "season": {
      "id": "int",
      "start_year": "int",
      "end_year": "int",
      "name": "str"
    },
    "name": "str"
  },
  "match_periods": "List[{'period': 'int', 'name': 'str', 'start_frame': 'int', 'end_frame': 'int', 'duration_frames': 'int', 'duration_minutes': 'float'}]",
  "competition_round": {
    "id": "int",
    "name": "str",
    "round_number": "int",
    "potential_overtime": "bool"
  },
  "referees": "List[Empty]",
  "players": "List[{'player_role': {'id': 'int', 'position_group': 'str', 'name': 'str', 'acronym': 'str'}, 'start_time': 'str', 'end_time': 'str', 'number': 'int', 'yellow_card': 'int', 'red_card': 'int', 'injured': 'bool', 'goal': 'int', 'own_goal': 'int', 'playing_time': {'total': {'minutes_tip': '...', 'minutes_otip': '...', 'start_frame': '...', 'end_frame': '...', 'minutes_played': '...', 'minutes_played_regular_time': '...'}, 'by_period': 'List[...]'}, 'team_player_id': 'int', 'team_id': 'int', 'id': 'int', 'first_name': 'str', 'last_name': 'str', 'short_name': 'str', 'birthday': 'str', 'trackable_object': 'int', 'gender': 'str'}]",
  "status": "str",
  "home_team_side": "List[str]",
  "ball": {
    "trackable_object": "int"
  },
  "pitch_length": "int",
  "pitch_width": "int"
}
```

### Schema de `<match_id>_dynamic_events.csv` (Eventos Dinâmicos & Posicionamento)
Dados em nível de evento com marcação temporal, posições (x, y), velocidade, aceleração e contexto de posse de bola.
| Coluna | Tipo de Dado |
| :--- | :--- |
| `event_id` | `object` |
| `index` | `int64` |
| `match_id` | `int64` |
| `frame_start` | `int64` |
| `frame_end` | `int64` |
| `frame_physical_start` | `float64` |
| `time_start` | `object` |
| `time_end` | `object` |
| `minute_start` | `int64` |
| `second_start` | `int64` |
| `duration` | `float64` |
| `period` | `int64` |
| `attacking_side_id` | `int64` |
| `attacking_side` | `object` |
| `event_type_id` | `int64` |
| `event_type` | `object` |
| `event_subtype_id` | `float64` |
| `event_subtype` | `object` |
| `player_id` | `int64` |
| `player_name` | `object` |
| `player_position_id` | `int64` |
| `player_position` | `object` |
| `player_in_possession_id` | `float64` |
| `player_in_possession_name` | `object` |
| `player_in_possession_position_id` | `float64` |
| `player_in_possession_position` | `object` |
| `team_id` | `int64` |
| `team_shortname` | `object` |
| `x_start` | `float64` |
| `y_start` | `float64` |
| `channel_id_start` | `int64` |
| `channel_start` | `object` |
| `third_id_start` | `int64` |
| `third_start` | `object` |
| `penalty_area_start` | `bool` |
| `x_end` | `float64` |
| `y_end` | `float64` |
| `channel_id_end` | `int64` |
| `channel_end` | `object` |
| `third_id_end` | `int64` |
| `third_end` | `object` |
| `penalty_area_end` | `bool` |
| `associated_player_possession_event_id` | `object` |
| `associated_player_possession_frame_start` | `float64` |
| `associated_player_possession_frame_end` | `float64` |
| `associated_player_possession_end_type_id` | `float64` |
| `associated_player_possession_end_type` | `object` |
| `associated_off_ball_run_event_id` | `object` |
| `associated_off_ball_run_subtype_id` | `float64` |
| `associated_off_ball_run_subtype` | `object` |
| `game_state_id` | `int64` |
| `game_state` | `object` |
| `team_score` | `int64` |
| `opponent_team_score` | `int64` |
| `phase_index` | `int64` |
| `player_possession_phase_index` | `float64` |
| `first_player_possession_in_team_possession` | `object` |
| `last_player_possession_in_team_possession` | `object` |
| `lead_to_different_phase` | `object` |
| `issued_from_different_phase` | `object` |
| `n_player_possessions_in_phase` | `float64` |
| `team_possession_loss_in_phase` | `object` |
| `team_in_possession_phase_type_id` | `int64` |
| `team_in_possession_phase_type` | `object` |
| `team_out_of_possession_phase_type_id` | `int64` |
| `team_out_of_possession_phase_type` | `object` |
| `current_team_in_possession_next_phase_type_id` | `float64` |
| `current_team_in_possession_next_phase_type` | `object` |
| `current_team_out_of_possession_next_phase_type_id` | `float64` |
| `current_team_out_of_possession_next_phase_type` | `object` |
| `current_team_in_possession_previous_phase_type_id` | `float64` |
| `current_team_in_possession_previous_phase_type` | `object` |
| `current_team_out_of_possession_previous_phase_type_id` | `float64` |
| `current_team_out_of_possession_previous_phase_type` | `object` |
| `game_interruption_before_id` | `float64` |
| `game_interruption_before` | `object` |
| `game_interruption_after_id` | `float64` |
| `game_interruption_after` | `object` |
| `lead_to_shot` | `bool` |
| `lead_to_goal` | `bool` |
| `distance_covered` | `float64` |
| `trajectory_angle` | `float64` |
| `trajectory_direction_id` | `float64` |
| `trajectory_direction` | `object` |
| `in_to_out` | `object` |
| `out_to_in` | `object` |
| `speed_avg` | `float64` |
| `speed_avg_band_id` | `float64` |
| `speed_avg_band` | `object` |
| `separation_start` | `float64` |
| `separation_end` | `float64` |
| `separation_gain` | `float64` |
| `last_defensive_line_x_start` | `float64` |
| `last_defensive_line_x_end` | `float64` |
| `delta_to_last_defensive_line_start` | `float64` |
| `delta_to_last_defensive_line_end` | `float64` |
| `delta_to_last_defensive_line_gain` | `float64` |
| `last_defensive_line_height_start` | `float64` |
| `last_defensive_line_height_end` | `float64` |
| `last_defensive_line_height_gain` | `float64` |
| `inside_defensive_shape_start` | `object` |
| `inside_defensive_shape_end` | `object` |
| `start_type_id` | `float64` |
| `start_type` | `object` |
| `end_type_id` | `float64` |
| `end_type` | `object` |
| `consecutive_on_ball_engagements` | `object` |
| `one_touch` | `object` |
| `quick_pass` | `object` |
| `carry` | `object` |
| `forward_momentum` | `object` |
| `is_header` | `object` |
| `hand_pass` | `object` |
| `initiate_give_and_go` | `object` |
| `pass_angle_received` | `float64` |
| `pass_direction_received_id` | `float64` |
| `pass_direction_received` | `object` |
| `pass_distance_received` | `float64` |
| `pass_range_received_id` | `float64` |
| `pass_range_received` | `object` |
| `pass_outcome_id` | `float64` |
| `pass_outcome` | `object` |
| `targeted_passing_option_event_id` | `object` |
| `high_pass` | `object` |
| `player_targeted_id` | `float64` |
| `player_targeted_name` | `object` |
| `player_targeted_position_id` | `float64` |
| `player_targeted_position` | `object` |
| `player_targeted_x_pass` | `float64` |
| `player_targeted_y_pass` | `float64` |
| `player_targeted_channel_pass_id` | `float64` |
| `player_targeted_channel_pass` | `object` |
| `player_targeted_third_pass_id` | `float64` |
| `player_targeted_third_pass` | `object` |
| `player_targeted_penalty_area_pass` | `object` |
| `player_targeted_x_reception` | `float64` |
| `player_targeted_y_reception` | `float64` |
| `player_targeted_channel_reception_id` | `float64` |
| `player_targeted_channel_reception` | `object` |
| `player_targeted_third_reception_id` | `float64` |
| `player_targeted_third_reception` | `object` |
| `player_targeted_penalty_area_reception` | `object` |
| `player_targeted_distance_to_goal_start` | `float64` |
| `player_targeted_distance_to_goal_end` | `float64` |
| `player_targeted_angle_to_goal_start` | `float64` |
| `player_targeted_angle_to_goal_end` | `float64` |
| `player_targeted_average_speed` | `float64` |
| `player_targeted_speed_avg_band_id` | `float64` |
| `player_targeted_speed_avg_band` | `object` |
| `speed_difference` | `float64` |
| `player_targeted_xpass_completion` | `float64` |
| `player_targeted_difficult_pass_target` | `object` |
| `player_targeted_xthreat` | `float64` |
| `player_targeted_dangerous` | `object` |
| `n_passing_options` | `float64` |
| `n_off_ball_runs` | `float64` |
| `n_passing_options_line_break` | `float64` |
| `n_passing_options_first_line_break` | `float64` |
| `n_passing_options_second_last_line_break` | `float64` |
| `n_passing_options_last_line_break` | `float64` |
| `n_passing_options_ahead` | `float64` |
| `n_passing_options_dangerous_difficult` | `float64` |
| `n_passing_options_dangerous_not_difficult` | `float64` |
| `n_passing_options_not_dangerous_not_difficult` | `float64` |
| `n_passing_options_not_dangerous_difficult` | `float64` |
| `n_passing_options_at_start` | `float64` |
| `n_passing_options_at_end` | `float64` |
| `n_passing_options_ahead_at_start` | `float64` |
| `n_passing_options_ahead_at_end` | `float64` |
| `n_teammates_ahead_end` | `float64` |
| `n_teammates_ahead_start` | `float64` |
| `n_player_targeted_opponents_ahead_start` | `float64` |
| `n_player_targeted_opponents_ahead_end` | `float64` |
| `n_player_targeted_teammates_ahead_start` | `float64` |
| `n_player_targeted_teammates_ahead_end` | `float64` |
| `n_player_targeted_teammates_within_5m_start` | `float64` |
| `n_player_targeted_teammates_within_5m_end` | `float64` |
| `n_player_targeted_opponents_within_5m_start` | `float64` |
| `n_player_targeted_opponents_within_5m_end` | `float64` |
| `organised_defense` | `object` |
| `defensive_structure` | `float64` |
| `n_defensive_lines` | `float64` |
| `first_line_break` | `object` |
| `first_line_break_type_id` | `float64` |
| `first_line_break_type` | `object` |
| `second_last_line_break` | `object` |
| `second_last_line_break_type_id` | `float64` |
| `second_last_line_break_type` | `object` |
| `last_line_break` | `object` |
| `last_line_break_type_id` | `float64` |
| `last_line_break_type` | `object` |
| `furthest_line_break_id` | `float64` |
| `furthest_line_break` | `object` |
| `furthest_line_break_type_id` | `float64` |
| `furthest_line_break_type` | `object` |
| `interplayer_distance` | `float64` |
| `interplayer_distance_range_id` | `float64` |
| `interplayer_distance_range` | `object` |
| `interplayer_distance_start` | `float64` |
| `interplayer_distance_end` | `float64` |
| `interplayer_distance_min` | `float64` |
| `interplayer_distance_start_physical` | `float64` |
| `close_at_player_possession_start` | `object` |
| `interplayer_angle` | `float64` |
| `interplayer_direction_id` | `float64` |
| `interplayer_direction` | `object` |
| `angle_of_engagement` | `float64` |
| `goal_side_start` | `object` |
| `goal_side_end` | `object` |
| `pass_distance` | `float64` |
| `pass_range_id` | `float64` |
| `pass_range` | `object` |
| `pass_angle` | `float64` |
| `pass_direction_id` | `float64` |
| `pass_direction` | `object` |
| `pass_ahead` | `object` |
| `n_opponents_ahead_player_in_possession_pass_moment` | `float64` |
| `n_opponents_ahead_pass_reception` | `float64` |
| `n_opponents_bypassed` | `float64` |
| `location_to_player_in_possession_id_start` | `float64` |
| `location_to_player_in_possession_start` | `object` |
| `location_to_player_in_possession_id_end` | `float64` |
| `location_to_player_in_possession_end` | `object` |
| `distance_to_player_in_possession_start` | `float64` |
| `distance_to_player_in_possession_end` | `float64` |
| `player_in_possession_x_start` | `float64` |
| `player_in_possession_y_start` | `float64` |
| `player_in_possession_channel_id_start` | `float64` |
| `player_in_possession_channel_start` | `object` |
| `player_in_possession_third_id_start` | `float64` |
| `player_in_possession_third_start` | `object` |
| `player_in_possession_penalty_area_start` | `object` |
| `player_in_possession_x_end` | `float64` |
| `player_in_possession_y_end` | `float64` |
| `player_in_possession_channel_id_end` | `float64` |
| `player_in_possession_channel_end` | `object` |
| `player_in_possession_third_id_end` | `float64` |
| `player_in_possession_third_end` | `object` |
| `player_in_possession_penalty_area_end` | `object` |
| `targeted` | `object` |
| `received` | `object` |
| `received_in_space` | `object` |
| `dangerous` | `object` |
| `difficult_pass_target` | `object` |
| `xthreat` | `float64` |
| `xpass_completion` | `float64` |
| `passing_option_score` | `float64` |
| `predicted_passing_option` | `object` |
| `peak_passing_option_frame` | `float64` |
| `passing_option_at_player_possession_start` | `object` |
| `n_simultaneous_runs` | `float64` |
| `give_and_go` | `object` |
| `intended_run_behind` | `object` |
| `push_defensive_line` | `object` |
| `break_defensive_line` | `object` |
| `passing_option_at_start` | `object` |
| `n_simultaneous_passing_options` | `float64` |
| `passing_option_at_pass_moment` | `object` |
| `n_opponents_ahead_end` | `float64` |
| `n_opponents_ahead_start` | `float64` |
| `n_opponents_overtaken` | `float64` |
| `pressing_chain` | `object` |
| `pressing_chain_length` | `float64` |
| `pressing_chain_end_type_id` | `float64` |
| `pressing_chain_end_type` | `object` |
| `pressing_chain_index` | `float64` |
| `index_in_pressing_chain` | `float64` |
| `simultaneous_defensive_engagement_same_target` | `object` |
| `simultaneous_defensive_engagement_same_target_rank` | `float64` |
| `affected_line_breaking_passing_option_id` | `object` |
| `affected_line_break_id` | `float64` |
| `affected_line_break` | `object` |
| `affected_line_breaking_passing_option_attempted` | `object` |
| `affected_line_breaking_passing_option_xthreat` | `float64` |
| `affected_line_breaking_passing_option_dangerous` | `object` |
| `affected_line_breaking_passing_option_run_subtype_id` | `float64` |
| `affected_line_breaking_passing_option_run_subtype` | `object` |
| `possession_danger` | `object` |
| `beaten_by_possession` | `object` |
| `beaten_by_movement` | `object` |
| `stop_possession_danger` | `object` |
| `reduce_possession_danger` | `object` |
| `force_backward` | `object` |
| `xloss_player_possession_start` | `float64` |
| `xloss_player_possession_end` | `float64` |
| `xloss_player_possession_max` | `float64` |
| `xshot_player_possession_start` | `float64` |
| `xshot_player_possession_end` | `float64` |
| `xshot_player_possession_max` | `float64` |
| `is_player_possession_start_matched` | `bool` |
| `is_player_possession_end_matched` | `bool` |
| `is_previous_pass_matched` | `object` |
| `is_pass_reception_matched` | `object` |
| `fully_extrapolated` | `object` |

### Schema de `<match_id>_phases_of_play.csv` (Fases do Jogo)
Segmentação tática da partida por fases de ataque, defesa e transições com marcação temporal.
| Coluna | Tipo de Dado |
| :--- | :--- |
| `index` | `int64` |
| `match_id` | `int64` |
| `frame_start` | `int64` |
| `frame_end` | `int64` |
| `time_start` | `object` |
| `time_end` | `object` |
| `minute_start` | `int64` |
| `second_start` | `int64` |
| `duration` | `float64` |
| `period` | `int64` |
| `attacking_side_id` | `int64` |
| `team_in_possession_id` | `int64` |
| `attacking_side` | `object` |
| `team_in_possession_shortname` | `object` |
| `n_player_possessions_in_phase` | `int64` |
| `team_possession_loss_in_phase` | `bool` |
| `team_possession_lead_to_goal` | `bool` |
| `team_possession_lead_to_shot` | `bool` |
| `team_in_possession_phase_type` | `object` |
| `team_in_possession_phase_type_id` | `int64` |
| `team_out_of_possession_phase_type` | `object` |
| `team_out_of_possession_phase_type_id` | `int64` |
| `x_start` | `float64` |
| `y_start` | `float64` |
| `channel_id_start` | `int64` |
| `channel_start` | `object` |
| `third_id_start` | `int64` |
| `third_start` | `object` |
| `penalty_area_start` | `bool` |
| `x_end` | `float64` |
| `y_end` | `float64` |
| `channel_id_end` | `int64` |
| `channel_end` | `object` |
| `third_id_end` | `int64` |
| `third_end` | `object` |
| `penalty_area_end` | `bool` |
| `team_in_possession_width_start` | `float64` |
| `team_in_possession_width_end` | `float64` |
| `team_in_possession_length_start` | `float64` |
| `team_in_possession_length_end` | `float64` |
| `team_out_of_possession_width_start` | `float64` |
| `team_out_of_possession_width_end` | `float64` |
| `team_out_of_possession_length_start` | `float64` |
| `team_out_of_possession_length_end` | `float64` |

## 4. Mapeamento de Chaves Primárias (PK) e Estrangeiras (FK)

As entidades do modelo de dados da SkillCorner estão conectadas através das seguintes chaves relacionais:

| Entidade | Chave Primária (PK) | Chaves Estrangeiras (FK) | Descrição do Relacionamento |
| :--- | :--- | :--- | :--- |
| **Partida (`Match`)** | `match_id` (ou `id`) | `competition_id`, `season_id` | Identifica univocamente uma partida em `matches.json` e no nome das pastas/arquivos de cada jogo. |
| **Jogador (`Player`)** | `player_id` (ou `id`) | `team_id` | Identifica cada atleta em `<match_id>_match.json`, `dynamic_events.csv` e arquivos de agregados físicas/passes. |
| **Equipe (`Team`)** | `team_id` (ou `id`) | - | Conecta partidas, jogadores, eventos dinâmicos e métricas agregadas por clube. |
| **Evento Dinâmico (`DynamicEvent`)** | `event_id` / `frame_start` | `match_id`, `player_id`, `team_id` | Liga eventos específicos no tempo às entidades de atleta, time e partida. |
| **Fase de Jogo (`PhaseOfPlay`)** | `phase_id` / `start_time` | `match_id`, `team_id` | Mapeia trechos temporais da partida para os times em posse/defesa. |

## 5. Próximos Passos Recomendados

1. **Validação do Schema (Fase 2):** Criar modelos Pydantic na camada `src/domain/entities/` para refletir as entidades `Match`, `Player`, `DynamicEvent` e `PhaseOfPlay` com tipagem forte.
2. **Engenharia de Features:** Desenvolver parsers de Polars para carregar e processar os eventos dinâmicos de forma performática.
3. **Pipeline de Agregação:** Construir conectores na camada `src/use_cases/` para consolidar métricas físicas e táticas por jogador e por equipe.
