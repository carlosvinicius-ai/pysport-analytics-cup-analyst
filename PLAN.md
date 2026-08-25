# PLAN.md - Plano de Execução Incremental

Este plano orienta o desenvolvimento passo a passo da plataforma de **Sports Analytics & SkillCorner Modeling**, estruturado sob a **Clean Architecture** e dividido em Marcos (Milestones) incrementais.

---

## 📌 MARCO 1: Engenharia de Dados Espaciais & Domínio (Clean Architecture)

- [x] **Governança de ADRs: Criação da estrutura `docs/adr/` e template (`docs/adr/0000-template.md`)**
  - **Camada:** `Documentação / Governança`
  - **Descrição:** Estruturar pasta e template padrão para Architecture Decision Records (ADRs).

- [x] **Governança de ADRs: Registro da ADR 0001 (`docs/adr/0001-adocao-clean-architecture-e-polars.md`)**
  - **Camada:** `Documentação / Governança`
  - **Descrição:** Documentar a decisão da Clean Architecture em 4 camadas e uso do Polars para processamento de alto desempenho.

- [x] **Governança de ADRs: Registro da ADR 0002 (`docs/adr/0002-representacao-entidades-espaciais-e-coordenadas.md`)**
  - **Camada:** `Documentação / Governança`
  - **Descrição:** Documentar representação em metros reais, imutabilidade com `frozen=True` e completude de atributos espaciais.

- [x] **Governança de ADRs: Registro da ADR 0003 (`docs/adr/0003-protocolos-e-interfaces-de-repositorio.md`)**
  - **Camada:** `Documentação / Governança`
  - **Descrição:** Documentar a definição de protocolos abstratos para Inversão de Dependência (DIP) e Segregação de Interfaces (ISP).

- [x] **Tarefa 1.1: Entidades Puras de Domínio (`src/domain/entities/player.py`, `match.py`)**
  - **Camada:** `Domain / Entities`
  - **Descrição:** Criar dataclasses puras `Player`, `Team`, `PitchDimensions` e `Match` sem dependências I/O ou de frameworks.
  - **Verificação:** Testes unitários em `tests/unit/domain/test_entities.py`.

- [x] **Tarefa 1.2: Entidades de Eventos Espaciais e Frames (`src/domain/entities/event.py`, `frame.py`)**
  - **Camada:** `Domain / Entities`
  - **Descrição:** Criar dataclasses `PassEvent`, `OffBallRunEvent` e `TrackingFrame` representando coordenadas ($x, y$), timestamp, pressão, separação espacial e contexto da linha defensiva.
  - **Verificação:** Testes unitários em `tests/unit/domain/test_events.py`.

- [x] **Tarefa 1.3: Protocolos e Interfaces de Repositório (`src/domain/protocols/repository.py`)**
  - **Camada:** `Domain / Protocols`
  - **Descrição:** Definir `typing.Protocol` para `IDatasetRepository`, `IMatchRepository`, `IEventRepository` e `ITrackingRepository`, desacoplando a infraestrutura do domínio.
  - **Verificação:** Testes unitários de conformidade em `tests/unit/domain/test_protocols.py`.

- [x] **Tarefa 1.4: Parser Concreto de Metadados e Elencos (`src/infrastructure/parsers/match_parser.py`)**
  - **Camada:** `Infrastructure / Parsers`
  - **Descrição:** Criar leitor robusto de `matches.json` e `<match_id>_match.json` para carregar partidas e escalações de jogadores.
  - **Verificação:** Teste de integração em `tests/integration/infrastructure/test_match_parser.py`.

- [x] **Tarefa 1.5: Parser Concreto de Eventos Dinâmicos (`src/infrastructure/parsers/tracking_parser.py`)**
  - **Camada:** `Infrastructure / Parsers`
  - **Descrição:** Criar parser em Polars para `<match_id>_dynamic_events.csv` extraindo eventos de passe e corridas sem bola com tipagem adequada.
  - **Verificação:** Teste de integração em `tests/integration/infrastructure/test_tracking_parser.py`.

