PROJECT_STATUS_OPTIONS = [
    "Backlog",
    "Planejamento",
    "Em Execução",
    "Em Validação",
    "Concluído",
    "Cancelado",
]

ACTIVE_PROJECT_STATUS = PROJECT_STATUS_OPTIONS[:4]

LEGACY_STATUS_MAP = {
    "Ativo": "Backlog",
    "Em Execu\xc3\xa7\xc3\xa3o": "Em Execução",
    "Em Valida\xc3\xa7\xc3\xa3o": "Em Validação",
    "Conclu\xc3\xaddo": "Concluído",
}

STATUS_COLORS = {
    "Backlog": "#1d4ed8",
    "Planejamento": "#7c3aed",
    "Em Execução": "#ea580c",
    "Em Validação": "#0f766e",
    "Concluído": "#166534",
    "Cancelado": "#b91c1c",
}

STATUS_DESCRIPTIONS = {
    "Backlog": "Ideias e demandas aguardando priorização.",
    "Planejamento": "Projetos sendo detalhados e organizados.",
    "Em Execução": "Iniciativas em andamento com entregas ativas.",
    "Em Validação": "Projetos em revisão, testes ou aprovação final.",
    "Concluído": "Projetos finalizados e entregues.",
    "Cancelado": "Projetos encerrados ou pausados sem continuidade.",
}


def normalize_project_status(status):
    if not status:
        return PROJECT_STATUS_OPTIONS[0]
    return LEGACY_STATUS_MAP.get(status, status)
