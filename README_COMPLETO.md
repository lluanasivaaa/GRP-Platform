# 📊 GRP Platform - Plataforma de Governança e Gestão de Riscos

## 📋 Sumário Executivo

A **GRP Platform** (Governance & Risk Platform) é uma aplicação web de gestão integrada de riscos, projetos e mitigação desenvolvida com tecnologias modernas e arquitetura modular. O sistema foi concebido como projeto de extensão acadêmica para demonstrar competências em desenvolvimento de software, engenharia de sistemas, análise de dados e governança corporativa.

A plataforma oferece um ambiente completo para organizações gerenciarem seus projetos, identificarem riscos associados, calcularem níveis de criticidade, acompanharem mitigações e visualizarem dados estratégicos através de dashboards interativos e relatórios analíticos.

---

## 🎯 Objetivos do Projeto

### Objetivos Gerais
- Desenvolver uma solução escalável e modular para gestão de riscos em ambiente corporativo
- Demonstrar competências em desenvolvimento full-stack com foco em análise e visualização de dados
- Implementar boas práticas de engenharia de software e arquitetura de sistemas

### Objetivos Específicos
1. **Governança de Projetos**: Centralizar o controle de projetos organizacionais com informações de responsáveis, prazos e orçamentos
2. **Análise de Riscos**: Permitir identificação, categorização e análise quantitativa de riscos
3. **Cálculo de Criticidade**: Implementar algoritmos matemáticos para calcular o nível de criticidade baseado em probabilidade e impacto
4. **Gerenciamento de Mitigação**: Rastrear ações de mitigação com responsáveis, prazos e status
5. **Visualização de Dados**: Oferecer dashboards interativos, kanban visual e relatórios exportáveis
6. **Rastreabilidade**: Manter histórico e auditoria de alterações nos projetos e riscos

---

## ✨ Funcionalidades Principais

### 1️⃣ **Dashboard Executivo**
- Visão geral consolidada de todos os projetos e riscos
- Indicadores-chave de performance (KPIs):
  - Total de projetos por status
  - Distribuição de riscos por nível de criticidade
  - Contagem de ações de mitigação ativas
  - Taxa de conclusão de projetos
- Gráficos interativos com Altair para análise visual
- Atualização em tempo real

### 2️⃣ **Gerenciamento de Projetos**
- Criar, editar e visualizar projetos
- Campos principais:
  - Nome do projeto
  - Responsável designado
  - Prazo final
  - Orçamento alocado
  - Status (Backlog, Em Progresso, Concluído, Cancelado)
- Filtros e busca avançada
- Visualização em lista com opções de ação

### 3️⃣ **Matriz de Riscos (Kanban Visual)**
- Visualização Kanban interativa de riscos por status
- Colunas: Identificado → Analisado → Em Mitigação → Mitigado
- Arrastar e soltar (drag-and-drop) para mudança de status
- Indicadores visuais de criticidade (cores por nível: Baixo/Médio/Alto)
- Resumo de riscos por coluna

### 4️⃣ **Gestão de Riscos Detalhada**
- Identificação estruturada de riscos:
  - Descrição do risco
  - Categoria (ex: Técnico, Organizacional, Externo, Financeiro)
  - Probabilidade de ocorrência (Baixa, Média, Alta)
  - Impacto potencial (Baixo, Médio, Alto)
  - Cálculo automático do nível de criticidade
  - Status do risco (Ativo, Mitigado, Aceito)
- Vinculação automática com projetos
- Histórico de alterações

### 5️⃣ **Matriz de Criticidade Risco vs Impacto**
- Visualização em matriz 3x3 (Probabilidade × Impacto)
- Cores representativas dos níveis de criticidade
- Posicionamento automático de riscos na matriz
- Análise visual de concentração de riscos

### 6️⃣ **Plano de Mitigação**
- Criação de ações de mitigação para cada risco
- Campos:
  - Descrição da ação
  - Responsável pela execução
  - Data alvo de implementação
  - Status de progresso (Planejado, Em Execução, Concluído)
  - Efetividade estimada
- Rastreamento de progresso
- Indicadores de status visual

