# AGENTS.md - Diretrizes Globais para Agentes de IA

## 1. Visão Geral do Projeto
- **Nome:** Sports Analytics - SkillCorner EDA & Modeling
- **Objetivo:** Analisar dados de tracking e métricas físicas de futebol da SkillCorner para extrair insights táticos/físicos e construir modelos de Data Science (ML/DL/NLP).
- **Papel da IA:** Atuar como Lead Data Scientist e Senior Data Engineer. Priorize rigor estatístico, modularidade, desacoplamento e código limpo em vez de soluções rápidas e desorganizadas.

## 2. Fluxo de Git e Controle de Versão (REGRAS DE BRANCH)
- **Verificação Inicial:** Antes de criar, alterar arquivos ou escrever código, verifique a branch atual executando `git branch --show-current`.
- **Proteção da Branch Main:** **NUNCA** faça alterações, commits ou crie novos arquivos diretamente na branch `main` (ou `master`).
- **Criação de Branches:** Se estiver na branch `main`, crie imediatamente uma nova branch descritiva antes de qualquer alteração:
  - Estrutura de nomes: `feature/nome-da-funcionalidade`, `eda/nome-da-analise`, `refactor/o-que-mudou` ou `chore/configuracoes`.
  - Exemplo: `git checkout -b eda/skillcorner-data-discovery`
- **Mensagens de Commit:** Siga o padrão *Conventional Commits* (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`).

## 3. Arquitetura de Software e Design (CLEAN ARCHITECTURE & SOLID)
O código fonte em `src/` deve seguir rigorosamente a **Clean Architecture** e os princípios **SOLID**:

### Divisão de Camadas (Clean Architecture)
1. **Domain / Entities (`src/domain/`):**
   - Regras de negócio e representações puras do futebol (ex: classes/dataclasses de `Player`, `Match`, `TrackingFrame`, `Metrics`).
   - Esta camada não deve ter dependências externas de frameworks, bibliotecas de I/O ou banco de dados.
2. **Use Cases / Application (`src/use_cases/`):**
   - Orquestração dos fluxos analíticos (ex: `CalculatePlayerSpeedDistribution`, `TrainInjuryModel`, `ParseTrackingData`).
   - Contém a lógica das tarefas sem saber de onde os dados vêm ou para onde vão.
3. **Infrastructure / Adapters (`src/infrastructure/`):**
   - Implementações concretas de I/O: parsers dos JSONs da SkillCorner, conexões com banco de dados, exportadores de arquivo e integração com bibliotecas específicas (`polars`, `pandas`).
4. **Interfaces / Presentation (`src/presentation/`):**
   - Scripts de execução, CLI, Jupyter Notebooks (`notebooks/`) e geradores de relatórios em Markdown.

### Princípios SOLID
- **Single Responsibility (SRP):** Cada módulo, classe ou função deve ter apenas uma razão para mudar. Não misture parsing de JSON com cálculo estatístico no mesmo arquivo.
- **Open/Closed (OCP):** Crie abstrações (Interfaces/Classes Base Abstratas) para que novas fontes de dados ou novos modelos possam ser adicionados sem alterar o código existente.
- **Liskov Substitution (LSP):** Subtipos e leitores alternativos de dados devem respeitar os contratos das interfaces base sem quebrar a execução.
- **Interface Segregation (ISP):** Prefira interfaces/protocolos pequenos e específicos em vez de interfaces genéricas e pesadas.
- **Dependency Inversion (DIP):** Módulos de alto nível (Use Cases) devem depender de abstrações (Interfaces/Protocols), nunca de implementações concretas (Infraestrutura).

## 4. Stack Tecnológica & Padrões de Código
- **Linguagem:** Python 3.11+
- **Manipulação de Dados:** Preferencialmente `polars` para performance ou `pandas` quando estritamente necessário.
- **Tipagem:** Utilização obrigatória de `Type Hints` e `Protocols` (`typing`).
- **Documentação:** Docstrings no padrão Google Style para todas as funções/classes.
- **Validação:** Pydantic v2 para validação de contratos de dados e schemas.

## 5. Gestão de Dados e Limites de Contexto (REGRAS RÍGIDAS)
- **NUNCA** tente ler ou carregar arquivos de dados brutos (`.json`, `.csv`, `.parquet`) inteiros diretamente no chat/contexto da conversa.
- **Processamento Local:** Toda inspeção e transformação deve ser feita via scripts Python executados no ambiente local.
- **Saídas de Dados:** Os scripts devem salvar relatórios e resumos estruturados na pasta `reports/` ou em arquivos `.md` dedicados (`DATA_STRUCTURE.md`, `SPEC.md`).
- **Arquivos Grandes:** Para arquivos de tracking espacial com milhões de linhas, utilize amostragem (`head`, `slice`) ou processamento streaming durante a fase exploratória.

## 6. Estrutura do Repositório
├── data/                  # Dados brutos e processados (ignorar no git)
├── notebooks/             # Prototipagem rápida e visualizações isoladas
├── reports/               # Relatórios gerados (.md, .html, .png)
├── tests/                 # Testes unitários e de integração (pytest)
├── src/                   # Código-fonte sob Clean Architecture
│   ├── domain/            # Entidades do futebol e interfaces/protocolos
│   ├── use_cases/         # Algoritmos de análise, ML, DL e transformações
│   ├── infrastructure/    # Parsers dos JSONs SkillCorner, I/O e Polars
│   └── presentation/      # CLI e pontes para notebooks/relatórios
├── AGENTS.md              # Este arquivo de contexto
└── pyproject.toml / requirements.txt