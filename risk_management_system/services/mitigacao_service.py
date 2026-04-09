from db_connection import db
from models.mitigacao import Mitigacao

class MitigacaoService:
    @staticmethod
    def criar_mitigacao(mitigacao):
        query = """
        INSERT INTO mitigacao (id_risco, descricao_acao, responsavel, prazo, status_acao)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (mitigacao.id_risco, mitigacao.descricao_acao, mitigacao.responsavel, mitigacao.prazo, mitigacao.status_acao)
        return db.execute_query(query, params)

    @staticmethod
    def listar_mitigacoes(filtro_risco=None, filtro_status=None):
        query = "SELECT * FROM mitigacao"
        params = []
        if filtro_risco:
            query += " WHERE id_risco = %s"
            params.append(filtro_risco)
        if filtro_status:
            if params:
                query += " AND status_acao = %s"
            else:
                query += " WHERE status_acao = %s"
            params.append(filtro_status)
        return db.execute_query(query, tuple(params))

    @staticmethod
    def obter_mitigacao(id_acao):
        query = "SELECT * FROM mitigacao WHERE id_acao = %s"
        result = db.execute_query(query, (id_acao,))
        if result:
            return Mitigacao(**result[0])
        return None

    @staticmethod
    def atualizar_mitigacao(mitigacao):
        query = """
        UPDATE mitigacao SET id_risco = %s, descricao_acao = %s, responsavel = %s, prazo = %s, status_acao = %s
        WHERE id_acao = %s
        """
        params = (mitigacao.id_risco, mitigacao.descricao_acao, mitigacao.responsavel, mitigacao.prazo, mitigacao.status_acao, mitigacao.id_acao)
        return db.execute_query(query, params)

    @staticmethod
    def excluir_mitigacao(id_acao):
        query = "DELETE FROM mitigacao WHERE id_acao = %s"
        return db.execute_query(query, (id_acao,))