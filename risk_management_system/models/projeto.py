class Projeto:
    def __init__(self, id_projeto=None, nome_projeto="", responsavel="", prazo_final="", orcamento=0.0, status="Ativo"):
        self.id_projeto = id_projeto
        self.nome_projeto = nome_projeto
        self.responsavel = responsavel
        self.prazo_final = prazo_final
        self.orcamento = orcamento
        self.status = status

    def to_dict(self):
        return {
            "id_projeto": self.id_projeto,
            "nome_projeto": self.nome_projeto,
            "responsavel": self.responsavel,
            "prazo_final": self.prazo_final,
            "orcamento": self.orcamento,
            "status": self.status,
        }
