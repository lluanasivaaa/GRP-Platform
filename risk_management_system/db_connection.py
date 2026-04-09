import mysql.connector
from mysql.connector import Error


class DatabaseConnection:
    def __init__(self, host="127.0.0.1", user="root", password="2005", database="risk_management", port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            if self.connection.is_connected():
                print("Conectado ao MySQL")
        except Error as e:
            print("ERRO REAL DO MYSQL:")
            print(e)
            self.connection = None
            raise e

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Desconectado do MySQL")

    def execute_query(self, query, params=None):
        if not self.connection or not self.connection.is_connected():
            self.connect()

        if not self.connection:
            raise Exception("Falha na conexão com o banco")

        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True, buffered=True)
            cursor.execute(query, params or ())

            if cursor.with_rows:
                result = cursor.fetchall()
            else:
                self.connection.commit()
                result = cursor.rowcount

            return result
        except Error as e:
            print("Erro na query:")
            print(e)
            return None
        finally:
            if cursor is not None:
                cursor.close()


db = DatabaseConnection()
