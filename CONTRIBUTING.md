# 🤝 Guia de Contribuição

Obrigada por considerar contribuir para a **GRP Platform**! Este documento fornece diretrizes e instruções para contribuir ao projeto.

## 📋 Código de Conduta

Por favor, note que este projeto é lançado com um [Contributor Code of Conduct](CODE_OF_CONDUCT.md). Ao participar deste projeto, você concorda em respeitar seus termos.

## 🚀 Como Contribuir

### Reportando Bugs

Antes de criar um relatório de bug, verifique se o problema já foi relatado. Se você encontrar um bug, abra uma [Nova Issue](https://github.com/lluanasivaaa/GRP-Platform/issues) com os seguintes detalhes:

- **Resumo**: Descrição clara e concisa do bug
- **Passos para Reproduzir**: Instruções específicas para reproduzir o problema
- **Comportamento Esperado**: O que você esperava que acontecesse
- **Comportamento Atual**: O que realmente aconteceu
- **Capturas de Tela/Logs**: Se aplicável
- **Ambiente**: Sistema operacional, versão do Python, etc.

### Sugerindo Melhorias

Se você tem uma ideia para melhorar o projeto:

1. Use um título claro e descritivo
2. Descreva a funcionalidade sugerida em detalhes
3. Explique por que essa melhoria seria útil
4. Liste alguns exemplos de como a funcionalidade funcionaria

### Pull Requests

Siga estes passos para contribuir com código:

#### 1. Fork e Clone
```bash
# Fork o repositório via GitHub UI
git clone https://github.com/SEU-USERNAME/GRP-Platform.git
cd GRP-Platform
```

#### 2. Configure o Ambiente
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
# ou
source .venv/bin/activate      # Linux/macOS

pip install -r requirements.txt
```

#### 3. Crie uma Branch
```bash
git checkout -b feature/sua-feature-descritiva
# ou
git checkout -b fix/seu-bug-fix
```

**Padrão de Nomenclatura de Branches:**
- `feature/nome-da-feature` - Para novas funcionalidades
- `fix/nome-do-bug` - Para correção de bugs
- `docs/nome-da-doc` - Para documentação
- `refactor/nome-da-refatoracao` - Para refatorações

#### 4. Faça suas Mudanças

Siga os padrões de código do projeto:

```python
# ✅ BOM - Nomes descritivos em inglês, comentários em português
def calcular_criticidade(probabilidade, impacto):
    """
    Calcula o nível de criticidade do risco.
    
    Args:
        probabilidade (str): Nível de probabilidade (Baixa, Média, Alta)
        impacto (str): Nível de impacto (Baixo, Médio, Alto)
    
    Returns:
        str: Nível de criticidade (Baixo, Médio, Alto)
    """
    scores = {"baixa": 1, "média": 2, "alta": 3}
    # Implementação...
    return criticidade

# ❌ RUIM - Nomes confusos, sem documentação
def calc(p, i):
    s = {"b": 1, "m": 2, "a": 3}
    return s.get(p, 1) * s.get(i, 1)
```

#### 5. Teste suas Mudanças

```bash
# Execute testes manuais
streamlit run risk_management_system/app.py

# Verifique sintaxe
python -m py_compile seu_arquivo.py
```

#### 6. Commit com Mensagens Claras

```bash
git add arquivo_modificado.py

git commit -m "feat: adicionar cálculo automático de criticidade

- Implementa algoritmo de probabilidade x impacto
- Adiciona validação de entrada
- Atualiza testes relacionados"
```

**Formato de Commit:**
```
<tipo>(<escopo>): <assunto>

<corpo>

<rodapé>
```

**Tipos:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Mudanças de documentação
- `style`: Formatação de código
- `refactor`: Reestruturação sem mudança de funcionalidade
- `test`: Adição de testes
- `chore`: Tarefas de manutenção

#### 7. Push para sua Fork

```bash
git push origin feature/sua-feature-descritiva
```

#### 8. Abra um Pull Request

No GitHub, clique em "New Pull Request" e forneça:

- **Título**: Descrição clara (ex: "Add risk criticality calculation")
- **Descrição**: 
  - Motivo das mudanças
  - Como foi testado
  - Screenshots se aplicável
  - Checklist de verificação

```markdown
## Descrição
Adiciona cálculo automático de nível de criticidade para riscos.

## Tipo de Mudança
- [ ] Bug fix (mudança que corrigi um problema)
- [x] Nova feature (mudança que adiciona funcionalidade)
- [ ] Mudança breaking (mudança que quebraria funcionalidade existente)
- [ ] Atualização de documentação

## Como foi testado
- Teste manual com valores baixa/baixo
- Teste manual com valores alta/alto
- Validação de inputs inválidos

## Checklist
- [x] Meu código segue os padrões de estilo do projeto
- [x] Realizei auto-review do meu próprio código
- [x] Adicionei comentários em código complexo
- [x] Atualizei a documentação se necessário
- [x] Minhas mudanças não geram novos warnings
- [x] Adicionei testes que provam meu fix/feature funciona
```

## 🎨 Padrões de Código

### Python
- Seguir [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints quando possível
- Máximo 100 caracteres por linha
- Docstrings em português, código em inglês

### Estrutura de Pastas
```
src/
├── models/           # Entidades de dados
├── services/         # Lógica de negócio
├── pages/           # Interface Streamlit
└── utils/           # Funções auxiliares
```

### Naming Conventions
```python
# Classes - PascalCase
class RiscoAnalyzer:
    pass

# Functions/Methods - snake_case
def calcular_criticidade():
    pass

# Constants - UPPER_SNAKE_CASE
MAX_PROBABILITY = 3
MIN_IMPACT = 1

# Private - leading underscore
def _internal_helper():
    pass
```

## 📚 Estrutura de Documentação

Ao adicionar nova funcionalidade, atualize:
- `README.md` - Se impacta uso geral
- `README_COMPLETO.md` - Se relevante para documentação completa
- Docstrings no código
- Exemplos práticos se aplicável

## 🧪 Testes

Qualidade é importante! Quando possível:
- Adicione testes para nova funcionalidade
- Certifique-se que testes existentes passam
- Teste em diferentes ambientes

## 📝 Documentação

Bom código é autodocumentado, mas documentação é crítica:
- Use comentários para *por quê*, não *como*
- Docstrings para módulos, classes e funções públicas
- Keep examples up-to-date
- Documente decisões arquiteturais importantes

## 🔄 Processo de Review

1. Sempre pelo menos 1 review antes de merge
2. Respostas construtivas esperadas
3. Aprovação depois de mudanças solicitadas
4. Rebase antes de merge quando necessário

## ⚠️ Política de Branches

- `main`: Código estável, pronto para produção
- `develop`: Código em desenvolvimento (se usado)
- `feature/*`: Features em desenvolvimento
- `fix/*`: Bug fixes

Nunca faça push direto para `main`. Sempre use Pull Requests.

## 📞 Dúvidas?

- Abra uma [Discussão](https://github.com/lluanasivaaa/GRP-Platform/discussions)
- Consulte [Issues Abertas](https://github.com/lluanasivaaa/GRP-Platform/issues)
- Email: lluanasivaaa@gmail.com

## ✨ Agradecimentos

Obrigada por contribuir! Todas as contribuições, grandes ou pequenas, ajudam a fazer este projeto melhor. 🙌

---

**Última Atualização:** 02 de Junho de 2026
