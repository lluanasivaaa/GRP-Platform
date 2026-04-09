from db_connection import db
from models.risco import Risco
from utils.calculo_risco import calcular_criticidade

class RiscoService:
    @staticmethod
    def criar_risco(risco):
        risco.nivel_criticidade = calcular_criticidade(risco.probabilidade, risco.impacto)
        query = """
        INSERT INTO riscos (id_projeto, descricao, categoria, probabilidade, impacto, nivel_criticidade, status_risco)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (risco.id_projeto, risco.descricao, risco.categoria, risco.probabilidade, risco.impacto, risco.nivel_criticidade, risco.status_risco)
        return db.execute_query(query, params)

    @staticmethod
    def listar_riscos(filtro_projeto=None, filtro_status=None):
        query = "SELECT * FROM riscos"
        params = []
        if filtro_projeto:
            query += " WHERE id_projeto = %s"
            params.append(filtro_projeto)
        if filtro_status:
            if params:
                query += " AND status_risco = %s"
            else:
                query += " WHERE status_risco = %s"
            params.append(filtro_status)
        return db.execute_query(query, tuple(params))

    @staticmethod
    def obter_risco(id_risco):
        query = "SELECT * FROM riscos WHERE id_risco = %s"
        result = db.execute_query(query, (id_risco,))
        if result:
            return Risco(**result[0])
        return None

    @staticmethod
    def atualizar_risco(risco):
        risco.nivel_criticidade = calcular_criticidade(risco.probabilidade, risco.impacto)
        query = """
        UPDATE riscos SET id_projeto = %s, descricao = %s, categoria = %s, probabilidade = %s, impacto = %s, nivel_criticidade = %s, status_risco = %s
        WHERE id_risco = %s
        """
        params = (risco.id_projeto, risco.descricao, risco.categoria, risco.probabilidade, risco.impacto, risco.nivel_criticidade, risco.status_risco, risco.id_risco)
        return db.execute_query(query, params)

    @staticmethod
    def excluir_risco(id_risco):
        query = "DELETE FROM riscos WHERE id_risco = %s"
        return db.execute_query(query, (id_risco,))