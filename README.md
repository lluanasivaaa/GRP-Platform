# GRP Platform

Aplicação de gestão de riscos, projetos, kanban, mitigação e relatórios desenvolvida em Streamlit.

## Visão geral
- Interface interativa com navegação por dashboard, projetos, kanban, riscos, mitigação e relatórios.
- Suporte para banco de dados local via SQLite e conexão opcional com MySQL.
- Estrutura modular com `risk_management_system/pages`, `services`, `models` e `utils`.

## Execução local
1. Abra um terminal na pasta do projeto.
2. Ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell impedir execução de scripts, habilite com:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

3. Instale as dependências:

```powershell
pip install -r requirements.txt
```

4. Execute o app:

```powershell
python app.py
```

Ou use o comando Streamlit diretamente:

```powershell
streamlit run risk_management_system/app.py
```

## Banco de dados
Por padrão, o app utiliza SQLite local para facilitar a execução em ambiente de avaliação.

Para usar SQLite:

- `DB_ENGINE=sqlite`
- `DB_SQLITE_PATH=risk_management.db`

Para usar MySQL, defina as variáveis de ambiente:

- `DB_ENGINE=mysql`
- `DB_HOST=<HOST>`
- `DB_PORT=<PORT>`
- `DB_USER=<USERNAME>`
- `DB_PASSWORD=<PASSWORD>`
- `DB_NAME=<DATABASE_NAME>`

## Detalhes importantes
- O esquema de tabelas é gerado automaticamente ao iniciar o app.
- Este repositório não contém credenciais ou dados sensíveis.
- Arquivos locais e de ambiente estão listados em `.gitignore`.

## Estrutura do repositório
- `app.py`: ponto de entrada raiz para execução do projeto.
- `requirements.txt`: dependências do Python.
- `risk_management_system/`: código principal da aplicação.
- `README.md`: documentação do projeto.
- `.gitignore`: regras de exclusão de arquivos locais.