### 7️⃣ **Relatórios Analíticos**
- Múltiplos formatos de relatório:
  - **Relatório de Projetos**: Sumário executivo com estatísticas
  - **Relatório de Riscos**: Análise detalhada de todos os riscos
  - **Relatório de Mitigação**: Ações implementadas e sua efetividade
- Gráficos estatísticos:
  - Distribuição de riscos por categoria
  - Evolução temporal de riscos
  - Status de mitigação
- Exportação em PDF para apresentações e documentação

### 8️⃣ **Visualizações e Gráficos Interativos**
- **Gráficos de Barras**: Contagem de riscos por categoria/status
- **Gráficos de Pizza**: Proporção de projetos por status
- **Gráficos de Scatter**: Probabilidade vs Impacto
- **Heatmaps**: Distribuição de criticidade
- **Tabelas Interativas**: Filtragem e ordenação em tempo real

---

## 🏗️ Arquitetura do Sistema

```
GRP Platform/
├── requirements.txt                # Dependências Python
├── scripts/                        # Utilitários de banco e execução
├── tests/                          # Testes automatizados de sanidade
├── risk_management_system/
│   ├── app.py                      # Configuração e navegação principal
│   ├── db_connection.py            # Gerenciamento de conexão com BD
│   ├── database.sql                # Schema do banco de dados
│   │
│   ├── models/                     # Camada de Modelo de Dados
│   │   ├── projeto.py              # Classe Projeto
│   │   ├── risco.py                # Classe Risco
│   │   └── mitigacao.py            # Classe Mitigação
│   │
│   ├── services/                   # Camada de Lógica de Negócio
│   │   ├── projeto_service.py      # CRUD e lógica de Projetos
│   │   ├── risco_service.py        # CRUD e lógica de Riscos
│   │   └── mitigacao_service.py    # CRUD e lógica de Mitigação
│   │
│   ├── pages/                      # Camada de Interface (Streamlit)
│   │   ├── dashboard.py            # Dashboard executivo
│   │   ├── projetos.py             # Página de gerenciamento de projetos
│   │   ├── riscos.py               # Página de análise de riscos
│   │   ├── kanban.py               # Visualização Kanban
│   │   ├── mitigacao.py            # Página de mitigação
│   │   └── relatorios.py           # Geração de relatórios
│   │
│   └── utils/                      # Utilitários e Funções Auxiliares
│       ├── calculo_risco.py        # Algoritmos de cálculo de criticidade
│       ├── bi_charts.py            # Componentes de gráficos BI
│       ├── projeto_status.py       # Gerenciamento de status de projetos
│       └── ui_components.py        # Componentes reutilizáveis de UI
│
└── README_COMPLETO.md              # Este arquivo
```

### 🔄 Fluxo de Arquitetura

```
Usuário (Interface Streamlit)
    ↓
Páginas (pages/*.py)
    ↓
Services (services/*.py) - Lógica de Negócio
    ↓
Models (models/*.py) - Entidades de Dados
    ↓
DB Connection (db_connection.py) - Acesso a Dados
    ↓
Banco de Dados (SQLite/MySQL)
```

