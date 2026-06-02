# 📝 Contribuindo com o Projeto

Este documento descreve como contribuir com melhorias ao projeto GRP Platform.

## 🐛 Reportando Bugs

Encontrou um problema? Abra uma [Issue](https://github.com/lluanasivaaa/GRP-Platform/issues) com os detalhes:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs. atual
- Ambiente (SO, versão Python, etc.)

## ✨ Sugerindo Melhorias

Tem uma ideia? Abra uma Issue descrevendo:
- O que você quer adicionar
- Por que seria útil
- Como funcionaria

## 🔧 Desenvolvendo

### Setup
```bash
git clone https://github.com/lluanasivaaa/GRP-Platform.git
cd GRP-Platform
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Fluxo de Trabalho
1. Crie uma branch: `git checkout -b feature/sua-feature`
2. Faça suas mudanças
3. Teste suas alterações
4. Commit: `git commit -m "feat: descrição"`
5. Push: `git push origin feature/sua-feature`
6. Abra um Pull Request

### Padrões de Código
- Nomes de funções e variáveis em **inglês**
- Comentários e docstrings em **português**
- Siga PEP 8 para Python
- Adicione docstrings em métodos públicos

### Estrutura de Commits
```
feat: adicionar nova funcionalidade
fix: corrigir bug
docs: atualizar documentação
refactor: reorganizar código
```

## ✅ Antes de fazer Pull Request
- Teste suas mudanças
- Não há código não utilizado
- Documentação atualizada se necessário
- Código segue os padrões do projeto

---

Obrigado por contribuir! 🙏
