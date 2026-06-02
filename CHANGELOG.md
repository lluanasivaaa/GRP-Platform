# 📝 Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/),
e este projeto segue [Semantic Versioning](https://semver.org/pt-BR/).

## [1.0.0] - 2026-06-02

### ✨ Adicionado
- **Dashboard Executivo**: Visão geral consolidada com KPIs e gráficos interativos
- **Gerenciamento de Projetos**: CRUD completo com campos de nome, responsável, prazo e orçamento
- **Gestão de Riscos Detalhada**: Identificação, categorização e análise de riscos
- **Matriz de Criticidade**: Visualização 3x3 de Probabilidade vs Impacto
- **Matriz Kanban**: Interface visual com drag-and-drop para status de riscos
- **Plano de Mitigação**: Criação e rastreamento de ações de mitigação
- **Relatórios Analíticos**: Geração de relatórios em PDF para projetos, riscos e mitigação
- **Visualizações Interativas**: Gráficos com Altair (barras, pizza, scatter, heatmaps)
- **Suporte a Banco de Dados**: SQLite padrão com opção MySQL
- **Cálculo Automático de Criticidade**: Algoritmo probabilidade × impacto
- **Interface Streamlit**: Layout responsivo com estilização customizada
- **Arquitetura Modular**: Separação em models, services, pages e utils

### 🐛 Corrigido
- Validação de entrada de dados
- Tratamento de exceções em operações de banco de dados
- Sincronização de estado entre componentes

### 📚 Documentação
- README principal com instruções básicas
- README completo com documentação detalhada
- Guia de instalação passo a passo
- Guia de uso de cada funcionalidade
- Documentação de API e modelos de dados
- Exemplos de uso prático

### 🔧 Técnico
- Python 3.8+ com Streamlit 1.43.0
- Pandas 2.1.4 para manipulação de dados
- Altair 6.0.0 para visualizações
- SQLite como banco de dados padrão
- MySQL 9.6.0 como suporte opcional
- Estrutura MVC com camadas service e repository

---

## Versionamento Semântico

Este projeto segue [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Mudanças incompatíveis na API
- **MINOR** (1.X.0): Nova funcionalidade compatível
- **PATCH** (1.0.X): Correção de bug

### Exemplo:
- `1.0.0` → `1.1.0`: Nova feature (feature-compatible)
- `1.1.0` → `1.1.1`: Bug fix
- `1.1.1` → `2.0.0`: Breaking change

---

## Roadmap Futuro

### 📌 Versão 1.1.0 (Q3 2026)
- [ ] Autenticação de usuários
- [ ] Histórico de auditoria completo
- [ ] Notificações automáticas por email
- [ ] Integração com calendário

### 📌 Versão 1.2.0 (Q4 2026)
- [ ] Análise preditiva com Machine Learning
- [ ] Dashboard mobile responsivo
- [ ] API REST para integração
- [ ] Suporte a múltiplas organizações

### 📌 Versão 2.0.0 (2027)
- [ ] Gestão de permissões por role
- [ ] Integração LDAP/Active Directory
- [ ] SLA e alertas em tempo real
- [ ] Análise de tendências históricas
- [ ] Matriz de correlação de riscos

---

## Como Reportar Mudanças

Para relatar bugs ou sugerir novos recursos:
1. Verifique [Issues Abertas](https://github.com/lluanasivaaa/GRP-Platform/issues)
2. Se não encontrar, [Abra uma Nova Issue](https://github.com/lluanasivaaa/GRP-Platform/issues/new)
3. Use template apropriado (bug ou feature)

---

## Política de Lançamento

- Lançamentos estáveis são taggeados com versionamento semântico
- Cada versão tem uma Release Notes associada
- Manutenção de até 2 versões anteriores
- Versão `main` é sempre estável e pronta para produção

---

**Última Atualização:** 02 de Junho de 2026

Veja também: [README.md](README.md) | [CONTRIBUTING.md](CONTRIBUTING.md)
