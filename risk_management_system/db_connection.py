import os
import sqlite3
from sqlite3 import Error as SQLiteError

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
except ImportError:
    mysql = None
    MySQLError = None


class DatabaseConnection:
    def __init__(
        self,
        host=None,
        user=None,
        password=None,
        database=None,
        port=None,
    ):
        self.engine = os.getenv("DB_ENGINE", "").strip().lower()
        if not self.engine:
            self.engine = "mysql" if mysql is not None else "sqlite"

        self.host = host or os.getenv("DB_HOST", "127.0.0.1")
        self.user = user or os.getenv("DB_USER", "root")
        self.password = password if password is not None else os.getenv("DB_PASSWORD", "2005")
        self.database = database or os.getenv("DB_NAME", "risk_management")
        self.port = int(port or os.getenv("DB_PORT", "3306"))
        self.sqlite_path = os.getenv("DB_SQLITE_PATH", "risk_management.db")
        self.connection = None

    def connect(self):
        if self.engine == "mysql":
            if mysql is None:
                raise RuntimeError(
                    "mysql.connector não está instalado. Instale as dependências ou use DB_ENGINE=sqlite."
                )

            try:
                self.connection = mysql.connector.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    autocommit=False,
                    charset="utf8mb4",
                    use_unicode=True,
                    connection_timeout=8,
                )
            except MySQLError as exc:
                self.connection = None
                raise RuntimeError(
                    f"Não foi possível conectar ao banco MySQL '{self.database}' em {self.host}:{self.port}. "
                    "Confira se o MySQL está ativo e se as credenciais estão corretas."
                ) from exc
        else:
            try:
                self.connection = sqlite3.connect(
                    self.sqlite_path,
                    timeout=8,
                    check_same_thread=False,
                )
                self.connection.row_factory = sqlite3.Row
                self._ensure_sqlite_schema()
            except SQLiteError as exc:
                self.connection = None
                raise RuntimeError(
                    f"Não foi possível abrir o banco SQLite em '{self.sqlite_path}'."
                ) from exc

    def _ensure_sqlite_schema(self):
        cursor = self.connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS projetos (
                id_projeto INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_projeto TEXT NOT NULL,
                responsavel TEXT NOT NULL,
                prazo_final TEXT NOT NULL,
                orcamento REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'Backlog'
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS riscos (
                id_risco INTEGER PRIMARY KEY AUTOINCREMENT,
                id_projeto INTEGER NOT NULL,
                descricao TEXT NOT NULL,
                categoria TEXT NOT NULL,
                probabilidade TEXT NOT NULL,
                impacto TEXT NOT NULL,
                nivel_criticidade TEXT NOT NULL,
                status_risco TEXT NOT NULL DEFAULT 'Ativo',
                FOREIGN KEY (id_projeto) REFERENCES projetos(id_projeto) ON DELETE CASCADE
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS mitigacao (
                id_acao INTEGER PRIMARY KEY AUTOINCREMENT,
                id_risco INTEGER NOT NULL,
                descricao_acao TEXT NOT NULL,
                responsavel TEXT NOT NULL,
                prazo TEXT NOT NULL,
                status_acao TEXT NOT NULL DEFAULT 'Pendente',
                FOREIGN KEY (id_risco) REFERENCES riscos(id_risco) ON DELETE CASCADE
            )
            """
        )
        self.connection.commit()
        cursor.close()

    def disconnect(self):
        if self.connection is None:
            return

        if self.engine == "mysql":
            if self.connection.is_connected():
                self.connection.close()
        else:
            self.connection.close()

        self.connection = None

    def execute_query(self, query, params=None):
        if self.engine == "mysql":
            if not self.connection or not self.connection.is_connected():
                self.connect()
        else:
            if self.connection is None:
                self.connect()

        cursor = None
        try:
            if self.engine == "mysql":
                cursor = self.connection.cursor(dictionary=True, buffered=True)
                cursor.execute(query, params or ())
                if cursor.with_rows:
                    return cursor.fetchall()
                self.connection.commit()
                return cursor.rowcount

            cursor = self.connection.cursor()
            safe_query = query.replace("%s", "?")
            cursor.execute(safe_query, params or ())

            if cursor.description is not None:
                rows = cursor.fetchall()
                return [dict(row) for row in rows]

            self.connection.commit()
            return cursor.rowcount

        except (MySQLError, SQLiteError) as exc:
            if self.connection is not None:
                if self.engine == "mysql" and self.connection.is_connected():
                    self.connection.rollback()
                elif self.engine == "sqlite":
                    self.connection.rollback()
            raise RuntimeError(f"Erro ao executar consulta no banco: {exc}") from exc
        finally:
            if cursor is not None:
                cursor.close()


db = DatabaseConnection()
