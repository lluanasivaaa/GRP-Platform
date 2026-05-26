import os

import mysql.connector
from mysql.connector import Error


class DatabaseConnection:
    def __init__(
        self,
        host=None,
        user=None,
        password=None,
        database=None,
        port=None,
    ):
        self.host = host or os.getenv("DB_HOST", "127.0.0.1")
        self.user = user or os.getenv("DB_USER", "root")
        self.password = password if password is not None else os.getenv("DB_PASSWORD", "2005")
        self.database = database or os.getenv("DB_NAME", "risk_management")
        self.port = int(port or os.getenv("DB_PORT", "3306"))
        self.connection = None

    def connect(self):
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
        except Error as exc:
            self.connection = None
            raise RuntimeError(
                f"Não foi possível conectar ao banco MySQL '{self.database}' em {self.host}:{self.port}. "
                "Confira se o MySQL está ativo e se as credenciais estão corretas."
            ) from exc

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
        self.connection = None

    def execute_query(self, query, params=None):
        if not self.connection or not self.connection.is_connected():
            self.connect()

        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True, buffered=True)
            cursor.execute(query, params or ())

            if cursor.with_rows:
                return cursor.fetchall()

            self.connection.commit()
            return cursor.rowcount
        except Error as exc:
            if self.connection and self.connection.is_connected():
                self.connection.rollback()
            raise RuntimeError(f"Erro ao executar consulta no banco: {exc}") from exc
        finally:
            if cursor is not None:
                cursor.close()


db = DatabaseConnection()
