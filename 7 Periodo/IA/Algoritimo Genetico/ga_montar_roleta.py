"""Implementação separada da função montar_roleta."""


def montar_roleta(populacao):
    """
    Monta a roleta de seleção.

    Se todos tiverem zero pontos, cada indivíduo ainda recebe peso 1
    para continuar podendo ser sorteado.
    """
    pesos = [max(bot.pontos, 0) + 1 for bot in populacao]
    soma = sum(pesos)
    acumulado = 0.0
    roleta = []

    for peso in pesos:
        acumulado += peso / soma
        roleta.append(acumulado)

    return roleta
