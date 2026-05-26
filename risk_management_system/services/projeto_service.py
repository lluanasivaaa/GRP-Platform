from db_connection import db
from models.projeto import Projeto
from utils.projeto_status import PROJECT_STATUS_OPTIONS, normalize_project_status


class ProjetoService:
    BASE_COLUMNS = "id_projeto, nome_projeto, responsavel, prazo_final, orcamento, status"
    _schema_checked = False

    @staticmethod
    def garantir_fluxo_kanban():
        if ProjetoService._schema_checked:
            return

        column_info = db.execute_query("SHOW COLUMNS FROM projetos LIKE 'status'") or []
        if not column_info:
            ProjetoService._schema_checked = True
            return

        column_type = str(column_info[0].get("Type", "")).lower()

        if column_type.startswith("enum("):
            allowed_values = {value.strip("'") for value in column_type[5:-1].split(",")}
            desired_values = {"ativo", *(value.lower() for value in PROJECT_STATUS_OPTIONS)}
            if not desired_values.issubset(allowed_values):
                enum_values = "', '".join(["Ativo", *PROJECT_STATUS_OPTIONS])
                db.execute_query(
                    f"""
                    ALTER TABLE projetos
                    MODIFY COLUMN status ENUM('{enum_values}') NOT NULL DEFAULT 'Backlog'
                    """
                )

        db.execute_query("UPDATE projetos SET status = 'Backlog' WHERE status = 'Ativo'")
        ProjetoService._schema_checked = True

    @staticmethod
    def criar_projeto(projeto):
        ProjetoService.garantir_fluxo_kanban()
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
        ProjetoService.garantir_fluxo_kanban()
        query = f"SELECT {ProjetoService.BASE_COLUMNS} FROM projetos"
        params = ()
        if filtro_status:
            query += " WHERE status = %s"
            params = (filtro_status,)
        projetos = db.execute_query(query, params) or []
        for projeto in projetos:
            projeto["status"] = normalize_project_status(projeto.get("status"))
        return projetos

    @staticmethod
    def obter_projeto(id_projeto):
        ProjetoService.garantir_fluxo_kanban()
        query = f"SELECT {ProjetoService.BASE_COLUMNS} FROM projetos WHERE id_projeto = %s"
        result = db.execute_query(query, (id_projeto,))
        if result:
            result[0]["status"] = normalize_project_status(result[0].get("status"))
            return Projeto(**result[0])
        return None

    @staticmethod
    def atualizar_projeto(projeto):
        ProjetoService.garantir_fluxo_kanban()
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
        ProjetoService.garantir_fluxo_kanban()
        query = "DELETE FROM projetos WHERE id_projeto = %s"
        return db.execute_query(query, (id_projeto,))
