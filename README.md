# GRP Platform

Projeto de gestão de riscos em Streamlit.

O aplicativo principal está em `risk_management_system/app.py`. O arquivo `app.py` na raiz é um ponto de entrada alternativo que redireciona para o app principal.

## Execução local
1. Abra um terminal na pasta do projeto:

```powershell
cd "C:\Users\luana\Desktop\GRP Plataform"
```

2. Ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Se necessário, permita scripts:

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

Ou:

```powershell
streamlit run risk_management_system/app.py
```

## Configuração do banco de dados
Por padrão, o app usa MySQL local com as variáveis de ambiente:

- `DB_ENGINE=mysql`
- `DB_HOST=127.0.0.1`
- `DB_PORT=3306`
- `DB_USER=root`
- `DB_PASSWORD=2005`
- `DB_NAME=risk_management`

Se preferir usar SQLite local:

- `DB_ENGINE=sqlite`
- `DB_SQLITE_PATH=risk_management.db`

## Observações
- O projeto já cria automaticamente o esquema de tabelas no banco se ele não existir.
- `.venv/`, `__pycache__/`, `risk_management.db`, `risk_management_dump.sql` e `.env` são ignorados pelo Git.
- Para apresentação local, mantenha as variáveis de ambiente com o MySQL local ou use o modo SQLite.
