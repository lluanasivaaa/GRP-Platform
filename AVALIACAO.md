# 📋 Guia para Avaliação do Projeto

Este documento orienta o avaliador sobre os principais pontos a verificar no projeto GRP Platform.

## 🎯 Objetivos do Projeto

A plataforma foi desenvolvida como projeto de extensão acadêmica com os seguintes objetivos:

1. **Governança de Projetos**: Centralizar controle de projetos com informações de responsáveis, prazos e orçamentos
2. **Análise de Riscos**: Permitir identificação, categorização e cálculo de criticidade
3. **Gestão de Mitigação**: Rastrear ações de mitigação com responsáveis e prazos
4. **Visualização de Dados**: Oferecer dashboards e relatórios para tomada de decisão

## 🚀 Como Executar e Testar

### Setup (5 minutos)
```bash
# 1. Clonar o repositório
git clone https://github.com/lluanasivaaa/GRP-Platform.git
cd GRP-Platform

# 2. Criar ambiente virtual
python -m venv .venv
.venv\Scripts\Activate  # Windows ou source .venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar
streamlit run risk_management_system/app.py
```

Acesse em `http://localhost:8501`

### Cenários de Teste Recomendados

#### 1️⃣ Criar um Projeto (2 min)
- Menu: **Projetos** → **+ Novo Projeto**
- Preencher: Nome, Responsável, Prazo, Orçamento
- Verificar: Projeto aparece na lista
- **Resultado esperado**: ✅ CRUD funcional

#### 2️⃣ Adicionar Riscos (3 min)
- Menu: **Riscos** → **+ Novo Risco**
- Selecionar projeto criado
- Preenchher: Descrição, Categoria, Probabilidade, Impacto
- **Verificar**: Nível de criticidade calculado automaticamente
- **Resultado esperado**: ✅ Cálculo correto (Prob × Impacto)

#### 3️⃣ Testar Cálculo de Criticidade (1 min)
Testar várias combinações e verificar fórmula:
- Baixa × Baixo = Baixo (1)
- Média × Média = Médio (4)
- Alta × Alto = Alto (9)

**Resultado esperado**: ✅ Algoritmo implementado corretamente

#### 4️⃣ Usar Kanban (2 min)
- Menu: **Kanban**
- Arrastar riscos entre colunas (Identificado → Analisado → Em Mitigação → Mitigado)
- **Resultado esperado**: ✅ Drag-and-drop funcionando

#### 5️⃣ Criar Plano de Mitigação (2 min)
- Menu: **Mitigação**
- Selecionar um risco
- **+ Adicionar Ação**
- Preencher descrição, responsável, data alvo
- **Resultado esperado**: ✅ Ação registrada e persistida

#### 6️⃣ Gerar Relatório (1 min)
- Menu: **Relatórios**
- Escolher tipo (Projetos, Riscos, Mitigação)
- **Gerar Relatório**
- **Resultado esperado**: ✅ PDF gerado com dados

#### 7️⃣ Explorar Dashboard (2 min)
- Menu: **Dashboard**
- Verificar KPIs e gráficos
- **Resultado esperado**: ✅ Dados atualizados em tempo real

## ✅ Checklist de Avaliação

### Funcionalidades Core
- [ ] Dashboard com KPIs funcionando
- [ ] CRUD de Projetos completo
- [ ] CRUD de Riscos com categorização
- [ ] Cálculo automático de criticidade correto
- [ ] Kanban com drag-and-drop
- [ ] CRUD de Mitigação
- [ ] Geração de relatórios em PDF
- [ ] Gráficos interativos com dados

### Arquitetura e Código
- [ ] Estrutura modular (models, services, pages, utils)
- [ ] Separação de responsabilidades clara
- [ ] Padrão MVC/Service Layer implementado
- [ ] Código legível e bem organizado
- [ ] Conexão com banco de dados funcional

### Qualidade
- [ ] Sem crashes ou erros não tratados
- [ ] Validação de entrada
- [ ] Tratamento de exceções
- [ ] Dados persistem após reload

### Documentação
- [ ] README.md claro e prático
- [ ] README_COMPLETO.md com documentação detalhada
- [ ] Modelo de dados documentado
- [ ] Algoritmo de criticidade explicado
- [ ] Padrões de arquitetura descritos

## 🧮 Verificação do Algoritmo

### Fórmula Matemática
$$\text{Criticidade} = \text{Probabilidade} \times \text{Impacto}$$

### Tabela de Referência
| Probabilidade | Impacto Baixo | Impacto Médio | Impacto Alto |
|---|---|---|---|
| **Baixa** | Baixo (1) | Médio (2) | Médio (3) |
| **Média** | Médio (2) | Médio (4) | Alto (6) |
| **Alta** | Médio (3) | Alto (6) | Alto (9) |

**Testes recomendados:**
1. Baixa + Baixo = 1 → Baixo
2. Média + Média = 4 → Médio
3. Alta + Alto = 9 → Alto

## 📊 Dados de Teste Sugeridos

### Projeto Exemplo
- Nome: "Implementação ERP"
- Responsável: "João Silva"
- Prazo: 30/09/2026
- Orçamento: R$ 50.000,00

### Riscos Exemplo
1. **Risco Alto**
   - Descrição: "Atraso na implementação"
   - Categoria: Técnico
   - Probabilidade: Alta
   - Impacto: Alto
   - Esperado: Criticidade **Alto (9)**

2. **Risco Médio**
   - Descrição: "Falta de conhecimento técnico"
   - Categoria: Organizacional
   - Probabilidade: Média
   - Impacto: Médio
   - Esperado: Criticidade **Médio (4)**

3. **Risco Baixo**
   - Descrição: "Conexão com internet instável"
   - Categoria: Infraestrutura
   - Probabilidade: Baixa
   - Impacto: Baixo
   - Esperado: Criticidade **Baixo (1)**

## 🔍 Pontos Importantes

### O que Funciona Bem
✅ Interface intuitiva com Streamlit  
✅ Cálculo automático de criticidade implementado  
✅ Banco de dados funcional (SQLite padrão)  
✅ Múltiplas visualizações de dados  
✅ Arquitetura modular e escalável  

### Limitações Conhecidas
- Não tem autenticação (ambiente acadêmico)
- SQLite é local (sem multi-usuário simultâneo)
- Relatórios básicos (sem gráficos em PDF)

## 💡 Recomendações para Melhorias Futuras

1. **Autenticação**: Implementar login de usuários
2. **Histórico de Auditoria**: Rastrear mudanças de usuários
3. **Alertas**: Notificações de prazos vencidos
4. **API REST**: Para integração com outros sistemas
5. **Análise Preditiva**: Machine Learning para previsão de riscos

## 📞 Suporte Durante Avaliação

Se tiver dúvidas sobre funcionamento:
- Consulte [README.md](README.md) para instruções rápidas
- Veja [README_COMPLETO.md](README_COMPLETO.md) para detalhes técnicos
- Código bem comentado em cada módulo

## ⏱️ Tempo Estimado para Avaliação

- Setup: 5 min
- Testes de funcionalidade: 15 min
- Análise de código: 10 min
- **Total: ~30 minutos**

---

**Data**: 02 de Junho de 2026  
**Desenvolvedor**: Luana Silva  
**Repositório**: https://github.com/lluanasivaaa/GRP-Platform
