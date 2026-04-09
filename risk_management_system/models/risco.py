class Risco:
    def __init__(self, id_risco=None, id_projeto=None, descricao='', categoria='', probabilidade='Baixa', impacto='Baixo', nivel_criticidade='Baixo', status_risco='Ativo'):
        self.id_risco = id_risco
        self.id_projeto = id_projeto
        self.descricao = descricao
        self.categoria = categoria
        self.probabilidade = probabilidade
        self.impacto = impacto
        self.nivel_criticidade = nivel_criticidade
        self.status_risco = status_risco

    def to_dict(self):
        return {
            'id_risco': self.id_risco,
            'id_projeto': self.id_projeto,
            'descricao': self.descricao,
            'categoria': self.categoria,
            'probabilidade': self.probabilidade,
            'impacto': self.impacto,
            'nivel_criticidade': self.nivel_criticidade,
            'status_risco': self.status_risco
        }