- [x] **Tarefa 1.6: Use Case de Extração de Features Espaciais (`src/use_cases/feature_extraction/spatial_features.py`)**
  - **Camada:** `Use Cases / Application`
  - **Descrição:** Criar `ComputeSpatialFeaturesUseCase` para calcular:
    - Distância para a linha defensiva (`last_defensive_line_x_start`, `delta_to_last_defensive_line_start`)
    - Pressão defensiva e distância de inter-jogadores (`interplayer_distance_start`, `angle_of_engagement`)
    - Separação espacial (`separation_start`, `separation_gain`)
    - Ângulo e distância do passe (`pass_angle`, `pass_distance`)
    - Métricas derivadas de ganho territorial (`progression_x`, `lateral_displacement`) e distâncias/ângulos ao gol
  - **Verificação:** Testes unitários em `tests/unit/use_cases/test_spatial_features.py`.

- [x] **Tarefa 1.7: Exploração Visual e Relatório Gráfico do Dataset (`notebooks/exploration.ipynb`)**
  - **Camada:** `Presentation / Notebooks`
  - **Descrição:** Estruturar notebook de EDA visual integrando todas as camadas da Clean Architecture com mapas de passes no gramado (`mplsoccer`), mapa individual por jogador, densidades KDE de ações, análise de pressão defensiva e dinâmicas de corridas de desmarque sem bola com descobertas detalhadas por tópico.
  - **Verificação:** Execução do Jupyter Notebook em `notebooks/exploration.ipynb`.

---

## 📌 MARCO 2: Modelo Baseline de xPass (MVP)

- [ ] **Governança de ADRs: Registro da ADR 0004 (`docs/adr/0004-estrategia-de-split-temporal-e-metricas-xpass.md`)**
  - **Camada:** `Documentação / Governança`
  - **Descrição:** Documentar a divisão cronológica de partidas (70% treino, 10% validação, 20% teste) para garantia de zero data leakage e métricas de calibração (Log-Loss, Brier Score, ROC-AUC, ECE).

- [ ] **Tarefa 2.1: Protocolo de Modelo e Pipeline de Validação Temporal (`src/domain/protocols/model.py`, `src/use_cases/modeling/validation_split.py`)**
  - **Camada:** `Domain / Protocols` & `Use Cases / Modeling`
  - **Descrição:** 
    - Definir `IXPassModel` em `src/domain/protocols/model.py`.
    - Implementar `MatchChronologicalSplitter` separando partidas por data/tempo cronológico sem sobreposição de `match_id` entre splits.
  - **Verificação:** Testes unitários em `tests/unit/use_cases/test_validation_split.py`.

- [ ] **Governança de ADRs: Registro da ADR 0005 (`docs/adr/0005-escolha-do-algoritmo-baseline-xgboost.md`)**
  - **Camada:** `Documentação / Governança`
  - **Descrição:** Documentar a escolha do XGBoost/LightGBM com Calibração Isotônica como baseline de referência para dados tabulares espaciais.

- [ ] **Tarefa 2.2: Adaptador do Modelo Baseline XGBoost/LightGBM (`src/infrastructure/ml_adapters/xpass_baseline.py`)**
  - **Camada:** `Infrastructure / ML Adapters`
  - **Descrição:** Implementar `XGBoostXPassAdapter` respeitando o contrato `IXPassModel`, contendo pipeline com `StandardScaler` isolado, treinamento, calibração e predição de probabilidades $P(\text{completed})$.
  - **Verificação:** Testes unitários do adaptador em `tests/unit/infrastructure/test_xpass_baseline.py`.

- [ ] **Tarefa 2.3: Use Case de Treinamento e Avaliação do Baseline (`src/use_cases/modeling/train_xpass_baseline.py`)**
  - **Camada:** `Use Cases / Application`
  - **Descrição:** Criar `TrainXPassBaselineUseCase` orquestrando: ingestão das 10 partidas via Polars, extração de features, divisão temporal, treino, avaliação com Log-Loss, Brier Score, ROC-AUC, ECE e persistência do modelo serializado.
  - **Verificação:** Teste de ponta a ponta gerando métricas do baseline em `reports/XPASS_BASELINE_METRICS.md`.

- [ ] **Tarefa 2.4: Interpretabilidade (SHAP Values) e Avaliação de Mérito ($x\text{Pass Added}$) (`src/use_cases/modeling/evaluate_xpass.py`)**
  - **Camada:** `Use Cases & Presentation`
  - **Descrição:** Calcular SHAP feature importance das variáveis espaciais e ranquear os jogadores da liga pelo $x\text{Pass Added}$ ($xPA = \sum_{\text{comp}} (1 - xPass) - \sum_{\text{incomp}} xPass$).
  - **Verificação:** Relatório em `reports/XPASS_PLAYER_RANKING.md`.

