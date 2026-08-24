# AGENTS.md - Diretrizes Globais para Agentes de IA

## 1. Visão Geral do Projeto
- **Nome:** Sports Analytics - SkillCorner EDA & Modeling
- **Objetivo:** Analisar dados de tracking e métricas físicas de futebol da SkillCorner para extrair insights táticos/físicos e construir modelos de Data Science (ML/DL/NLP).
- **Papel da IA:** Atuar como Lead Data Scientist e Senior Data Engineer. Priorize rigor estatístico, modularidade, desacoplamento e código limpo em vez de soluções rápidas e desorganizadas.

## 2. Fluxo de Git, Controle de Versão e Confirmação de Commits
- **Verificação Inicial:** Antes de criar, alterar arquivos ou escrever código, verifique a branch atual executando `git branch --show-current`.
- **Proteção da Branch Main:** **NUNCA** faça alterações, commits ou crie novos arquivos diretamente na branch `main` (ou `master`).
- **Criação de Branches:** Se estiver na branch `main`, crie imediatamente uma nova branch descritiva antes de qualquer alteração:
  - Estrutura de nomes: `feature/nome-da-funcionalidade`, `eda/nome-da-analise`, `refactor/o-que-mudou` ou `chore/configuracoes`.
  - Exemplo: `git checkout -b eda/skillcorner-data-discovery`
- **Validação e Confirmação Obrigatória do Usuário (REGRA RÍGIDA DE COMMITS):**
  - **NUNCA** execute comandos de commit (`git commit`) de forma automática ou presumida.
  - Após implementar uma tarefa ou alteração e rodar os devidos testes, a IA deve **PARAR**, apresentar o resumo executivo detalhado das alterações para o usuário e **AGUARDAR** a validação e autorização explícita do usuário antes de realizar qualquer commit no Git.
- **Mensagens de Commit:** Siga o padrão *Conventional Commits* (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`).

## 3. Governança de Decisões Arquiteturais (ADRs)
- **Quando Criar um ADR:** Sempre que uma decisão técnica ou arquitetural de impacto for necessária (ex: escolha de bibliotecas, definição de padrões de coordenadas, imutabilidade de entidades, estratégias de modelagem de dados ou arquitetura de redes neurais), a IA deve registrar a decisão em `docs/adr/`.
- **Padrão de Nomenclatura:** `docs/adr/XXXX-titulo-da-decisao.md` (sequencial, com 4 dígitos).
- **Template Obrigatório:** Seguir rigorosamente a estrutura definida em `docs/adr/0000-template.md` (*Data, Status, Contexto, Decisão, Consequências - Pontos Positivos e Tradeoffs*).
- **Rastreamento no Planejamento:** Toda nova ADR criada deve ser referenciada no `PLAN.md` no marco correspondente.

## 4. Arquitetura de Software e Design (CLEAN ARCHITECTURE & SOLID)
O código fonte em `src/` deve seguir rigorosamente a **Clean Architecture** e os princípios **SOLID**:

### Divisão de Camadas (Clean Architecture)
1. **Domain / Entities (`src/domain/`):**
   - Regras de negócio e representações puras do futebol (ex: classes/dataclasses de `Player`, `Match`, `PassEvent`, `TrackingFrame`, `Metrics`).
   - Esta camada não deve ter dependências externas de frameworks, bibliotecas de I/O ou banco de dados.
2. **Use Cases / Application (`src/use_cases/`):**
   - Orquestração dos fluxos analíticos (ex: `ComputeSpatialFeatures`, `TrainXPassBaseline`, `ClusterPlayerProfiles`).
   - Contém a lógica das tarefas sem saber de onde os dados vêm ou para onde vão.
3. **Infrastructure / Adapters (`src/infrastructure/`):**
   - Implementações concretas de I/O: parsers dos JSONs e CSVs da SkillCorner, adaptadores de ML/DL e integração com bibliotecas de alta performance (`polars`, `pandas`).
4. **Interfaces / Presentation (`src/presentation/`):**
   - Scripts de execução, CLI, Jupyter Notebooks (`notebooks/`) e geradores de relatórios e visualizações.

### Princípios SOLID
- **Single Responsibility (SRP):** Cada módulo, classe ou função deve ter apenas uma razão para mudar. Não misture parsing de JSON com cálculo estatístico no mesmo arquivo.
- **Open/Closed (OCP):** Crie abstrações (Interfaces/Classes Base Abstratas/Protocols) para que novas fontes de dados ou novos modelos possam ser adicionados sem alterar o código existente.
- **Liskov Substitution (LSP):** Subtipos e leitores alternativos de dados devem respeitar os contratos das interfaces base sem quebrar a execução.
- **Interface Segregation (ISP):** Prefira interfaces/protocolos pequenos e específicos em vez de interfaces genéricas e pesadas.
- **Dependency Inversion (DIP):** Módulos de alto nível (Use Cases) devem depender de abstrações (Interfaces/Protocols), nunca de implementações concretas (Infraestrutura).

## 5. Stack Tecnológica & Padrões de Código
- **Linguagem:** Python 3.11+
- **Idioma:** Todos os comentários, docstrings e relatórios devem ser escritos em **Português (pt-BR)**.
- **Manipulação de Dados:** Preferencialmente `polars` para performance ou `pandas` quando estritamente necessário.
- **Tipagem:** Utilização obrigatória de `Type Hints` e `Protocols` (`typing`).
- **Documentação:** Docstrings no padrão Google Style em português para todas as funções/classes.
- **Validação:** Dataclasses imutáveis (`frozen=True`) no domínio e Pydantic v2 para validação de contratos de dados e schemas.

## 6. Gestão de Dados e Limites de Contexto (REGRAS RÍGIDAS)
- **NUNCA** tente ler ou carregar arquivos de dados brutos (`.json`, `.csv`, `.parquet`) inteiros diretamente no chat/contexto da conversa.
- **Processamento Local:** Toda inspeção e transformação deve ser feita via scripts Python executados no ambiente local.
- **Saídas de Dados:** Os scripts devem salvar relatórios e resumos estruturados na pasta `reports/` ou em arquivos `.md` dedicados (`DATA_STRUCTURE.md`, `SPEC.md`, `PLAN.md`).
- **Arquivos Grandes:** Para arquivos de tracking espacial com milhões de linhas, utilize amostragem (`head`, `slice`) ou processamento streaming durante a fase exploratória.

## 7. Estrutura do Repositório
├── data/                  # Dados brutos e processados (ignorar no git)
├── docs/                  # Documentação e governança do projeto
│   └── adr/               # Architectural Decision Records (ADRs)
├── notebooks/             # Prototipagem rápida e visualizações isoladas
├── reports/               # Relatórios gerados (.md, .html, .png)
├── tests/                 # Testes unitários e de integração (pytest)
├── src/                   # Código-fonte sob Clean Architecture
│   ├── domain/            # Entidades do futebol e interfaces/protocolos
│   ├── use_cases/         # Algoritmos de análise, ML, DL e transformações
│   ├── infrastructure/    # Parsers dos dados SkillCorner, I/O e Polars
│   └── presentation/      # CLI, relatórios e visualizações
├── AGENTS.md              # Este arquivo de contexto e regras globais
├── SPEC.md                # Especificação técnica dos modelos
├── PLAN.md                # Plano de execução incremental
└── pyproject.toml / requirements.txt