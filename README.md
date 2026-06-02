# GRP Platform

Este repositório contém o app Streamlit de gestão de riscos (`risk_management_system/app.py`).

## Execução local
1. Abra o terminal em `c:\Users\luana\Desktop\GRP Plataform`.
2. Ative o ambiente virtual:

```powershell
cd "C:\Users\luana\Desktop\GRP Plataform"
.\.venv\Scripts\Activate.ps1
```

Se aparecer erro de execução de scripts, execute apenas uma vez como administrador:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

3. Execute o app:

```powershell
cd risk_management_system
streamlit run app.py
```

4. O app usa MySQL local por padrão com as variáveis:

- `DB_ENGINE=mysql`
- `DB_HOST=127.0.0.1`
- `DB_PORT=3306`
- `DB_USER=root`
- `DB_PASSWORD=2005`
- `DB_NAME=risk_management`

Se quiser rodar localmente com SQLite, defina `DB_ENGINE=sqlite` e opcionalmente `DB_SQLITE_PATH=risk_management.db`.

## Executando localmente
1. Ative o ambiente virtual:

```powershell
cd "C:\Users\luana\Desktop\GRP Plataform"
.\.venv\Scripts\Activate.ps1
```

2. Execute o app (a partir da raiz):

```powershell
python app.py
```

Ou, se preferir, execute diretamente o Streamlit no app:

```powershell
cd risk_management_system
streamlit run app.py
```

## Deploy no Streamlit Cloud
Para publicar no Streamlit Cloud e usar o mesmo banco de dados, você precisa de um MySQL acessível a partir da nuvem.

No painel do Streamlit, configure Secrets com as chaves:

```toml
DB_ENGINE = "mysql"
DB_HOST = "<HOST>"
DB_PORT = "3306"
DB_USER = "<USERNAME>"
DB_PASSWORD = "<PASSWORD>"
DB_NAME = "<DATABASE_NAME>"
```

> Atenção: `localhost` não funciona no Streamlit Cloud. O banco deve estar em um host público ou em um túnel TCP exposto.

## Observações
- O app local já foi testado e conecta ao MySQL local.
- Se desejar usar o banco local no deploy, é preciso criar um MySQL remoto ou usar um túnel público (por exemplo, `ngrok tcp 3306`).
- O código atual mantém a estrutura do app e a lógica existente, usando conexão MySQL conforme antes.
