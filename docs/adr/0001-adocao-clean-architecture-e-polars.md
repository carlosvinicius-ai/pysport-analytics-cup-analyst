# 0001. Adoção da Clean Architecture e Polars para Processamento de Dados da SkillCorner

- **Data:** 2026-08-24
- **Status:** Aceito
- **Contexto:**
  O projeto de Sports Analytics processa grandes volumes de dados de tracking espacial e eventos dinâmicos do futebol oriundos da SkillCorner Open Data. Para garantir a manutenibilidade, testabilidade e escalabilidade da solução analítica, era necessário definir:
  1. Uma arquitetura de software desacoplada das bibliotecas de I/O e algoritmos de ML.
  2. Uma engine de manipulação de dados de alta performance capaz de processar conjuntos de dados de tracking espacial sem problemas de concorrência ou gargalos de memória.

- **Decisão:**
  1. **Adoção da Clean Architecture & Princípios SOLID:**
     - Divisão estrita em 4 camadas de código fonte (`src/`):
       - `src/domain/`: Entidades puras do futebol (`Player`, `Match`, `PassEvent`, `TrackingFrame`) e contratos (`Protocols`). Isento de dependências de I/O ou bibliotecas de terceiros.
       - `src/use_cases/`: Orquestração da lógica analítica e treinamento de modelos de dados.
       - `src/infrastructure/`: Adaptadores I/O (parsers SkillCorner), suporte a Polars/Pandas e persistência de modelos.
       - `src/presentation/`: Scripts CLI e geradores de relatórios/visualizações.
  2. **Uso do Polars como Engine Principal de Ingestão:**
     - Utilização prioritária de `polars` em substituição ou complementaridade ao `pandas` na camada de infraestrutura devido à sua execução multithreaded e otimização por vetorização em Rust.

- **Consequências:**
  - *Pontos Positivos:*
    - **Alta Testabilidade:** As entidades e casos de uso podem ser testados com suítes unitárias rápidas e puras sem mockar arquivos de dados complexos.
    - **Independência de Frameworks:** Facilidade para trocar algoritmos de ML ou parsers no futuro sem afetar as regras de negócio.
    - **Desempenho de Processamento:** Polars processa eventos dinâmicos e tracking espacial em fração do tempo e com menor pegada de memória RAM.
  - *Tradeoffs / Custos:*
    - Complexidade inicial de boilerplate e separação de camadas.
    - Necessidade de conversões pontuais para Pandas/NumPy no momento de passar tensores para bibliotecas como XGBoost/PyTorch.
