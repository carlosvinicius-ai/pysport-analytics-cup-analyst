# Especificação Técnica e Arquitetural — SkillCorner Sports Analytics

## Visão Geral do Projeto
O objetivo deste projeto é construir uma plataforma modular de **Data Science & Sports Analytics** utilizando dados de tracking e métricas físicas/táticas da **SkillCorner Open Data**. A plataforma adota rigorosamente a **Clean Architecture** e os princípios **SOLID**, permitindo que treinadores, analistas e comissões técnicas extraiam insights sobre a performance física, espacial e tática de atletas e equipes.

---

## 1. Objetivos e Casos de Uso de Data Science

### Caso de Uso 1 (Machine Learning Clássico): Profiling Físico-Tático e Agrupamento de Atletas
- **Objetivo:** Identificar perfis funcionais e padrões de intensidade física de atletas (ex: *High-Volume Engine*, *Explosive Sprinter*, *Defensive Line-Breaker*) além da posição nominal de escalação.
- **Mapeamento de Colunas (`DATA_STRUCTURE.md`):**
  - **Métricas Físicas e Distâncias:** `distance_covered`, `speed_avg`, `speed_avg_band`, `speed_difference`.
  - **Métricas de Intensidade e Ações sem Bola:** `n_off_ball_runs`, `n_passing_options`, `n_passing_options_line_break`, `n_simultaneous_runs`.
  - **Métricas da Aus1League Physical Aggregates:** Distâncias acumuladas por zonas de velocidade (Caminhada, Corrida Leve, Alta Intensidade, Sprints).
- **Abordagem Algorítmica:**
  - Redução de dimensionalidade com **PCA** ou **UMAP** para projeção do espaço físico-tático.
  - Algoritmos de agrupamento não-supervisionado: **K-Means**, **Gaussian Mixture Models (GMM)** ou **HDBSCAN**.
- **Entrega Analítica:** Matriz de Similaridade de Jogadores (procura por substitutos com perfil físico equivalente) e Perfis Rader/Spider charts para comissão técnica.

---

### Caso de Uso 2 (Deep Learning / Spatial Analytics): Probabilidade de Passe (`xPass`) e Valor do Desmarque sem Bola (*Off-Ball Run Value*)
- **Objetivo:** Quantificar a qualidade dos desmarques sem bola e a probabilidade de sucesso de passes em janelas sob pressão defensiva.
- **Mapeamento de Colunas (`DATA_STRUCTURE.md`):**
  - **Coordenadas e Separação Espacial:** `x_start`, `y_start`, `x_end`, `y_end`, `separation_start`, `separation_end`, `separation_gain`.
  - **Contexto da Linha Defensiva:** `last_defensive_line_x_start`, `delta_to_last_defensive_line_start`, `inside_defensive_shape_start`.
  - **Pressão e Interplay:** `interplayer_distance`, `interplayer_distance_start`, `interplayer_angle`, `angle_of_engagement`.
  - **Métricas Avançadas Existentes no Dataset:** `xpass_completion`, `xthreat`, `passing_option_score`, `first_line_break`, `last_line_break`.
- **Abordagem Algorítmica:**
  - **Modelagem xPass:** Classificador baseado em **XGBoost / LightGBM** ou **Multi-Layer Perceptron (MLP)** para estimar $P(\text{pass\_outcome} = \text{completed} \mid \text{Spatial Features})$.
  - **Modelagem de Valor sem Bola:** Redes Neurais Profundas ou **Graph Neural Networks (GNN)** para avaliar o ganho de ameaça provocada por corridas sem bola (`separation_gain` $\times$ $\Delta\text{xThreat}$).
- **Entrega Analítica:** Mapa térmico de controle de espaço (*Pitch Control*) e ranking de atletas que criam mais valor através do posicionamento e desmarque.

---

