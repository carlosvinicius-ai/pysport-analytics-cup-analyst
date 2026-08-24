"""Parser de Descoberta e Inspeção dos Dados da SkillCorner.

Componente de infraestrutura responsável por inspecionar localmente as bases da SkillCorner,
extrair schemas, tipos de dados, níveis de aninhamento, relacionamentos de chaves e métricas
de volumetria, gerando o relatório estruturado reports/DATA_STRUCTURE.md sob a Clean Architecture.
"""

from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Set, Union
import pandas as pd

# Garante saída UTF-8 padrão no console Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


@dataclass
class DatasetMetrics:
    """Dataclass com as métricas resumidas do dataset da SkillCorner."""
    total_matches: int = 0
    unique_players: Set[int] = field(default_factory=set)
    unique_teams: Set[int] = field(default_factory=set)
    total_dynamic_events_records: int = 0
    total_phases_records: int = 0
    categories_found: Dict[str, List[str]] = field(default_factory=dict)
    file_tree: List[str] = field(default_factory=list)


def get_json_schema(data: Any, max_depth: int = 5, current_depth: int = 1) -> Any:
    """Infere recursivamente o schema JSON, tipos de dados e níveis de aninhamento.

    Args:
        data: Objeto JSON parseado (dict, list ou primitivo).
        max_depth: Profundidade máxima de recursão.
        current_depth: Nível de profundidade atual.

    Returns:
        Representação estruturada do schema com os tipos de dados.
    """
    if current_depth > max_depth:
        return "..."

    if isinstance(data, dict):
        schema = {}
        for key, val in data.items():
            schema[key] = get_json_schema(val, max_depth, current_depth + 1)
        return schema
    elif isinstance(data, list):
        if not data:
            return "List[Empty]"
        # Inspeciona o primeiro item como amostra representativa
        sample_schema = get_json_schema(data[0], max_depth, current_depth + 1)
        return f"List[{sample_schema}]"
    else:
        return type(data).__name__


