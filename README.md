# GRP Platform - Plataforma de Governança e Gestão de Riscos

Projeto de Extensão Acadêmica para desenvolvimento de uma aplicação web de gestão integrada de riscos, projetos e mitigação.

## 📌 Visão Geral

A **GRP Platform** é uma solução desenvolvida em Python com Streamlit que oferece funcionalidades completas para gerenciamento de riscos e projetos em ambiente organizacional. A aplicação implementa conceitos de governança corporativa e gestão de riscos, permitindo identificação, análise, mitigação e monitoramento de riscos associados a projetos.

## 🎯 Funcionalidades Principais

| Funcionalidade | Descrição |
|---|---|
| **Dashboard Executivo** | Visão consolidada com KPIs, indicadores e gráficos em tempo real |
| **Gestão de Projetos** | CRUD completo com nome, responsável, prazo e orçamento |
| **Análise de Riscos** | Identificação, categorização e cálculo automático de criticidade |
| **Matriz Kanban** | Visualização com drag-and-drop de riscos por status |
| **Plano de Mitigação** | Rastreamento de ações de mitigação com progresso |
| **Relatórios** | Geração em PDF com análises e estatísticas |
| **Gráficos Interativos** | Visualizações com Altair (barras, pizza, scatter, heatmaps) |

## 🏗️ Arquitetura do Sistema

```
risk_management_system/
├── models/              # Entidades de dados
├── services/            # Lógica de negócio
├── pages/               # Interface Streamlit
├── utils/               # Funções auxiliares
└── app.py               # Aplicação principal
scripts/                 # Utilitários de banco e execução
tests/                   # Testes automatizados de sanidade
```

## 📊 Modelo de Dados

**Projeto**: id, nome, responsável, prazo, orçamento, status  
**Risco**: id, projeto_id, descrição, categoria, probabilidade, impacto, criticidade, status  
**Mitigação**: id, risco_id, ação, responsável, data_alvo, status, efetividade

## 🧮 Cálculo de Criticidade

**Fórmula:** Score = Probabilidade × Impacto (escala 1-3)  
**Classificação:** Baixo (1-2) | Médio (3-4) | Alto (6-9)

## 🚀 Como Executar

### Pré-requisitos
- Python 3.11+
- pip

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/lluanasivaaa/GRP-Platform.git
cd GRP-Platform
```

2. Crie ambiente virtual:
```bash
python -m venv .venv
.venv\Scripts\Activate  # Windows
# ou
source .venv/bin/activate  # Linux/macOS
```

3. Instale dependências:
```bash
pip install -r requirements.txt
```

4. Execute:
```bash
streamlit run risk_management_system/app.py
```

Acesse em `http://localhost:8501`

## 💾 Banco de Dados

**SQLite (padrão)**: usa `risk_management_system/risk_management.db` por padrão, sem configuração necessária  
**MySQL (opcional)**: configure variáveis de ambiente `DB_ENGINE=mysql`, `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`

Para popular o SQLite com dados de demonstração:

```bash
python scripts/populate_db.py
```

## 📚 Documentação Completa

Para documentação detalhada sobre arquitetura, conceitos de governança e guias aprofundados, consulte [README_COMPLETO.md](README_COMPLETO.md).

## 📋 Tecnologias Utilizadas

- Python 3.x | Streamlit | Pandas | Altair | SQLite/MySQL | FPDF

## 📞 Informações

- **Repositório**: https://github.com/lluanasivaaa/GRP-Platform
- **Email**: lluanasivaaa@gmail.com

---

**Última Atualização:** 02 de Junho de 2026
