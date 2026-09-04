# Pseudoalgoritmos do Algoritmo Genético

Este arquivo descreve, em pseudoalgoritmo, quatro partes importantes do algoritmo genético usado no projeto:

- `montar_roleta`
- `selecao_natural`
- `crossover`
- `mutacoes`

O objetivo é mostrar a lógica passo a passo, sem depender da sintaxe do Python.

---

## 1. Pseudoalgoritmo de `montar_roleta`

### Ideia

Essa função transforma a pontuação dos indivíduos em probabilidades acumuladas.
Assim, indivíduos com mais pontos têm mais chance de serem escolhidos.

### Pseudoalgoritmo

```text
função montar_roleta(populacao)
    criar lista pesos vazia

    para cada individuo da populacao
        peso <- pontos do individuo + 1
        adicionar peso na lista pesos
    fim para

    soma <- somatório de todos os pesos
    acumulado <- 0
    criar lista roleta vazia

    para cada peso da lista pesos
        acumulado <- acumulado + (peso / soma)
        adicionar acumulado na lista roleta
    fim para

    retornar roleta
fim função
```

### Explicação simples

Se a população tiver pesos:

```text
[2, 3, 5]
```

então a roleta acumulada será algo parecido com:

```text
[0.2, 0.5, 1.0]
```

Isso significa:

- o primeiro indivíduo ocupa 20% da roleta;
- o segundo ocupa do 20% até 50%;
- o terceiro ocupa do 50% até 100%.

---

## 2. Pseudoalgoritmo de `selecao_natural`

### Ideia

Essa função usa a roleta para escolher quais indivíduos sobrevivem e poderão gerar filhos.

### Pseudoalgoritmo

```text
função selecao_natural(populacao, num_sobreviventes, roleta)
    criar lista selecionados vazia
    criar conjunto assinaturas vazio

    enquanto tamanho de selecionados for menor que num_sobreviventes
        valor <- número aleatório entre 0 e 1

        para i de 0 até tamanho da roleta - 1
            se valor for menor ou igual a roleta[i]
                escolhido <- populacao[i]
                parar o laço
            fim se
        fim para

        assinatura <- (nome do escolhido, ações do escolhido)

        se assinatura ainda não estiver em assinaturas
            adicionar assinatura em assinaturas
            clone <- cópia do escolhido
            adicionar clone em selecionados
        fim se
    fim enquanto

    retornar selecionados
fim função
```

### Explicação simples

A seleção natural faz um sorteio com peso.
Quem tem mais pontos tem mais chance de continuar.

Mesmo assim, indivíduos mais fracos ainda podem ser escolhidos, dependendo do sorteio.
Isso ajuda a manter diversidade.

---

## 3. Pseudoalgoritmo de `crossover`

### Ideia

O crossover mistura ações de dois pais para criar um filho.

### Pseudoalgoritmo

```text
função crossover(progenitor1, progenitor2)
    acoes1 <- lista de ações do progenitor1
    acoes2 <- lista de ações do progenitor2

    escolher ponto1 aleatório em acoes1
    escolher ponto2 aleatório em acoes2

    novas_acoes <- início de acoes1 até ponto1
    concatenado com
    final de acoes2 a partir de ponto2

    se novas_acoes estiver vazia
        novas_acoes <- ["F-1"]
    fim se

    criar filho com:
        nome aleatório
        cor herdada de um dos pais
        posição aleatória
        ações = novas_acoes

    construir ações formatadas do filho

    retornar filho
fim função
```

### Exemplo conceitual

Se:

```text
Pai 1 = [R-5, F-2, F-1, T-1]
Pai 2 = [F-3, R-10, T-2, F-1]
```

e os pontos sorteados forem:

```text
ponto1 = 2
ponto2 = 1
```

então o filho pode ficar:

```text
[R-5, F-2, R-10, T-2, F-1]
```

### Explicação simples

O crossover tenta juntar partes boas de dois indivíduos diferentes.

---

## 4. Pseudoalgoritmo de `mutacoes`

### Ideia

A mutação altera aleatoriamente uma ação de alguns indivíduos.

### Pseudoalgoritmo

```text
função mutacoes(populacao, taxa)
    para cada individuo da populacao
        sorteio <- número aleatório entre 0 e 1

        se sorteio for maior que taxa
            continuar para o próximo indivíduo
        fim se

        se individuo não possuir ações
            continuar para o próximo indivíduo
        fim se

        indice <- posição aleatória dentro da lista de ações
        tipo <- escolher aleatoriamente entre R, F e T

        se tipo for R
            nova_acao <- "R-" + valor aleatório entre 1 e 18
        senão
            nova_acao <- tipo + "-" + valor aleatório entre 1 e 3
        fim se

        substituir a ação antiga pela nova_acao
        reconstruir as ações formatadas do indivíduo
    fim para
fim função
```

### Explicação simples

A mutação insere pequenas mudanças aleatórias.
Ela é importante para:

- evitar que todos os indivíduos fiquem iguais;
- trazer novas possibilidades;
- permitir que soluções inesperadas apareçam.

---

## Fluxo entre essas funções

As quatro funções trabalham juntas nesta ordem:

```text
1. avaliar a população pelos pontos
2. montar_roleta
3. selecao_natural
4. crossover para gerar novos filhos
5. mutacoes para introduzir variações
6. formar a nova geração
```

---

## Resumo final em pseudoalgoritmo geral

```text
início
    criar população inicial

    enquanto o programa estiver executando
        simular movimentos e ataques
        calcular pontos de cada indivíduo

        se chegar o momento de criar nova geração
            roleta <- montar_roleta(populacao)
            sobreviventes <- selecao_natural(populacao, metade_da_populacao, roleta)

            enquanto nova população não estiver completa
                escolher dois sobreviventes
                filho <- crossover(sobrevivente1, sobrevivente2)
                adicionar filho na nova população
            fim enquanto

            aplicar mutacoes na nova população
            substituir população antiga pela nova população
        fim se
    fim enquanto
fim
```
