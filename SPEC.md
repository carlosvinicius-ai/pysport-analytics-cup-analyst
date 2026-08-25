# Especificação Técnica e Arquitetural — SkillCorner Sports Analytics

## Visão Geral do Projeto
O objetivo deste projeto é construir uma plataforma modular de **Data Science & Sports Analytics** focada 100% na modelagem matemática, estatística e espacial utilizando dados de tracking e métricas físicas/táticas da **SkillCorner Open Data**. A plataforma adota rigorosamente a **Clean Architecture** e os princípios **SOLID**, permitindo extrair métricas avançadas de controle espacial, probabilidade de passe e perfilamento tático de atletas.

---

## 1. Objetivos e Casos de Uso de Data Science

### FOCO PRINCIPAL (Fase 1): Spatial Analytics & Deep Learning — Probabilidade de Passe (`xPass`) e Valor do Desmarque sem Bola (*Off-Ball Run Value*)

- **Objetivo:** Quantificar o risco e a recompensa de cada tentativa de passe em janelas sob pressão defensiva e avaliar o valor criado pelos atletas através de movimentações e desmarques sem a posse da bola.

- **Matriz de Features Espaciais Descobertas e Construídas (`ComputeSpatialFeaturesUseCase`):**
  - **Geometria Territorial do Passe:**
    - `pass_distance`: Distância euclidiana total percorrida pelo passe (em metros).
    - `pass_angle`: Ângulo trigonométrico de execução da trajetória.
    - `progression_x`: Ganho territorial para frente ($x_{\text{end}} - x_{\text{start}}$ em metros).
    - `lateral_displacement`: Deslocamento lateral no campo ($|y_{\text{end}} - y_{\text{start}}|$).
  - **Orientação Espacial em Relação ao Gol Adversário ($x = 52.5$m, $y = 0.0$m):**
    - `distance_to_goal_start` e `distance_to_goal_end`: Distância em linha reta até a trave adversária.
    - `angle_to_goal_start` e `angle_to_goal_end`: Ângulo angular de visão do gol.
  - **Pressão Defensiva e Separação Espacial (Limiar Empírico do EDA):**
    - `interplayer_distance_start`: Distância do marcador mais próximo no momento do passe.
    - `has_defensive_pressure`: Flag booleana de pressão imediata (quando `interplayer_distance_start` $\le 3.0$ metros, ponto de inflexão comprovado onde a taxa de acerto cai de $82\%$ para $< 58\%$).
    - `separation_start`, `separation_end` e `separation_gain`: Espaço criado pelo atleta antes e depois da ação.
  - **Contexto de Linha Defensiva e Ruptura:**
    - `last_defensive_line_x_start`: Posição da última linha defensiva adversária.
    - `delta_to_last_defensive_line_start`: Distância do passador para a linha de zaga.
    - `first_line_break` e `last_line_break`: Flags indicativas de quebra de linhas táticas.
  - **Métricas de Benchmark da SkillCorner:**
    - `xthreat` ($x\text{T}$): Valor de ameaça esperada gerada pelo evento.
    - `xpass_completion`: Probabilidade de conclusão fornecida no dataset para comparação de calibração.

- **Métrica de Desempenho do Passador ($x\text{Pass Added}$):**
  $$\text{xPass Added} (xPA) = \sum_{p \in \text{completos}} (1 - xPass_p) - \sum_{p \in \text{incompletos}} (xPass_p)$$
  Permite isolar a habilidade técnica individual do passador contra a facilidade/dificuldade inerente do contexto espacial da jogada.

- **Abordagem Algorítmica:**
  - **Marco 2 (Baseline xPass):** Classificador tabular supervisionado (**XGBoost / LightGBM**) com calibração isotônica para estimar $P(\text{pass\_outcome} = \text{completed} \mid \text{Spatial Features})$.
  - **Marco 3 (xPass Avançado & Valor sem Bola):** Arquitetura Neural Profunda (MLP com *Feature Interactions* / Embeddings Posicionais) e cálculo do valor do desmarque:
    $$\text{Off-Ball Run Value} = \text{separation\_gain} \times \Delta\text{xThreat}$$

---

### FOCO SECUNDÁRIO (Fase 2): Machine Learning Clássico — Profiling Físico-Tático e Agrupamento de Atletas

- **Objetivo:** Identificar perfis funcionais e padrões de intensidade física de atletas (ex: *High-Volume Engine*, *Explosive Sprinter*, *Defensive Line-Breaker*) combinando eventos por partida e agregados de temporada da A-League.
- **Base de Dados Utilizada:**
  - `data/opendata/data/aggregates/aus1league_physicalaggregates_20242025.csv`
  - `data/opendata/data/aggregates/aus1league_passingaggregates_20242025.csv`
  - `data/opendata/data/aggregates/aus1league_obraggregates_20242025.csv`
- **Abordagem Algorítmica:**
  - Redução de dimensionalidade com **PCA** / **UMAP** para projeção do espaço de atributos.
  - Algoritmos de agrupamento não-supervisionado: **K-Means** e **Gaussian Mixture Models (GMM)**.
- **Entrega Analítica:** Matriz de Similaridade de Atletas (busca por substitutos de elenco) e Radar Charts táticos.

---

## 2. Arquitetura do Sistema (Clean Architecture)

O código segue rigorosamente as 4 camadas da Clean Architecture, com decisões registradas em `docs/adr/`:

