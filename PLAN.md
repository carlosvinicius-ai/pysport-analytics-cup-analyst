# Plano de Execução Incremental — SkillCorner Sports Analytics (`PLAN.md`)

Este plano detalha o roteiro incremental de desenvolvimento do projeto, dividido em 4 Marcos (Milestones) atômicos. Cada tarefa indica a camada da **Clean Architecture** a ser modificada e o teste associado.

---

## 🎯 Prioridades do Projeto
- **FOCO PRINCIPAL (Fase 1):** Modelo de Probabilidade de Passe (`xPass`) e Valor do Desmarque sem Bola (*Off-Ball Run Value*) — Spatial Analytics & Deep Learning.
- **FOCO SECUNDÁRIO (Fase 2):** Profiling Físico-Tático e Agrupamento de Atletas por K-Means/GMM — ML Clássico.

---

## 📌 MARCO 1: Engenharia de Dados Espaciais & Domínio (Clean Architecture)

- [x] **Tarefa 1.1: Entidades Puras de Domínio (`src/domain/entities/player.py`, `match.py`)**
  - **Camada:** `Domain / Entities`
  - **Descrição:** Criar dataclasses puras `Player`, `Team`, `PitchDimensions` e `Match` sem dependências I/O ou de frameworks.
  - **Verificação:** Testes unitários em `tests/unit/domain/test_entities.py`.


- [ ] **Tarefa 1.2: Entidades de Eventos Espaciais e Frames (`src/domain/entities/event.py`, `frame.py`)**
  - **Camada:** `Domain / Entities`
  - **Descrição:** Criar dataclasses `PassEvent`, `OffBallRunEvent` e `TrackingFrame` representando coordenadas ($x, y$), timestamp, pressão, separação espacial e contexto da linha defensiva.
  - **Verificação:** Testes unitários em `tests/unit/domain/test_events.py`.

- [ ] **Tarefa 1.3: Protocolos e Interfaces de Repositório (`src/domain/protocols/repository.py`)**
  - **Camada:** `Domain / Protocols`
  - **Descrição:** Definir `typing.Protocol` para `IDatasetRepository` e `ITrackingParser`, desacoplando a infraestrutura do domínio.
  - **Verificação:** Teste de conformidade de tipo (`mypy` / `pytest`).

- [ ] **Tarefa 1.4: Parser Concreto de Metadados e Elencos (`src/infrastructure/parsers/match_parser.py`)**
  - **Camada:** `Infrastructure / Parsers`
  - **Descrição:** Criar leitor robusto de `matches.json` e `<match_id>_match.json` para carregar partidas e escalações de jogadores.
  - **Verificação:** Teste de integração em `tests/integration/infrastructure/test_match_parser.py`.

- [ ] **Tarefa 1.5: Parser Concreto de Eventos Dinâmicos (`src/infrastructure/parsers/tracking_parser.py`)**
  - **Camada:** `Infrastructure / Parsers`
  - **Descrição:** Criar parser em Polars/Pandas para `<match_id>_dynamic_events.csv` extraindo eventos de passe e corridas sem bola com tipagem adequada.
  - **Verificação:** Teste de integração em `tests/integration/infrastructure/test_tracking_parser.py`.

- [ ] **Tarefa 1.6: Use Case de Extração de Features Espaciais (`src/use_cases/feature_extraction/spatial_features.py`)**
  - **Camada:** `Use Cases / Application`
  - **Descrição:** Criar `ComputeSpatialFeaturesUseCase` para calcular:
    - Distância para a linha defensiva (`last_defensive_line_x_start`, `delta_to_last_defensive_line_start`)
    - Pressão defensiva e distância de inter-jogadores (`interplayer_distance_start`, `angle_of_engagement`)
    - Separação espacial (`separation_start`, `separation_gain`)
    - Ângulo e distância do passe (`pass_angle`, `pass_distance`)
  - **Verificação:** Teste unitário em `tests/unit/use_cases/test_spatial_features.py`.

---

## 📌 MARCO 2: Modelo Baseline de xPass (MVP)

- [ ] **Tarefa 2.1: Pipeline de Validação Temporal por Partida (`tests/unit/use_cases/test_validation_split.py`)**
  - **Camada:** `Use Cases & Tests`
  - **Descrição:** Implementar gerador de split de partidas (*Match-Based Chronological Split*) separando treino (70%), validação (15%) e teste (15%) com garantia de **zero data leakage**.
  - **Verificação:** Teste unitário confirmando ausência de sobreposição de `match_id` entre splits.