### Caso de Uso 3 (NLP / LLMs): Agente de Inteligência Tática para Geração de Informes Pós-Jogo
- **Objetivo:** Converter os dados numéricos brutos da partida (metadados, eventos dinâmicos e métricas físicas) em relatórios táticos estruturados em linguagem natural para o treinador.
- **Mapeamento de Colunas (`DATA_STRUCTURE.md`):**
  - **Metadados do Jogo (`matches.json`, `_match.json`):** `home_team`, `away_team`, placar, escalações, tempo de posse de bola (`minutes_tip`, `minutes_otip`).
  - **Fases do Jogo (`_phases_of_play.csv`):** `team_in_possession_phase_type`, `n_player_possessions_in_phase`, `team_possession_lead_to_shot`, `team_possession_lead_to_goal`.
  - **Eventos Notáveis (`_dynamic_events.csv`):** `lead_to_shot`, `lead_to_goal`, `first_line_break`, `pressing_chain_length`.
- **Abordagem Algorítmica:**
  - **Pipeline Data-to-Text:** Agregação de estatísticas chave da partida em um objeto de contexto JSON/Prompt Estruturado.
  - **Arquitetura LLM:** Utilização de Modelos de Linguagem (ex: LLMs via API ou Ollama/Local) orientados por **Prompt Engineering Avançado** (Few-Shot Prompting, Chain-of-Thought) e validação de consistência sintática via **Pydantic Output Parsers**.
- **Entrega Analítica:** Relatório Narrativo da Partida ("Sumário Executivo para o Técnico"), cobrindo momentos críticos de pressão, transições defensivas/ofensivas e destaques individuais.

---

## 2. Arquitetura do Sistema (Clean Architecture)

A estrutura do código fonte em `src/` obedece a separação estrita de responsabilidades:

```
src/
├── domain/                  # Camada de Domínio (Entidades e Contratos Puros)
│   ├── entities/            # Dataclasses / Modelos Pydantic v2 sem dependências I/O
│   │   ├── player.py        # Entidade Player, PlayerProfile
│   │   ├── match.py         # Entidade Match, Team, PitchDimensions
│   │   ├── event.py         # Entidade DynamicEvent, OffBallRun
│   │   ├── phase.py         # Entidade PhaseOfPlay
│   │   └── metrics.py       # Dataclass PhysicalMetrics, SpatialMetrics
│   └── protocols/           # Interfaces e Protocolos abstratos (typing.Protocol)
│       ├── repository.py    # Protocol IDatasetRepository
│       ├── model.py         # Protocol ITacticalModel, IXPassPredictor
│       └── reporter.py      # Protocol ITacticalReporter
│
├── use_cases/               # Camada de Casos de Uso (Orquestração das Regras de Negócio)
│   ├── feature_extraction/  # Extração e engenharia de atributos
│   │   ├── physical_features.py  # ComputePhysicalAggregatesUseCase
│   │   └── spatial_features.py   # ComputeSpatialFeaturesUseCase
│   ├── modeling/            # Fluxos de Treinamento e Predição
│   │   ├── cluster_players.py    # ClusterPlayerProfilesUseCase
│   │   └── train_xpass.py        # TrainXPassModelUseCase
│   └── reporting/           # Orquestração de Geração de Relatórios
│       └── generate_report.py    # GenerateTacticalReportUseCase
│
├── infrastructure/          # Camada de Infraestrutura (I/O, Bibliotecas Externas, Parsers)
│   ├── parsers/             # Leitores de JSON e CSV da SkillCorner
│   │   ├── discovery.py     # Script de descoberta de dados
│   │   ├── json_parser.py   # SkillCornerJSONParser (Pandas/Polars)
│   │   └── csv_parser.py    # SkillCornerCSVParser (Polars for high-speed I/O)
│   ├── ml_adapters/         # Adaptadores Scikit-Learn, XGBoost, PyTorch
│   │   ├── clustering.py    # SklearnClusterAdapter
│   │   └── xpass.py         # XGBoostXPassAdapter
│   └── llm_adapters/        # Adaptador para LLM / Prompt Engine
│       └── prompt_engine.py # LLMTacticalReportAdapter
│
└── presentation/            # Camada de Apresentação e CLI
    ├── cli.py               # Interface de Linha de Comando (Click / Argparse)
    └── report_generator.py # Gerador de Saídas em Markdown/HTML
```

