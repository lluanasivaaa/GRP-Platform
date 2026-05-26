import pandas as pd


PROBABILITY_LEVELS = ["Baixa", "Média", "Alta"]
IMPACT_LEVELS = ["Baixo", "Médio", "Alto"]

_PROBABILITY_SCORES = {
    "baixa": 1,
    "media": 2,
    "média": 2,
    "mã©dia": 2,
    "alta": 3,
}

_IMPACT_SCORES = {
    "baixo": 1,
    "medio": 2,
    "médio": 2,
    "mã©dio": 2,
    "alto": 3,
}


def _normalize_label(value):
    if value is None:
        return ""
    return str(value).strip().lower()


def calcular_score_risco(probabilidade, impacto):
    prob = _PROBABILITY_SCORES.get(_normalize_label(probabilidade), 1)
    imp = _IMPACT_SCORES.get(_normalize_label(impacto), 1)
    return prob * imp


def normalizar_probabilidade(value):
    score = _PROBABILITY_SCORES.get(_normalize_label(value), 1)
    return PROBABILITY_LEVELS[score - 1]


def normalizar_impacto(value):
    score = _IMPACT_SCORES.get(_normalize_label(value), 1)
    return IMPACT_LEVELS[score - 1]


def calcular_criticidade(probabilidade, impacto):
    """
    Calcula o nível de criticidade baseado em probabilidade e impacto.
    Probabilidade: 'Baixa' = 1, 'Média' = 2, 'Alta' = 3
    Impacto: 'Baixo' = 1, 'Médio' = 2, 'Alto' = 3
    Fórmula: criticidade = probabilidade * impacto
    Classificação: 1-2 Baixo, 3-4 Médio, 6-9 Alto
    """
    criticidade = calcular_score_risco(probabilidade, impacto)

    if criticidade <= 2:
        return "Baixo"
    if criticidade <= 4:
        return "Médio"
    return "Alto"


def construir_matriz_risco(riscos):
    rows = []
    for probabilidade in reversed(PROBABILITY_LEVELS):
        for impacto in IMPACT_LEVELS:
            total = sum(
                1
                for risco in riscos
                if normalizar_probabilidade(risco.get("probabilidade")) == probabilidade
                and normalizar_impacto(risco.get("impacto")) == impacto
            )
            score = calcular_score_risco(probabilidade, impacto)
            rows.append(
                {
                    "probabilidade": probabilidade,
                    "impacto": impacto,
                    "total": total,
                    "score": score,
                    "criticidade": calcular_criticidade(probabilidade, impacto),
                }
            )
    return pd.DataFrame(rows)