```
src/
├── domain/                  # Camada de Domínio (Entidades e Protocolos Puros)
│   ├── entities/            # Dataclasses imutáveis (frozen=True) em metros reais (ADR 0002)
│   │   ├── player.py        # Player, PlayerRole, PlayerPlayingTime
│   │   ├── match.py         # Match, Team, PitchDimensions, Stadium, MatchPeriod
│   │   ├── event.py         # PassEvent, OffBallRunEvent
│   │   └── frame.py         # TrackingFrame, PlayerPosition, BallPosition
│   └── protocols/           # Contratos abstratos com @runtime_checkable (ADR 0003)
│       ├── repository.py    # IMatchRepository, IEventRepository, ITrackingRepository, IDatasetRepository
│       └── model.py         # IXPassModel, IClusteringModel
│
├── use_cases/               # Camada de Casos de Uso (Lógica da Aplicação)
│   ├── feature_extraction/  # Engenharia de atributos espaciais e físicos
│   │   ├── spatial_features.py   # ComputeSpatialFeaturesUseCase (Matriz de variáveis espaciais)
│   │   └── physical_features.py  # ComputePhysicalAggregatesUseCase (Consolidação física)
│   └── modeling/            # Orquestração de Treinamento, Validação e Métricas
│       ├── validation_split.py   # MatchChronologicalSplitter (Zero Data Leakage)
│       ├── train_xpass.py        # TrainXPassBaselineUseCase & TrainXPassAdvancedUseCase
│       ├── off_ball_value.py     # ComputeOffBallRunValueUseCase
│       └── cluster_players.py    # ClusterPlayerProfilesUseCase
│
├── infrastructure/          # Camada de Infraestrutura (I/O, Polars e ML Adapters)
│   ├── parsers/             # Ingestão de alta performance com Polars (ADR 0001)
│   │   ├── discovery.py     # Auditoria e volumetria de dados
│   │   ├── match_parser.py  # SkillCornerMatchParser (JSONs de partidas e elencos)
│   │   └── tracking_parser.py # SkillCornerTrackingParser (CSV dinâmico com Polars)
│   └── ml_adapters/         # Implementações concretas de modelos de ML/DL
│       ├── xpass_baseline.py# XGBoostXPassAdapter (XGBoost / LightGBM)
│       ├── xpass_deep.py    # PyTorchXPassAdapter (Rede Neural Profunda)
│       └── clustering.py    # SklearnClusterAdapter (K-Means/GMM com PCA)
│
└── presentation/            # Camada de Apresentação, Notebooks e Visualizações
    ├── spatial_visualizer.py# Gerador de Pass Maps, Heatmaps e Pitch Control
    ├── cli.py               # Interface CLI para execução de pipelines
    └── notebooks/           # exploration.ipynb (EDA visual com mplsoccer)
```

---

## 3. Plano de Validação e Métricas Estatísticas

### 3.1. Métricas de Avaliação dos Modelos de xPass
- **Log-Loss (Binary Cross-Entropy):** Métrica primária para aferir a qualidade probabilística das predições ($-\frac{1}{N}\sum [y_i \ln(p_i) + (1-y_i)\ln(1-p_i)]$).
- **Brier Score:** Erro quadrático médio das probabilidades preditas ($BS = \frac{1}{N}\sum (p_i - y_i)^2$).
- **ROC-AUC & PR-AUC:** Capacidade discriminativa entre passes completos e interceptados, mesmo em cenários de alta pressão defensiva.
- **Expected Calibration Error (ECE):** Aferição de confiabilidade da calibração (a probabilidade de $70\%$ deve corresponder a 7 acertos a cada 10 passes na prática).
- **Interpretabilidade (SHAP Values):** Importância e impacto marginal de cada feature no cálculo do xPass.

---

### 3.2. Estratégia de Validação Temporal e Prevenção de Data Leakage
1. **Divisão Baseada em Partidas Ordenadas Cronologicamente (*Match-Based Chronological Split*):**
   - **Regra Rígida:** NUNCA misturar eventos ou frames da mesma partida entre conjuntos de treino e teste.
   - Partidas divididas por ordem cronológica: **7 Partidas para Treino (70%)**, **1 Partida para Validação (10%)** e **2 Partidas para Teste Final (20%)**.
2. **Isolamento de Pré-processamento (*Strict Pipeline Isolation*):**
   - Todo escalonamento (`StandardScaler`) e imputação de valores ausentes são ajustados exclusivamente no conjunto de treino (`fit`) e aplicados nos dados de validação e teste (`transform`).

---

## 4. Governança de Decisões Arquiteturais (ADRs)

| ADR | Título | Status |
| :--- | :--- | :--- |
| [ADR 0001](file:///d:/Hackaton/pysport-analytics-cup-analyst/docs/adr/0001-adocao-clean-architecture-e-polars.md) | Adoção da Clean Architecture e Polars para Performance | Aceito ✅ |
| [ADR 0002](file:///d:/Hackaton/pysport-analytics-cup-analyst/docs/adr/0002-representacao-entidades-espaciais-e-coordenadas.md) | Representação em Metros Reais e Imutabilidade de Entidades Espaciais | Aceito ✅ |
| [ADR 0003](file:///d:/Hackaton/pysport-analytics-cup-analyst/docs/adr/0003-protocolos-e-interfaces-de-repositorio.md) | Contratos Abstratos de Repositório e Inversão de Dependência (DIP/ISP) | Aceito ✅ |