---

## 3. Plano de Validação e Métricas Estatísticas

### 3.1. Métricas de Avaliação por Caso de Uso

1. **Caso de Uso 1 (ML Clássico - Clusterização):**
   - **Silhouette Score:** Mede o quão bem separado cada cluster está em relação aos clusters vizinhos (alvo $> 0.45$).
   - **Davies-Bouldin Index:** Avalia a dispersão interna dos clusters comparada à distância entre eles (quanto menor, melhor).
   - **Calinski-Harabasz Index:** Razão entre a dispersão inter-cluster e intra-cluster.
   - **Estabilidade do Cluster:** Re-execução com Bootstrap/Sub-amostragem para medir o Índice Rand Ajustado (ARI).

2. **Caso de Uso 2 (Spatial Analytics - Modelo xPass / Off-Ball Value):**
   - **Log-Loss (Cross-Entropy Loss):** Métrica primária para calibração de probabilidades preditas de passes completos vs incompletos.
   - **ROC-AUC & PR-AUC:** Área sob a curva ROC e Precisão-Recall para lidar com desbalanceamento de passes de alto risco.
   - **Brier Score:** Avalia o erro quadrático médio das probabilidades preditas ($BS = \frac{1}{N}\sum (p_i - y_i)^2$).
   - **Expected Calibration Error (ECE):** Mede o alinhamento das probabilidades preditas com a frequência real de acerto em decibéis de confiança.

3. **Caso de Uso 3 (NLP / LLMs - Relatórios Táticos):**
   - **Consistência Factual (Factuality Check):** Verificação automatizada se os números/placar/estatísticas citadas no texto correspondem exatamente aos dados do JSON da partida.
   - **ROUGE-L & BLEU (Opcional):** Avaliação de alinhamento com relatórios de referência caso disponíveis.
   - **LLM-as-a-Judge:** Avaliação com critério cego avaliando **Relevância Tática**, **Clareza para Treinadores** e **Ausência de Alucinações** (Escala 1 a 5).

---

### 3.2. Estratégia de Validação Temporal e Prevenção de Data Leakage

Para garantir a integridade científica e evitar o vazamento de informações entre treino e teste (*Data Leakage*):

1. **Divisão Baseada em Partida (*Match-Based Split*):**
   - **Regra Rígida:** NUNCA misturar eventos ou frames da mesma partida entre conjuntos de Treino, Validação e Teste.
   - As partidas serão divididas na proporção **70% Treino (7 jogos), 15% Validação (1.5 jogos), 15% Teste (1.5 jogos)** ou por ordenação cronológica de realização do jogo.

2. **Isolamento de Pré-processamento (*Strict Scaler Pipeline*):**
   - Todos os pré-processamentos (imputação de nulos, padronização `StandardScaler`, redução `PCA`) serão ajustados (*fit*) **exclusivamente nos dados de treino**.
   - Apenas a transformação (*transform*) será aplicada nos conjuntos de validação e teste.

3. **Independência de Atletas nas Métricas de Clusterização:**
   - A clusterização será avaliada tanto no nível global quanto no nível intra-posicional, garantindo que jogadas de uma única partida não distorçam o perfil de longo prazo do atleta.

---

## 4. Resumo de Entregáveis da Especificação

1. Documento `SPEC.md` aprovado na raiz do repositório.
2. Arquitetura em camadas sob Clean Architecture validada com `AGENTS.md`.
3. Pronto para o início da execução da Fase 2 (Desenvolvimento de Entidades de Domínio e Parsers).
