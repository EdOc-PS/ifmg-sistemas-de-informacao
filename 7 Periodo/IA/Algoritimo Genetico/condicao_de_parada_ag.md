# Condição de Parada no Algoritmo Genético

## Existe uma condição de parada no código atual?

Sim, mas ela está ligada mais à simulação do que ao algoritmo genético em si.

No arquivo principal, existe este controle:

```text
MAX_GAME_LOOPS = 10000
```

e no método `desenha()` a execução para quando:

```text
gameloops >= MAX_GAME_LOOPS
```

Isso significa que, no estado atual do projeto, a condição de parada é:

- encerrar a simulação depois de uma quantidade fixa de ciclos da arena.

Então, hoje, a parada acontece por **limite de loops da simulação**.

---

## Essa é uma condição de parada típica de algoritmo genético?

Não é a forma mais clássica.

Em algoritmo genético, a condição de parada normalmente está relacionada à evolução da população, e não apenas ao tempo de execução da simulação.

Ou seja, em um algoritmo genético, normalmente o programa para quando:

- atingiu um número máximo de gerações;
- encontrou uma solução considerada boa o suficiente;
- ou percebeu que não está mais melhorando.

---

## Se tivesse uma condição de parada mais própria do algoritmo genético, qual seria?

A melhor resposta para este projeto seria usar **número máximo de gerações**.

Como o sistema já evolui a população a cada certo intervalo, uma condição simples e correta seria:

- parar depois de `N` gerações.

### Exemplo

Se cada nova geração é criada a cada 1000 loops, então poderíamos definir:

```text
MAX_GERACOES = 20
```

e encerrar o algoritmo quando:

```text
geracao_atual >= MAX_GERACOES
```

---

## Por que essa seria uma boa condição?

Porque ela mede diretamente quantas vezes o processo evolutivo aconteceu.

Isso faz mais sentido em algoritmo genético do que contar apenas os loops da animação, já que o mais importante não é quantas vezes a tela foi atualizada, mas sim quantas gerações foram produzidas.

---

## Outras condições de parada possíveis

Além do número máximo de gerações, existem outras condições comuns.

### 1. Melhor indivíduo atingiu uma pontuação desejada

Exemplo:

```text
se melhor_individuo.pontos >= meta
    parar
```

Nesse caso, o algoritmo para quando encontra uma solução considerada satisfatória.

No contexto do projeto, isso significaria:

- parar quando um bot alcançasse um desempenho muito bom.

---

### 2. A população parou de melhorar

Exemplo:

```text
se durante muitas gerações a melhor pontuação não aumentar
    parar
```

Isso é útil quando o algoritmo entra em estagnação.

No projeto, essa condição indicaria que:

- os bots já não estão evoluindo de forma significativa;
- continuar executando provavelmente não vai trazer ganho importante.

---

### 3. Tempo máximo de execução

Exemplo:

```text
se tempo_total >= limite
    parar
```

Essa condição é útil quando existe restrição de tempo.

---

## Qual seria a melhor escolha para este trabalho?

Para este projeto, a condição mais adequada e mais fácil de justificar seria:

- **parar após um número máximo de gerações**.

Motivos:

- é simples de implementar;
- combina diretamente com a lógica do algoritmo genético;
- é fácil de explicar em atividade, relatório ou apresentação;
- permite comparar resultados entre execuções.

---

## Exemplo de pseudoalgoritmo com condição de parada

```text
geracao <- 0
MAX_GERACOES <- 20

enquanto geracao < MAX_GERACOES
    executar batalha entre os indivíduos
    avaliar pontuação
    selecionar melhores indivíduos
    gerar filhos com crossover
    aplicar mutações
    formar nova geração
    geracao <- geracao + 1
fim enquanto
```

---

## Conclusão

No código atual, existe sim uma condição de parada, mas ela é:

- baseada em quantidade de loops da simulação.

Se quisermos uma condição de parada mais correta para o algoritmo genético, a melhor opção seria:

- usar um número máximo de gerações.

Se quisermos uma versão mais avançada, também poderíamos combinar:

- máximo de gerações;
- meta de pontuação;
- ausência de melhoria por várias gerações.
