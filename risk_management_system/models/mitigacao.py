class Mitigacao:
    def __init__(self, id_acao=None, id_risco=None, descricao_acao='', responsavel='', prazo='', status_acao='Pendente'):
        self.id_acao = id_acao
        self.id_risco = id_risco
        self.descricao_acao = descricao_acao
        self.responsavel = responsavel
        self.prazo = prazo
        self.status_acao = status_acao

    def to_dict(self):
        return {
            'id_acao': self.id_acao,
            'id_risco': self.id_risco,
            'descricao_acao': self.descricao_acao,
            'responsavel': self.responsavel,
            'prazo': self.prazo,
            'status_acao': self.status_acao
        }