- [ ] **Tarefa 2.2: Adaptador do Modelo Baseline XGBoost (`src/infrastructure/ml_adapters/xpass_baseline.py`)**
  - **Camada:** `Infrastructure / ML Adapters`
  - **Descrição:** Implementar `XGBoostXPassAdapter` encapsulando pré-processador e modelo supervisionado de classificação de probabilidade de passe.
  - **Verificação:** Teste unitário do adaptador em `tests/unit/infrastructure/test_xpass_baseline.py`.

- [ ] **Tarefa 2.3: Use Case de Treinamento e Avaliação do Baseline (`src/use_cases/modeling/train_xpass_baseline.py`)**
  - **Camada:** `Use Cases / Application`
  - **Descrição:** Criar `TrainXPassBaselineUseCase` orquestrando extração de atributos espaciais, treino, cálculo de Log-Loss, ROC-AUC, Brier Score e salvamento dos artefatos do modelo em `reports/`.
  - **Verificação:** Teste de ponta a ponta gerando métricas do baseline em `reports/XPASS_BASELINE_METRICS.md`.

---

## 📌 MARCO 3: Modelo Avançado de Spatial Analytics & Deep Learning (xPass & Off-Ball Value)

- [ ] **Tarefa 3.1: Modelo Profundo / Avançado de Probabilidade de Passe (`src/infrastructure/ml_adapters/xpass_deep.py`)**
  - **Camada:** `Infrastructure / ML Adapters`
  - **Descrição:** Construir arquitetura de Rede Neural Profunda (PyTorch / Multi-Layer Perceptron) incorporando embedding posicional e vetores de pressão espacial.
  - **Verificação:** Teste unitário de forward-pass e loss computation em `tests/unit/infrastructure/test_xpass_deep.py`.

- [ ] **Tarefa 3.2: Use Case de Cálculo do Valor de Desmarque sem Bola (`src/use_cases/modeling/off_ball_value.py`)**
  - **Camada:** `Use Cases / Application`
  - **Descrição:** Implementar `ComputeOffBallRunValueUseCase` estimando a ameaça gerada por corridas sem bola ($\text{Off-Ball Value} = \text{separation\_gain} \times \Delta\text{xThreat}$).
  - **Verificação:** Teste unitário em `tests/unit/use_cases/test_off_ball_value.py`.

- [ ] **Tarefa 3.3: Gerador de Visualizações e Mapas Espaciais (`src/presentation/spatial_visualizer.py`)**
  - **Camada:** `Interfaces / Presentation`
  - **Descrição:** Criar módulo de visualização espacial para mapas térmicos de controle de espaço (*Pitch Control*) e gráficos de valor de movimentação sem bola por jogador.
  - **Verificação:** Gerar imagens de mapa térmico em `reports/figures/`.

---

## 📌 MARCO 4: Profiling Físico-Tático (Caso de Uso 2 - Foco Secundário)

- [ ] **Tarefa 4.1: Pipeline de Agregação Físico-Tática (`src/use_cases/feature_extraction/physical_features.py`)**
  - **Camada:** `Use Cases / Application`
  - **Descrição:** Criar `ComputePhysicalAggregatesUseCase` consolidando distâncias em sprints, corridas de alta intensidade, velocidade média e volume de desmarques por atleta.
  - **Verificação:** Teste unitário em `tests/unit/use_cases/test_physical_features.py`.

- [ ] **Tarefa 4.2: Adaptador de Clusterização K-Means / GMM (`src/infrastructure/ml_adapters/clustering.py`)**
  - **Camada:** `Infrastructure / ML Adapters`
  - **Descrição:** Implementar `SklearnClusterAdapter` com redução de dimensionalidade PCA e ajuste de clusters K-Means/GMM.
  - **Verificação:** Teste unitário avaliando Silhouette Score e Davies-Bouldin Index.

- [ ] **Tarefa 4.3: Use Case e Apresentação do Profiling de Atletas (`src/use_cases/modeling/cluster_players.py`)**
  - **Camada:** `Use Cases & Presentation`
  - **Descrição:** Orquestrar o treinamento do clusterizador e criar exportador de matriz de similaridade e gráficos de radar dos perfis dos jogadores.
  - **Verificação:** Gerar relatório final de profiling em `reports/PLAYER_PROFILING.md`.
