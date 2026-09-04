"""Implementação separada da função selecao_natural."""

import random


def _sortear_por_roleta(populacao, roleta):
    """Escolhe um indivíduo com base na roleta acumulada."""
    valor = random.random()
    for indice, limite in enumerate(roleta):
        if valor <= limite:
            return populacao[indice]
    return populacao[-1]


def selecao_natural(populacao, num_sobreviventes, roleta):
    """
    Seleciona os sobreviventes usando a roleta.

    Evitamos duplicatas exatas para preservar um pouco mais de variedade.
    """
    selecionados = []
    assinaturas = set()

    while len(selecionados) < num_sobreviventes:
        escolhido = _sortear_por_roleta(populacao, roleta)
        assinatura = (escolhido.nome, tuple(escolhido.acoes))
        if assinatura not in assinaturas:
            assinaturas.add(assinatura)
            clone = escolhido.copiar()
            clone.nome = f"{escolhido.nome}_sel"
            selecionados.append(clone)

    return selecionados
