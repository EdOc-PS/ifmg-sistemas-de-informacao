"""Implementação separada da função crossover."""

import random


def crossover(progenitor1, progenitor2, largura_janela, tamanho_bot, individuo_cls):
    """
    Combina comandos de dois pais para formar um filho.

    Usamos crossover de um ponto: início do primeiro com final do segundo.
    """
    acoes1 = list(progenitor1.acoes)
    acoes2 = list(progenitor2.acoes)

    ponto1 = random.randint(1, len(acoes1)) if acoes1 else 0
    ponto2 = random.randint(0, len(acoes2) - 1) if acoes2 else 0
    novas_acoes = acoes1[:ponto1] + acoes2[ponto2:]

    if not novas_acoes:
        novas_acoes = ["F-1"]

    filho = individuo_cls(
        nome=f"Filho:{random.randint(1000, 9999)}",
        cor=random.choice([progenitor1.cor, progenitor2.cor]),
        x=random.randint(0, largura_janela - tamanho_bot),
        y=random.randint(0, largura_janela - tamanho_bot),
        tlado=tamanho_bot,
        acoes=novas_acoes,
    )
    filho.construir_acoes_formatadas()
    return filho
