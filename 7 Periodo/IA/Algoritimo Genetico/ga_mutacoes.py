"""Implementação separada da função mutacoes."""

import random


def mutacoes(populacao, taxa):
    """
    Aplica mutações aleatórias na lista de ações dos indivíduos.

    A ideia é introduzir variedade genética entre as gerações.
    """
    for bot in populacao:
        if random.random() > taxa or not bot.acoes:
            continue

        indice = random.randrange(len(bot.acoes))
        tipo = random.choice(["R", "F", "T"])
        if tipo == "R":
            bot.acoes[indice] = f"R-{random.randint(1, 18)}"
        else:
            bot.acoes[indice] = f"{tipo}-{random.randint(1, 3)}"
        bot.construir_acoes_formatadas()
