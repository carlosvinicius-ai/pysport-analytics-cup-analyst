# 0002. Representação de Entidades Espaciais, Imutabilidade e Sistema de Coordenadas

- **Data:** 2026-08-24
- **Status:** Aceito
- **Contexto:**
  Na modelagem dos dados espaciais de passes, corridas sem bola e frames de tracking da SkillCorner, era necessário definir:
  1. O sistema de coordenadas adotado nas entidades puras de domínio.
  2. O contrato de mutabilidade para eventos e snapshots de tracking histórico.
  3. A abrangência dos atributos contextuais extraídos dos eventos dinâmicos.

- **Decisão:**
  1. **Coordenadas em Metros Reais:**
     - As entidades de domínio (`PassEvent`, `OffBallRunEvent`, `PlayerPosition`, `TrackingFrame`) mantêm as coordenadas espaciais métricas originais fornecidas pela SkillCorner (origem no centro do campo, $x \in [-52.5, 52.5]$ m e $y \in [-34.0, 34.0]$ m). Qualquer normalização ou transformação para tensores de Machine Learning será de responsabilidade exclusiva da camada de `use_cases`.
  2. **Imutabilidade Rigorosa (`frozen=True`):**
     - Todas as entidades de eventos e frames são declaradas como dataclasses imutáveis (`frozen=True`), garantindo integridade de dados históricos, *hashability* e *thread-safety* durante processamento concorrente.
  3. **Completude Estrutural com Tipagem Forte:**
     - Inclusão abrangente de métricas contextuais (como ganho de separação, distância para última linha defensiva, pressão do adversário mais próximo, $x\text{Threat}$ e probabilidade de passe pré-calculada) com anotações de tipo opcionais (`Optional[float]`).

- **Consequências:**
  - *Pontos Positivos:*
    - **Clareza Tática:** Analistas e desenvolvedores operam com distâncias reais em metros intuitivas para o futebol.
    - **Segurança e Confiabilidade:** Elimina riscos de mutação de estado acidental durante o pipeline.
    - **Riqueza de Informação:** Permite que múltiplos use cases (xPass, Off-Ball Value, Pitch Control) consumam as mesmas entidades sem recarregar arquivos.
  - *Tradeoffs / Custos:*
    - Dataclasses imutáveis exigem recriação de instâncias caso haja necessidade de enriquecimento de dados em etapas posteriores (usando `dataclasses.replace`).
