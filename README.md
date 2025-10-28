# ⚽ PySport x SkillCorner Analytics Cup — Analyst Track

## 🧠 Visão Geral

Este projeto foi desenvolvido para a **PySport / SkillCorner Analytics Cup**, na trilha **Analyst Track** — cujo objetivo é criar ferramentas e visualizações que auxiliem **treinadores, analistas e equipes técnicas** a compreenderem de forma mais profunda as **qualidades e fraquezas de atletas e times**, utilizando dados abertos da SkillCorner.

A ideia principal é permitir que profissionais do futebol explorem, de forma intuitiva e interativa, **como diferentes atletas se comportam em campo**, revelando padrões táticos e insights de performance que podem apoiar a tomada de decisão.

---

## 🎯 Objetivos

- Criar **ferramentas visuais interativas** para exploração de dados esportivos.  
- Ajudar treinadores a **entender o perfil tático e físico** de seus atletas e adversários.  
- Demonstrar habilidades práticas em **ciência de dados aplicada ao futebol**, desde a coleta até a visualização.  
- Desenvolver uma base sólida para futuras aplicações em análise de performance esportiva.

---

## 🏗️ Estrutura do Repositório

``` bash
📁 pysport-analytics-cup-analyst/
│
├── README.md <- Este arquivo
├── requirements.txt <- Bibliotecas necessárias
├── submission.ipynb <- Notebook final para submissão
│
├── 📁 notebooks/ <- Notebooks de exploração e prototipagem
│ └── exploration.ipynb
│
├── 📁 utils/ <- Funções auxiliares e scripts de apoio
│ └── utils_data.py
│
└── 📁 data/ <- Dados locais (opcional, pequeno volume)
```

## ⚙️ Como Executar o Projeto

### 1️⃣ Criar o ambiente virtual
```bash
python -m venv .venv
```

### 2️⃣ Ativar o ambiente

- Windows (PowerShell):

```bash
.venv\Scripts\activate
```

- Git Bash / Linux / WSL:

```bash
source .venv/Scripts/activate
```

### 3️⃣ Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Abrir o Jupyter Notebook

```bash
jupyter notebook
```

## 📊 Dados Utilizados

Os dados utilizados são provenientes do repositório público da SkillCorner Open Data:

- [SkillCorner Open Data – Repositório](https://github.com/SkillCorner/opendata)

- Contém arquivos JSON com informações de partidas, eventos e tracking.

## 🧩 Próximos Passos

- [ ] Desenvolver função para carregar dados de eventos por partida

- [ ] Criar visualizações iniciais de comportamento de atletas

- [ ] Explorar estatísticas agregadas de times e competições

- [ ] Desenvolver dashboard interativo (Plotly / Dash / Streamlit)

## 👨‍💻 Autor

**Carlos Vinicius**

Participante da PySport / SkillCorner Analytics Cup — Analyst Track

MBA em Data Science & Artificial Intelligence — FIAP

### Redes Sociais

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/https://www.linkedin.com/in/carlosvini/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/carlosvinicius-ai)