from db_connection import db
from models.projeto import Projeto


class ProjetoService:
    BASE_COLUMNS = "id_projeto, nome_projeto, responsavel, prazo_final, orcamento, status"

    @staticmethod
    def criar_projeto(projeto):
        query = """
        INSERT INTO projetos (nome_projeto, responsavel, prazo_final, orcamento, status)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            projeto.nome_projeto,
            projeto.responsavel,
            projeto.prazo_final,
            projeto.orcamento,
            projeto.status,
        )
        return db.execute_query(query, params)

    @staticmethod
    def listar_projetos(filtro_status=None):
        query = f"SELECT {ProjetoService.BASE_COLUMNS} FROM projetos"
        params = ()
        if filtro_status:
            query += " WHERE status = %s"
            params = (filtro_status,)
        return db.execute_query(query, params)

    @staticmethod
    def obter_projeto(id_projeto):
        query = f"SELECT {ProjetoService.BASE_COLUMNS} FROM projetos WHERE id_projeto = %s"
        result = db.execute_query(query, (id_projeto,))
        if result:
            return Projeto(**result[0])
        return None

    @staticmethod
    def atualizar_projeto(projeto):
        query = """
        UPDATE projetos SET nome_projeto = %s, responsavel = %s, prazo_final = %s, orcamento = %s, status = %s
        WHERE id_projeto = %s
        """
        params = (
            projeto.nome_projeto,
            projeto.responsavel,
            projeto.prazo_final,
            projeto.orcamento,
            projeto.status,
            projeto.id_projeto,
        )
        return db.execute_query(query, params)

    @staticmethod
    def excluir_projeto(id_projeto):
        query = "DELETE FROM projetos WHERE id_projeto = %s"
        return db.execute_query(query, (id_projeto,))
