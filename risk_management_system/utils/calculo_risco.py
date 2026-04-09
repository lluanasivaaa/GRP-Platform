def calcular_criticidade(probabilidade, impacto):
    """
    Calcula o nível de criticidade baseado em probabilidade e impacto.
    Probabilidade e impacto: 'Baixa' = 1, 'Média' = 2, 'Alta' = 3
    Fórmula: criticidade = probabilidade * impacto
    Classificação: 1-2 Baixo, 3-4 Médio, 6-9 Alto
    """
    mapa = {'Baixa': 1, 'Média': 2, 'Alta': 3}
    prob = mapa.get(probabilidade, 1)
    imp = mapa.get(impacto, 1)
    criticidade = prob * imp

    if criticidade <= 2:
        return 'Baixo'
    elif criticidade <= 4:
        return 'Médio'
    else:
        return 'Alto'