# Especificação Técnica e Arquitetural — SkillCorner Sports Analytics

## Visão Geral do Projeto
O objetivo deste projeto é construir uma plataforma modular de **Data Science & Sports Analytics** focada 100% na modelagem matemática, estatística e espacial utilizando dados de tracking e métricas físicas/táticas da **SkillCorner Open Data**. A plataforma adota rigorosamente a **Clean Architecture** e os princípios **SOLID**, permitindo extrair métricas avançadas de controle espacial, probabilidade de passe e perfilamento tático de atletas.

---

## 1. Objetivos e Casos de Uso de Data Science

### FOCO PRINCIPAL (Fase 1): Spatial Analytics & Deep Learning — Probabilidade de Passe (`xPass`) e Valor do Desmarque sem Bola (*Off-Ball Run Value*)
- **Objetivo:** Quantificar o risco e a recompensa de cada tentativa de passe em janelas sob pressão defensiva e avaliar o valor criado pelos atletas através de movimentações e desmarques sem a posse da bola.
- **Mapeamento de Colunas (`DATA_STRUCTURE.md`):**
  - **Coordenadas e Separação Espacial:** `x_start`, `y_start`, `x_end`, `y_end`, `separation_start`, `separation_end`, `separation_gain`.
  - **Contexto da Linha Defensiva:** `last_defensive_line_x_start`, `delta_to_last_defensive_line_start`, `inside_defensive_shape_start`.
  - **Pressão e Interplay:** `interplayer_distance`, `interplayer_distance_start`, `interplayer_angle`, `angle_of_engagement`.
  - **Métricas Avançadas Existentes no Dataset:** `xpass_completion`, `xthreat`, `passing_option_score`, `first_line_break`, `last_line_break`.
- **Abordagem Algorítmica:**
  - **Modelagem xPass Baseline:** Classificador supervisionado (XGBoost / Regressão Logística) para estimar $P(\text{pass\_outcome} = \text{completed} \mid \text{Spatial Features})$.
  - **Modelagem xPass Avançada & Valor sem Bola:** Redes Neurais Profundas (MLP) ou **Graph Neural Networks (GNN)** para estimar a probabilidade de passe e o ganho de ameaça gerado por corridas sem bola ($\text{Off-Ball Value} = \text{separation\_gain} \times \Delta\text{xThreat}$).
- **Entrega Analítica:** Mapa térmico de controle de espaço (*Pitch Control*) e ranking de atletas que criam mais valor através do posicionamento e desmarque.

---

### FOCO SECUNDÁRIO (Fase 2): Machine Learning Clássico — Profiling Físico-Tático e Agrupamento de Atletas
- **Objetivo:** Identificar perfis funcionais e padrões de intensidade física de atletas (ex: *High-Volume Engine*, *Explosive Sprinter*, *Defensive Line-Breaker*) além da posição nominal de escalação.
- **Mapeamento de Colunas (`DATA_STRUCTURE.md`):**
  - **Métricas Físicas e Distâncias:** `distance_covered`, `speed_avg`, `speed_avg_band`, `speed_difference`.
  - **Métricas de Intensidade e Ações sem Bola:** `n_off_ball_runs`, `n_passing_options`, `n_passing_options_line_break`, `n_simultaneous_runs`.
  - **Métricas da Aus1League Physical Aggregates:** Distâncias acumuladas por zonas de velocidade (Caminhada, Corrida Leve, Alta Intensidade, Sprints).
- **Abordagem Algorítmica:**
  - Redução de dimensionalidade com **PCA** ou **UMAP** para projeção do espaço físico-tático.
  - Algoritmos de agrupamento não-supervisionado: **K-Means** ou **Gaussian Mixture Models (GMM)**.
- **Entrega Analítica:** Matriz de Similaridade de Jogadores (procura por substitutos com perfil físico equivalente) e Perfis Radar/Spider charts para comissão técnica.

---

## 2. Arquitetura do Sistema (Clean Architecture)

A estrutura do código fonte em `src/` obedece a separação estrita de responsabilidades:

```
src/
├── domain/                  # Camada de Domínio (Entidades e Contratos Puros)
│   ├── entities/            # Dataclasses / Modelos Pydantic v2 sem dependências I/O
│   │   ├── player.py        # Entidade Player, PlayerProfile
│   │   ├── match.py         # Entidade Match, Team, PitchDimensions
│   │   ├── event.py         # Entidade DynamicEvent, PassEvent, OffBallRun
│   │   ├── frame.py         # Entidade TrackingFrame, PlayerPosition
│   │   └── metrics.py       # Dataclass PhysicalMetrics, SpatialMetrics
│   └── protocols/           # Interfaces e Protocolos abstratos (typing.Protocol)
│       ├── repository.py    # Protocol IDatasetRepository
│       └── model.py         # Protocol ITacticalModel, IXPassPredictor
│
├── use_cases/               # Camada de Casos de Uso (Orquestração das Regras de Negócio)
│   ├── feature_extraction/  # Extração e engenharia de atributos espaciais e físicos
│   │   ├── spatial_features.py   # ComputeSpatialFeaturesUseCase (distância linha defensiva, pressão, ângulo, separação)
│   │   └── physical_features.py  # ComputePhysicalAggregatesUseCase
│   └── modeling/            # Fluxos de Treinamento e Predição
│       ├── train_xpass.py        # TrainXPassBaselineUseCase & TrainXPassAdvancedUseCase
│       ├── off_ball_value.py     # ComputeOffBallRunValueUseCase
│       └── cluster_players.py    # ClusterPlayerProfilesUseCase
│
├── infrastructure/          # Camada de Infraestrutura (I/O, Bibliotecas Externas, Parsers)
│   ├── parsers/             # Leitores de JSON e CSV da SkillCorner
│   │   ├── discovery.py     # Script de descoberta de dados
│   │   ├── match_parser.py  # SkillCornerMatchParser (Match metadata & rosters)
│   │   ├── tracking_parser.py # SkillCornerTrackingParser (Events & tracking frames)
│   │   └── csv_parser.py    # SkillCornerCSVParser (Polars for high-speed I/O)
│   └── ml_adapters/         # Adaptadores Scikit-Learn, XGBoost, PyTorch
│       ├── xpass_baseline.py# XGBoostXPassAdapter
│       ├── xpass_deep.py    # PyTorchXPassAdapter
│       └── clustering.py    # SklearnClusterAdapter
│
└── presentation/            # Camada de Apresentação e CLI
    ├── cli.py               # Interface de Linha de Comando (Click / Argparse)
    └── report_generator.py # Gerador de Saídas em Markdown/HTML e visualizações
```

---

## 3. Plano de Validação e Métricas Estatísticas

### 3.1. Métricas de Avaliação por Modelo

1. **Modelo xPass Baseline e Avançado (Spatial Analytics / Deep Learning):**
   - **Log-Loss (Cross-Entropy Loss):** Métrica primária para calibração de probabilidades preditas de passes completos vs incompletos.
   - **ROC-AUC & PR-AUC:** Área sob a curva ROC e Precisão-Recall para lidar com desbalanceamento de passes de alto risco.
   - **Brier Score:** Avalia o erro quadrático médio das probabilidades preditas ($BS = \frac{1}{N}\sum (p_i - y_i)^2$).
   - **Expected Calibration Error (ECE):** Mede o alinhamento das probabilidades preditas com a frequência real de acerto.

2. **Profiling Físico-Tático (ML Clássico - Clusterização):**
   - **Silhouette Score:** Mede o quão bem separado cada cluster está em relação aos clusters vizinhos (alvo $> 0.45$).
   - **Davies-Bouldin Index:** Avalia a dispersão interna dos clusters comparada à distância entre eles (quanto menor, melhor).
   - **Calinski-Harabasz Index:** Razão entre a dispersão inter-cluster e intra-cluster.

---

### 3.2. Estratégia de Validação Temporal e Prevenção de Data Leakage

Para garantir a integridade científica e evitar o vazamento de informações entre treino e teste (*Data Leakage*):

1. **Divisão Baseada em Partida (*Match-Based Split*):**
   - **Regra Rígida:** NUNCA misturar eventos ou frames da mesma partida entre conjuntos de Treino, Validação e Teste.
   - As partidas serão divididas na proporção **70% Treino, 15% Validação, 15% Teste** ou por ordenação cronológica de realização do jogo.

2. **Isolamento de Pré-processamento (*Strict Scaler Pipeline*):**
   - Todos os pré-processamentos (imputação de nulos, padronização `StandardScaler`, redução `PCA`) serão ajustados (*fit*) **exclusivamente nos dados de treino**.
   - Apenas a transformação (*transform*) será aplicada nos conjuntos de validação e teste.