**Padrões de Arquitetura Aplicados:**
- **Model-View-Controller (MVC)**: Separação de modelos, visualização e lógica
- **Service Layer**: Centralização da lógica de negócio
- **Repository Pattern**: Abstração do acesso a dados
- **Single Responsibility Principle**: Cada módulo com responsabilidade única
- **DRY (Don't Repeat Yourself)**: Reutilização de código em utils

---

## 💻 Stack Tecnológico

### Backend
- **Python 3.x**: Linguagem principal
- **Streamlit**: Framework web para interface interativa
- **SQLite**: Banco de dados padrão (leve e portável)
- **MySQL**: Suporte opcional para ambientes produção

### Frontend
- **Streamlit**: Interface responsiva e interativa
- **Altair**: Biblioteca para visualizações interativas
- **CSS/HTML customizado**: Estilização visual

### Dependências Principais
```
streamlit==1.43.0          # Framework web
pandas==2.1.4              # Manipulação de dados
numpy==2.3.4               # Computação numérica
altair==6.0.0              # Visualizações
fpdf==1.7.2                # Geração de PDF
mysql-connector-python==9.6.0  # Suporte MySQL
GitPython==3.1.46          # Controle de versão
```

---

## 📊 Modelo de Dados

### Entidades Principais

#### 1. **Projeto**
```sql
CREATE TABLE projetos (
    id_projeto INT PRIMARY KEY AUTO_INCREMENT,
    nome_projeto VARCHAR(255) NOT NULL,
    responsavel VARCHAR(255),
    prazo_final DATE,
    orcamento DECIMAL(10,2),
    status VARCHAR(50) DEFAULT 'Backlog'
);
```

**Campos:**
- `id_projeto`: Identificador único
- `nome_projeto`: Nome descritivo do projeto
- `responsavel`: Pessoa responsável
- `prazo_final`: Data limite de conclusão
- `orcamento`: Valor alocado em reais
- `status`: Backlog, Em Progresso, Concluído, Cancelado

#### 2. **Risco**
```sql
CREATE TABLE riscos (
    id_risco INT PRIMARY KEY AUTO_INCREMENT,
    id_projeto INT NOT NULL,
    descricao TEXT,
    categoria VARCHAR(100),
    probabilidade VARCHAR(20),
    impacto VARCHAR(20),
    nivel_criticidade VARCHAR(20),
    status_risco VARCHAR(50) DEFAULT 'Ativo',
    FOREIGN KEY (id_projeto) REFERENCES projetos(id_projeto)
);
```

**Campos:**
- `id_risco`: Identificador único
- `id_projeto`: Referência ao projeto
- `descricao`: Descrição detalhada do risco
- `categoria`: Tipo de risco (Técnico, Organizacional, etc)
- `probabilidade`: Baixa, Média, Alta
- `impacto`: Baixo, Médio, Alto
- `nivel_criticidade`: Calculado automaticamente (Baixo/Médio/Alto)
- `status_risco`: Ativo, Mitigado, Aceito

#### 3. **Mitigação**
```sql
CREATE TABLE mitigacoes (
    id_mitigacao INT PRIMARY KEY AUTO_INCREMENT,
    id_risco INT NOT NULL,
    descricao_acao TEXT,
    responsavel VARCHAR(255),
    data_alvo DATE,
    status_mitigacao VARCHAR(50),
    efetividade DECIMAL(3,2),
    FOREIGN KEY (id_risco) REFERENCES riscos(id_risco)
);
```

**Campos:**
- `id_mitigacao`: Identificador único
- `id_risco`: Referência ao risco
- `descricao_acao`: O que será feito para mitigar
- `responsavel`: Responsável pela execução
- `data_alvo`: Quando a ação deve estar completa
- `status_mitigacao`: Planejado, Em Execução, Concluído
- `efetividade`: Percentual esperado de redução do risco (0-1)

### Relacionamentos
```
Projeto (1) -----> (N) Risco
  ↓                  ↓
  |                  └─→ (1) Mitigação
  |
  └─ Responsável do Projeto
     Responsável da Mitigação
```

---

## 🧮 Algoritmo de Cálculo de Criticidade

### Fórmula Matemática

O nível de criticidade é calculado multiplicando a probabilidade pelo impacto em uma escala de 1 a 3:

$$\text{Score de Risco} = \text{Probabilidade} \times \text{Impacto}$$

Onde:
- **Probabilidade**: Baixa=1, Média=2, Alta=3
- **Impacto**: Baixo=1, Médio=2, Alto=3

### Matriz de Criticidade

|  | Impacto Baixo (1) | Impacto Médio (2) | Impacto Alto (3) |
|---|---|---|---|
| **Prob. Baixa (1)** | **Baixo (1)** | **Médio (2)** | **Médio (3)** |
| **Prob. Média (2)** | **Médio (2)** | **Médio (4)** | **Alto (6)** |
| **Prob. Alta (3)** | **Médio (3)** | **Alto (6)** | **Alto (9)** |

### Classificação Final
- **Baixo**: Score 1-2
- **Médio**: Score 3-4
- **Alto**: Score 6-9

**Implementação:**
```python
def calcular_score_risco(probabilidade, impacto):
    prob_scores = {"baixa": 1, "média": 2, "alta": 3}
    impact_scores = {"baixo": 1, "médio": 2, "alto": 3}
    
    prob_value = prob_scores.get(probabilidade.lower(), 1)
    impact_value = impact_scores.get(impacto.lower(), 1)
    
    score = prob_value * impact_value
    
    if score <= 2:
        return "Baixo"
    elif score <= 4:
        return "Médio"
    else:
        return "Alto"
```

---

## 🚀 Como Instalar e Executar

### Pré-requisitos
- **Python 3.11+** instalado
- **Git** para controle de versão
- **pip** (gerenciador de pacotes Python)
- **Windows, macOS ou Linux**

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/lluanasivaaa/GRP-Platform.git
cd GRP-Platform
```

### Passo 2: Criar Ambiente Virtual

#### Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se receber erro de política de execução:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

#### macOS/Linux (Bash):
```bash
python -m venv .venv
source .venv/bin/activate
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Executar a Aplicação

#### Opção A - Streamlit direto:
```bash
streamlit run risk_management_system/app.py
```

A aplicação abrirá automaticamente em `http://localhost:8501`

### Passo 5: Configurar Banco de Dados (Opcional)

**Padrão - SQLite Local:**
O sistema utiliza SQLite por padrão e o arquivo padrão é `risk_management_system/risk_management.db`.

Para gerar dados de demonstração no SQLite local:

```bash
python scripts/populate_db.py
```

**Alternativa - MySQL:**
Defina as variáveis de ambiente:

```powershell
# Windows
$env:DB_ENGINE = "mysql"
$env:DB_HOST = "localhost"
$env:DB_PORT = "3306"
$env:DB_USER = "root"
$env:DB_PASSWORD = "senha"
$env:DB_NAME = "grp_platform"
```

```bash
# Linux/macOS
export DB_ENGINE=mysql
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=senha
export DB_NAME=grp_platform
```

---

## 📖 Guia de Uso

### 1. **Acessar o Dashboard**
- Página inicial com visão geral dos projetos e riscos
- Indicadores principais e gráficos interativos
- Navegação através do menu lateral

### 2. **Criar um Novo Projeto**
1. Clique em "Projetos" no menu lateral
2. Clique em "➕ Novo Projeto"
3. Preencha os campos:
   - Nome do projeto
   - Responsável
   - Prazo final
   - Orçamento
   - Status inicial
4. Clique em "Salvar Projeto"

### 3. **Identificar um Risco**
1. Acesse "Riscos" → "Novo Risco"
2. Selecione o projeto associado
3. Descreva o risco
4. Defina:
   - Categoria
   - Probabilidade
   - Impacto
5. O sistema calcula automaticamente o nível de criticidade
6. Clique em "Salvar Risco"

### 4. **Visualizar em Kanban**
1. Acesse "Kanban" no menu
2. Visualize riscos organizados por status
3. Arraste e solte para mudança de status
4. Clique em um risco para editar

### 5. **Criar Plano de Mitigação**
1. Em "Mitigação", selecione o risco
2. Clique em "Adicionar Ação"
3. Descreva a ação de mitigação
4. Defina responsável e data alvo
5. Acompanhe o progresso

### 6. **Gerar Relatórios**
1. Acesse "Relatórios" no menu
2. Escolha o tipo de relatório:
   - Projetos
   - Riscos
   - Mitigação
3. Clique em "Gerar Relatório"
4. Visualize ou exporte em PDF

### 7. **Analisar Matriz de Risco**
1. Em "Riscos", visualize a "Matriz de Probabilidade vs Impacto"
2. Identifique riscos de alta criticidade
3. Priorize ações baseado na posição na matriz

---

## 🔧 Funcionalidades Técnicas Avançadas

### 1. **Validação de Dados**
- Validação de entrada em tempo real
- Verificação de integridade referencial
- Tratamento de exceções

### 2. **Segurança**
- Prepared statements para prevenção de SQL Injection
- Validação de entradas do usuário
- Isolamento de ambiente

### 3. **Performance**
- Cache de consultas frequentes
- Indexação de banco de dados
- Otimização de queries SQL

### 4. **Rastreabilidade**
- Registro de criação e modificação
- Histórico de alterações de status
- Auditoria de ações críticas

### 5. **Escalabilidade**
- Arquitetura modular facilitando expansão
- Suporte para múltiplos usuários
- Possibilidade de integração com sistemas externos

---

## 📈 Indicadores e Métricas

### Métricas de Projeto
- **Total de Projetos**: Contagem absoluta
- **Por Status**: Distribuição em cada estágio
- **Taxa de Conclusão**: % de projetos concluídos
- **Orçamento Total**: Soma de investimentos

### Métricas de Risco
- **Total de Riscos Identificados**: Contagem absoluta
- **Distribuição por Criticidade**: Baixo/Médio/Alto
- **Riscos Mitigados**: % de riscos resolvidos
- **Risco Residual**: Risco remanescente após mitigação

### Métricas de Efetividade
- **Ações de Mitigação Concluídas**: % de progresso
- **Efetividade Média**: Média ponderada de efetividade
- **Redução de Risco**: Impacto das ações implementadas

---

## 🎓 Conceitos de Governança e Gestão de Riscos

### Governança
A plataforma implementa princípios de governança corporativa:
- **Centralização**: Todos os dados em um único ponto de acesso
- **Transparência**: Visibilidade completa de projetos e riscos
- **Accountability**: Designação clara de responsáveis
- **Conformidade**: Rastreabilidade para auditoria

### Gestão de Riscos (Framework COSO)
Segue metodologia COSO (Committee of Sponsoring Organizations):
1. **Identificação**: Reconhecer riscos potenciais
2. **Análise**: Avaliar probabilidade e impacto
3. **Resposta**: Definir estratégias de mitigação
4. **Monitoramento**: Acompanhar efetividade das ações
5. **Comunicação**: Reportar status para stakeholders

---

## 🧪 Testes e Validação

### Cenários de Teste Cobertos
- ✅ CRUD completo de Projetos
- ✅ CRUD completo de Riscos
- ✅ CRUD completo de Mitigação
- ✅ Cálculo correto de criticidade
- ✅ Mudança de status em Kanban
- ✅ Geração de relatórios
- ✅ Validações de entrada
- ✅ Integridade referencial

### Dados de Teste
O sistema inclui scripts para população com dados de exemplo para demonstração de funcionalidades.

---

## 📋 Requisitos Não-Funcionais

### Performance
- Resposta de consultas < 2 segundos
- Suporte para 10.000+ registros
- Interface responsiva

### Disponibilidade
- Funcionamento 24/7
- Modo offline com SQLite
- Sincronização com MySQL quando disponível

### Usabilidade
- Interface intuitiva com Streamlit
- Navegação clara e lógica
- Feedback visual de ações
- Atalhos e automatizações

### Manutenibilidade
- Código modular e bem documentado
- Logging de operações críticas
- Fácil identificação de bugs

### Escalabilidade
- Arquitetura preparada para crescimento
- Suporte para múltiplos usuários simultâneos
- Banco de dados escalável

---

## 🤝 Como Contribuir

Para contribuir com melhorias ao projeto:

1. **Fork** o repositório
2. **Clone** em sua máquina local
3. **Crie uma branch** para sua feature:
   ```bash
   git checkout -b feature/MeuFeature
   ```
4. **Realize suas mudanças** com commits descritivos
5. **Push** para sua branch
   ```bash
   git push origin feature/MeuFeature
   ```
6. **Abra um Pull Request** descrevendo suas mudanças

### Padrões de Código
- Nomes em inglês para variáveis e funções
- Comentários descritivos em português
- Seguir PEP 8 para Python
- Adicionar docstrings em métodos públicos

---

## 📝 Estrutura de Commits

```
feat: adicionar nova funcionalidade
fix: corrigir bug
docs: atualizar documentação
style: mudanças de formatação
refactor: reestruturar código
test: adicionar testes
chore: tarefas de manutenção
```

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError"
**Solução**: Ative o ambiente virtual e instale dependências
```bash
pip install -r requirements.txt
```

### Erro: "Port 8501 is already in use"
**Solução**: Execute em porta diferente
```bash
streamlit run risk_management_system/app.py --server.port 8502
```

### Erro: "Database Connection Failed"
**Solução**: Verifique se SQLite está criado ou configure MySQL corretamente

### Erro: "Permission Denied (PowerShell)"
**Solução**: Execute o comando de policy:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

## 📊 Roadmap Futuro

### Phase 2 - Enhancements
- [ ] Autenticação de usuários
- [ ] Histórico de auditoria completo
- [ ] Análise preditiva com ML
- [ ] Integração com APIs externas
- [ ] Notificações automáticas

### Phase 3 - Enterprise
- [ ] Suporte a múltiplas organizações
- [ ] Gestão de permissões por role
- [ ] Dashboard mobile responsivo
- [ ] Integração LDAP/Active Directory
- [ ] SLA e alertas em tempo real

### Phase 4 - Advanced Analytics
- [ ] Análise de tendências históricas
- [ ] Simulação de cenários
- [ ] Matriz de correlação de riscos
- [ ] Análise de causa-raiz automatizada
- [ ] Dashboards customizáveis por usuário

---

## 📞 Suporte e Contato

Para dúvidas, sugestões ou relato de bugs:
- **GitHub Issues**: https://github.com/lluanasivaaa/GRP-Platform/issues
- **Email**: lluanasivaaa@gmail.com

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## ✍️ Autores

**Luana Silva**
- Desenvolvedora Principal
- Arquitetura e Implementação
- GitHub: [@lluanasivaaa](https://github.com/lluanasivaaa)

**Projeto de Extensão Acadêmica**
- Instituição: [Sua Faculdade]
- Período: [Data Início - Data Fim]
- Orientador(es): [Nome do Orientador]

---

## 🙏 Agradecimentos

- Streamlit pela excelente framework
- Comunidade Python por bibliotecas robustas
- Professores e orientadores pelo suporte acadêmico
- Testadores e usuários por feedback valioso

---

## 📚 Referências

### Frameworks e Bibliotecas
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Altair Documentation](https://altair-viz.github.io/)

### Conceitos de Gestão de Riscos
- COSO Framework - Enterprise Risk Management
- ISO 31000 - Risk Management
- PMBOK - Project Management Body of Knowledge

### Arquitetura de Software
- Clean Architecture
- Hexagonal Architecture
- MVC Pattern
- Repository Pattern

---

## 📊 Estatísticas do Projeto

- **Linhas de Código**: 2000+
- **Módulos**: 12
- **Funcionalidades Principais**: 8
- **Tecnologias**: 10+
- **Tempo de Desenvolvimento**: [Seu tempo]

---

## 🔐 Segurança

Este é um projeto educacional. Para uso em produção, considere:
- Implementar autenticação
- Adicionar criptografia de dados sensíveis
- Configurar HTTPS
- Realizar testes de segurança
- Implementar logging de auditoria completo

---

## ❓ Perguntas Frequentes

**P: Posso usar este código em produção?**
R: O código é educacional. Para produção, realize security audits e testes rigorosos.

**P: Como faço backup do banco de dados?**
R: Com SQLite, copie o arquivo `.db`. Com MySQL, use ferramentas nativas de backup.

**P: É possível customizar as cores e temas?**
R: Sim, os estilos CSS estão em `app.py` e podem ser modificados.

**P: Como escalar para muitos usuários?**
R: Migre para MySQL/PostgreSQL e implemente cache e otimizações.

---

## 📅 Changelog

### Versão 1.0.0 (Data)
- ✅ Release inicial
- ✅ Todas as funcionalidades core implementadas
- ✅ Banco de dados SQLite
- ✅ Interface Streamlit completa

---

## 🎯 Conclusão

A **GRP Platform** demonstra aplicação prática de conceitos de engenharia de software, governança corporativa e análise de dados em um projeto real e funcional. O sistema oferece uma solução robusta, escalável e educacional para gestão de riscos e projetos organizacionais.

Desenvolvido com foco em excelência técnica, usabilidade e extensibilidade, o projeto representa um case study completo de desenvolvimento de aplicação web profissional em ambiente acadêmico.

---

**Última Atualização:** 02 de Junho de 2026  
**Status:** ✅ Ativo e em Desenvolvimento  
**Versão:** 1.0.0