class SkillCornerDiscoveryParser:
    """Classe de parser para inspecionar arquivos locais da SkillCorner Open Data."""

    def __init__(self, data_dir: Union[str, Path]):
        """Inicializa o parser com o diretório raiz dos dados.

        Args:
            data_dir: Caminho para a pasta contendo os arquivos da SkillCorner.
        """
        self.data_dir = Path(data_dir)
        self.metrics = DatasetMetrics()
        self.schemas: Dict[str, Any] = {}

    def scan_files(self) -> DatasetMetrics:
        """Varre a árvore de diretórios e categoriza os arquivos encontrados."""
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Diretório de dados não encontrado: {self.data_dir}")

        categories = {
            "Metadados de Partidas": [],
            "Métricas Agregadas": [],
            "Eventos Dinâmicos e Tracking Tático": [],
            "Fases do Jogo": []
        }

        file_list = []
        for root, _, files in os.walk(self.data_dir):
            rel_root = Path(root).relative_to(self.data_dir)
            for f in sorted(files):
                if f.startswith("."):
                    continue
                rel_path = str(rel_root / f) if str(rel_root) != "." else f
                file_list.append(rel_path)

                if f == "matches.json" or f.endswith("_match.json"):
                    categories["Metadados de Partidas"].append(rel_path)
                elif f.endswith("aggregates_20242025.csv"):
                    categories["Métricas Agregadas"].append(rel_path)
                elif f.endswith("_dynamic_events.csv"):
                    categories["Eventos Dinâmicos e Tracking Tático"].append(rel_path)
                elif f.endswith("_phases_of_play.csv"):
                    categories["Fases do Jogo"].append(rel_path)

        self.metrics.file_tree = sorted(file_list)
        self.metrics.categories_found = categories
        return self.metrics

    def inspect_matches_metadata(self) -> Dict[str, Any]:
        """Inspeciona os metadados do arquivo matches.json."""
        matches_json_path = self.data_dir / "data" / "matches.json"
        if not matches_json_path.exists():
            matches_files = list(self.data_dir.glob("**/matches.json"))
            if matches_files:
                matches_json_path = matches_files[0]

        if matches_json_path.exists():
            with open(matches_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list):
                self.metrics.total_matches = len(data)
                sample_item = data[0] if data else {}
                self.schemas["matches.json"] = get_json_schema(sample_item)

                for m in data:
                    if "home_team" in m and isinstance(m["home_team"], dict):
                        self.metrics.unique_teams.add(m["home_team"].get("id"))
                    if "away_team" in m and isinstance(m["away_team"], dict):
                        self.metrics.unique_teams.add(m["away_team"].get("id"))
        return self.schemas.get("matches.json", {})

    def inspect_single_match_json(self) -> Dict[str, Any]:
        """Inspeciona o schema detalhado do JSON individual da partida (ex: <match_id>_match.json)."""
        match_json_files = list(self.data_dir.glob("**/*_match.json"))
        if match_json_files:
            sample_file = match_json_files[0]
            with open(sample_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.schemas["single_match.json"] = get_json_schema(data)

            if isinstance(data, dict):
                players = data.get("players", [])
                for p in players:
                    if isinstance(p, dict) and "id" in p:
                        self.metrics.unique_players.add(p["id"])

                teams = data.get("teams", [])
                for t in teams:
                    if isinstance(t, dict) and "id" in t:
                        self.metrics.unique_teams.add(t["id"])
                        
        return self.schemas.get("single_match.json", {})

    def inspect_tabular_data(self):
        """Inspeciona CSVs de eventos dinâmicos, fases de jogo e métricas físicas agregadas."""
        # Eventos Dinâmicos
        dynamic_csvs = list(self.data_dir.glob("**/*_dynamic_events.csv"))
        for csv_path in dynamic_csvs:
            df = pd.read_csv(csv_path)
            self.metrics.total_dynamic_events_records += len(df)
            if "player_id" in df.columns:
                self.metrics.unique_players.update(df["player_id"].dropna().astype(int).tolist())
            if "team_id" in df.columns:
                self.metrics.unique_teams.update(df["team_id"].dropna().astype(int).tolist())
            if "dynamic_events.csv" not in self.schemas:
                self.schemas["dynamic_events.csv"] = {col: str(dtype) for col, dtype in df.dtypes.items()}

        # Fases do Jogo
        phases_csvs = list(self.data_dir.glob("**/*_phases_of_play.csv"))
        for csv_path in phases_csvs:
            df = pd.read_csv(csv_path)
            self.metrics.total_phases_records += len(df)
            if "team_id" in df.columns:
                self.metrics.unique_teams.update(df["team_id"].dropna().astype(int).tolist())
            if "phases_of_play.csv" not in self.schemas:
                self.schemas["phases_of_play.csv"] = {col: str(dtype) for col, dtype in df.dtypes.items()}

        # Agregados
        aggregates_csvs = list(self.data_dir.glob("**/aggregates/*.csv"))
        for csv_path in aggregates_csvs:
            filename = csv_path.name
            df = pd.read_csv(csv_path)
            if "player_id" in df.columns:
                self.metrics.unique_players.update(df["player_id"].dropna().astype(int).tolist())
            if "team_id" in df.columns:
                self.metrics.unique_teams.update(df["team_id"].dropna().astype(int).tolist())
            self.schemas[f"aggregate_{filename}"] = {col: str(dtype) for col, dtype in df.dtypes.items()}

    def run_full_discovery(self) -> DatasetMetrics:
        """Executa a esteira completa de descoberta e inspeção."""
        self.scan_files()
        self.inspect_matches_metadata()
        self.inspect_single_match_json()
        self.inspect_tabular_data()
        return self.metrics

    def generate_report(self, output_path: Union[str, Path]) -> str:
        """Gera o relatório estruturado em markdown e salva no caminho de saída.

        Args:
            output_path: Caminho do arquivo markdown de destino.

        Returns:
            Conteúdo do relatório gerado.
        """
        out_p = Path(output_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)

        report = []
        report.append("# Relatório de Descoberta e Estrutura dos Dados — SkillCorner Open Data\n")
        report.append("Este relatório documenta a estrutura, schemas, relacionamentos entre entidades e volume total de dados da base SkillCorner Open Data.\n")

        report.append("## 1. Visão Geral e Estatísticas de Volume\n")
        report.append("> [!NOTE]")
        report.append("> Os volumes abaixo representam o conjunto total de dados abertos inspecionados localmente em `data/opendata`.\n")
        report.append("| Métrica | Valor |")
        report.append("| :--- | :--- |")
        report.append(f"| **Total de Partidas Disponíveis** | `{self.metrics.total_matches}` |")
        report.append(f"| **Total de Jogadores Únicos** | `{len(self.metrics.unique_players)}` |")
        report.append(f"| **Total de Equipes Únicas** | `{len(self.metrics.unique_teams)}` |")
        report.append(f"| **Total de Eventos Dinâmicos/Tracking (Registros)** | `{self.metrics.total_dynamic_events_records:,}` |")
        report.append(f"| **Total de Fases de Jogo (Registros)** | `{self.metrics.total_phases_records:,}` |\n")

        report.append("## 2. Árvore de Arquivos e Categorização dos Dados\n")
        for cat_name, file_list in self.metrics.categories_found.items():
            report.append(f"### {cat_name} ({len(file_list)} arquivos)")
            for f in file_list[:15]:
                report.append(f"- `{f}`")
            if len(file_list) > 15:
                report.append(f"- *... e mais {len(file_list) - 15} arquivos.*")
            report.append("")

        report.append("## 3. Schemas, Tipos de Dados e Níveis de Aninhamento\n")

        if "matches.json" in self.schemas:
            report.append("### Schema de `matches.json` (Metadados Globais das Partidas)")
            report.append("Contém a lista de partidas com informações de data, competição, estádio e placar.")
            report.append("```json")
            report.append(json.dumps(self.schemas["matches.json"], indent=2))
            report.append("```\n")

        if "single_match.json" in self.schemas:
            report.append("### Schema de `<match_id>_match.json` (Detalhes da Partida & Elencos)")
            report.append("Arquivo individual por partida contendo lista completa de jogadores, treinadores, árbitros, dimensões do campo e alinhamento tático.")
            report.append("```json")
            report.append(json.dumps(self.schemas["single_match.json"], indent=2))
            report.append("```\n")

        if "dynamic_events.csv" in self.schemas:
            report.append("### Schema de `<match_id>_dynamic_events.csv` (Eventos Dinâmicos & Posicionamento)")
            report.append("Dados em nível de evento com marcação temporal, posições (x, y), velocidade, aceleração e contexto de posse de bola.")
            report.append("| Coluna | Tipo de Dado |")
            report.append("| :--- | :--- |")
            for col, dtype in self.schemas["dynamic_events.csv"].items():
                report.append(f"| `{col}` | `{dtype}` |")
            report.append("")

        if "phases_of_play.csv" in self.schemas:
            report.append("### Schema de `<match_id>_phases_of_play.csv` (Fases do Jogo)")
            report.append("Segmentação tática da partida por fases de ataque, defesa e transições com marcação temporal.")
            report.append("| Coluna | Tipo de Dado |")
            report.append("| :--- | :--- |")
            for col, dtype in self.schemas["phases_of_play.csv"].items():
                report.append(f"| `{col}` | `{dtype}` |")
            report.append("")

        report.append("## 4. Mapeamento de Chaves Primárias (PK) e Estrangeiras (FK)\n")
        report.append("As entidades do modelo de dados da SkillCorner estão conectadas através das seguintes chaves relacionais:\n")
        report.append("| Entidade | Chave Primária (PK) | Chaves Estrangeiras (FK) | Descrição do Relacionamento |")
        report.append("| :--- | :--- | :--- | :--- |")
        report.append("| **Partida (`Match`)** | `match_id` (ou `id`) | `competition_id`, `season_id` | Identifica univocamente uma partida em `matches.json` e no nome das pastas/arquivos de cada jogo. |")
        report.append("| **Jogador (`Player`)** | `player_id` (ou `id`) | `team_id` | Identifica cada atleta em `<match_id>_match.json`, `dynamic_events.csv` e arquivos de agregados físicas/passes. |")
        report.append("| **Equipe (`Team`)** | `team_id` (ou `id`) | - | Conecta partidas, jogadores, eventos dinâmicos e métricas agregadas por clube. |")
        report.append("| **Evento Dinâmico (`DynamicEvent`)** | `event_id` / `frame_start` | `match_id`, `player_id`, `team_id` | Liga eventos específicos no tempo às entidades de atleta, time e partida. |")
        report.append("| **Fase de Jogo (`PhaseOfPlay`)** | `phase_id` / `start_time` | `match_id`, `team_id` | Mapeia trechos temporais da partida para os times em posse/defesa. |\n")

        report.append("## 5. Próximos Passos Recomendados\n")
        report.append("1. **Validação do Schema (Fase 2):** Criar modelos Pydantic na camada `src/domain/entities/` para refletir as entidades `Match`, `Player`, `DynamicEvent` e `PhaseOfPlay` com tipagem forte.")
        report.append("2. **Engenharia de Features:** Desenvolver parsers de Polars para carregar e processar os eventos dinâmicos de forma performática.")
        report.append("3. **Pipeline de Agregação:** Construir conectores na camada `src/use_cases/` para consolidar métricas físicas e táticas por jogador e por equipe.\n")

        content = "\n".join(report)
        out_p.write_text(content, encoding="utf-8")
        return content


def main():
    """Função principal de execução da esteira de descoberta de dados."""
    project_root = Path(__file__).resolve().parents[3]
    opendata_dir = project_root / "data" / "opendata"
    report_output_path = project_root / "reports" / "DATA_STRUCTURE.md"

    print(f"[+] Iniciando descoberta dos dados em: {opendata_dir}")
    parser = SkillCornerDiscoveryParser(data_dir=opendata_dir)
    metrics = parser.run_full_discovery()

    print(f"[+] Estatísticas encontradas:")
    print(f"   - Total de Partidas: {metrics.total_matches}")
    print(f"   - Jogadores Únicos: {len(metrics.unique_players)}")
    print(f"   - Equipes Únicas: {len(metrics.unique_teams)}")
    print(f"   - Registros de Eventos Dinâmicos: {metrics.total_dynamic_events_records:,}")
    print(f"   - Registros de Fases do Jogo: {metrics.total_phases_records:,}")

    print(f"[+] Gerando relatório em: {report_output_path}")
    parser.generate_report(output_path=report_output_path)
    print("[OK] Descoberta e geração de relatório concluídas com sucesso!")


if __name__ == "__main__":
    main()
