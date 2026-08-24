# 0003. Contratos Abstratos de Repositório e Inversão de Dependência

- **Data:** 2026-08-24
- **Status:** Aceito
- **Contexto:**
  Para aplicar os princípios **SOLID** (em especial o **ISP - Interface Segregation Principle** e o **DIP - Dependency Inversion Principle**) na Clean Architecture do projeto, era necessário desacoplar a camada de domínio e os casos de uso dos detalhes de implementação concreta de parsers e adaptadores de dados (Polars, Pandas, JSON local, CSV).

- **Decisão:**
  1. **Adoção de `typing.Protocol` com `@runtime_checkable`:**
     - Criação de protocolos abstratos em `src/domain/protocols/repository.py` sem qualquer acoplamento com bibliotecas de I/O.
  2. **Segregação das Interfaces:**
     - `IMatchRepository`: Operações relativas a partidas e elencos.
     - `IEventRepository`: Operações de recuperação de eventos espaciais (`PassEvent`, `OffBallRunEvent`).
     - `ITrackingRepository`: Recuperação de frames temporais de tracking (`TrackingFrame`).
     - `IDatasetRepository`: Interface agregadora para repositórios unificados.

- **Consequências:**
  - *Pontos Positivos:*
    - **Desacoplamento Total:** Casos de uso dependem unicamente das interfaces abstratas, permitindo substituição de provedores de dados ou bancos de dados futuros sem tocar na lógica analítica.
    - **Facilidade de Testes Unitários:** Permite a criação de *Mocks/Fakes* rápidos em memória para testar algoritmos de ML e use cases.
    - **Verificação Estática e Dinâmica:** Suporte a análise estática via `mypy` e validação em tempo de execução via `isinstance`.
  - *Tradeoffs / Custos:*
    - Exige que adaptadores concretos em `src/infrastructure/` implementem estritamente as assinaturas dos métodos definidos nos protocolos.
