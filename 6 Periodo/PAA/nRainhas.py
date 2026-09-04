def print_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        print(" ".join("Q" if c else "." for c in linha))
    print()

def eh_seguro(tabuleiro, linha, coluna, n):
    # checa a coluna
    for i in range(linha):
        if tabuleiro[i][coluna]:
            return False

    # diagonal esquerda superior
    i, j = linha - 1, coluna - 1
    while i >= 0 and j >= 0:
        if tabuleiro[i][j]:
            return False
        i -= 1
        j -= 1

    # diagonal direita superior
    i, j = linha - 1, coluna + 1
    while i >= 0 and j < n:
        if tabuleiro[i][j]:
            return False
        i -= 1
        j += 1

    return True

def resolver_n_rainhas(tabuleiro, linha, n):
    if linha == n:
        print_tabuleiro(tabuleiro)
        return True  # mostra só a primeira solução encontrada

    for coluna in range(n):
        if eh_seguro(tabuleiro, linha, coluna, n):
            tabuleiro[linha][coluna] = True
            if resolver_n_rainhas(tabuleiro, linha + 1, n):
                return True
            tabuleiro[linha][coluna] = False  # desfaz (backtrack)

    return False

def n_rainhas(n):
    tabuleiro = [[False] * n for _ in range(n)]
    resolver_n_rainhas(tabuleiro, 0, n)

# 🧩 Exemplo: tabuleiro 4x4
n_rainhas(8)