---

## 📌 MARCO 3: Modelo Avançado de Spatial Analytics & Deep Learning (xPass & Off-Ball Value)

- [ ] **Governança de ADRs: Registro da ADR 0006 (`docs/adr/0006-arquitetura-neural-deep-xpass-e-off-ball.md`)**
  - **Camada:** `Documentação / Governança`
  - **Descrição:** Documentar a arquitetura de Rede Neural Profunda (PyTorch) e modelagem de ganho de ameaça por movimentação sem bola.

- [ ] **Tarefa 3.1: Modelo Profundo / Avançado de Probabilidade de Passe (`src/infrastructure/ml_adapters/xpass_deep.py`)**
  - **Camada:** `Infrastructure / ML Adapters`
  - **Descrição:** Construir arquitetura de Rede Neural Profunda (PyTorch MLP com *Residual Connections* e *Cross-Feature Embeddings*) implementando `IXPassModel`.
  - **Verificação:** Teste unitário de forward-pass e loss em `tests/unit/infrastructure/test_xpass_deep.py`.

- [ ] **Tarefa 3.2: Use Case de Cálculo do Valor de Desmarque sem Bola (`src/use_cases/modeling/off_ball_value.py`)**
  - **Camada:** `Use Cases / Application`
  - **Descrição:** Implementar `ComputeOffBallRunValueUseCase` estimando o valor criado por corridas sem bola ($\text{Off-Ball Value} = \text{separation\_gain} \times \Delta\text{xThreat}$).
  - **Verificação:** Testes unitários em `tests/unit/use_cases/test_off_ball_value.py`.

- [ ] **Tarefa 3.3: Gerador de Visualizações e Mapas Espaciais (`src/presentation/spatial_visualizer.py`)**
  - **Camada:** `Interfaces / Presentation`
  - **Descrição:** Criar módulo de visualização espacial para mapas térmicos de controle de espaço (*Pitch Control*) e gráficos de valor de movimentação sem bola por atleta.
  - **Verificação:** Gerar imagens de mapa térmico em `reports/figures/`.

---

## 📌 MARCO 4: Profiling Físico-Tático (Caso de Uso 2 - Foco Secundário)

- [ ] **Governança de ADRs: Registro da ADR 0007 (`docs/adr/0007-clusterizacao-e-metricas-fisico-taticas.md`)**
  - **Camada:** `Documentação / Governança`
  - **Descrição:** Documentar a metodologia de agrupamento K-Means/GMM, redução de dimensionalidade PCA e seleção de features das tabelas agregadas de temporada.

- [ ] **Tarefa 4.1: Pipeline de Agregação Físico-Tática (`src/use_cases/feature_extraction/physical_features.py`)**
  - **Camada:** `Use Cases / Application`
  - **Descrição:** Criar `ComputePhysicalAggregatesUseCase` integrando dados das tabelas de temporada (`aus1league_physicalaggregates_20242025.csv` e `aus1league_passingaggregates_20242025.csv`) consolidando distâncias em alta intensidade, sprints, velocidade média e volume de desmarques por atleta.
  - **Verificação:** Testes unitários em `tests/unit/use_cases/test_physical_features.py`.

- [ ] **Tarefa 4.2: Adaptador de Clusterização K-Means / GMM (`src/infrastructure/ml_adapters/clustering.py`)**
  - **Camada:** `Infrastructure / ML Adapters`
  - **Descrição:** Implementar `SklearnClusterAdapter` com redução de dimensionalidade PCA e ajuste de clusters K-Means/GMM.
  - **Verificação:** Teste unitário avaliando Silhouette Score e Davies-Bouldin Index.

- [ ] **Tarefa 4.3: Use Case e Apresentação do Profiling de Atletas (`src/use_cases/modeling/cluster_players.py`)**
  - **Camada:** `Use Cases & Presentation`
  - **Descrição:** Orquestrar o treinamento do clusterizador e criar exportador de matriz de similaridade e gráficos de radar dos perfis dos jogadores.
  - **Verificação:** Gerar relatório final de profiling em `reports/PLAYER_PROFILING.md`.
