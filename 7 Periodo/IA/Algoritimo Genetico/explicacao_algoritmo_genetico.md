# Explicação do Algoritmo Genético e do Fluxo do Programa

## Visão geral

Este projeto simula uma batalha entre vários bots em uma arena 2D.
Cada bot possui uma sequência de ações, como girar, andar para frente e andar para trás.

A ideia do algoritmo genético é melhorar essas sequências ao longo do tempo.
Em vez de programar manualmente o comportamento ideal de cada bot, o programa:

1. cria vários indivíduos com ações aleatórias;
2. deixa esses indivíduos "competirem";
3. mede quais tiveram melhor desempenho;
4. usa os melhores para gerar uma nova geração;
5. repete o processo.

Esse processo tenta imitar, de forma simplificada, a ideia de evolução.

---

## O que é um indivíduo neste projeto

No arquivo principal, cada `Individuo` representa um bot da arena.
Ele possui:

- `nome`: identificação do bot;
- `cor`: usada para desenhar o bot na tela;
- `x` e `y`: posição do bot;
- `angulo`: direção para onde ele está apontando;
- `acoes`: lista de comandos originais;
- `acoes_formatadas`: lista expandida de comandos;
- `pontos`: quantidade de acertos feitos em outros bots;
- `vivo`: indica se o bot ainda está ativo na rodada.

Exemplo de ações:

- `R-10`: girar;
- `F-2`: andar para frente;
- `T-1`: andar para trás.

---

## Etapa 1: geração da população inicial

Isso acontece na função `gera_populacao`.

O programa cria vários bots aleatórios.
Para cada bot, ele também cria uma lista de ações aleatórias.

Essa é a população inicial.

Em algoritmo genético, "população" é o conjunto de soluções atuais que serão avaliadas.
Neste caso, cada solução é um bot com um conjunto de comandos.

---

## Etapa 2: execução da simulação

Durante a execução da arena:

1. cada bot pega sua próxima ação;
2. o bot gira ou se move;
3. o sistema verifica ataques;
4. se um bot acertar outro, ele ganha ponto e o alvo deixa de participar daquela rodada.

Esse processo acontece várias vezes em loop.

No arquivo `ga_battle.py`, isso ocorre principalmente dentro de:

- `desenha()`
- `verifica_ataques()`

O objetivo dessa fase é descobrir quais indivíduos tiveram melhor desempenho.

---

## Etapa 3: avaliação

A avaliação é feita pela pontuação (`pontos`) de cada indivíduo.

Quanto mais pontos um bot faz, melhor ele se saiu.
Então a pontuação funciona como a medida de qualidade da solução.

No contexto de algoritmo genético, isso costuma ser chamado de:

- aptidão;
- fitness;
- desempenho.

Aqui, a aptidão do bot é representada pela quantidade de pontos que ele conseguiu.

---

## Etapa 4: seleção

Depois de um número de loops, o programa cria uma nova geração.
Antes disso, ele precisa escolher quais indivíduos têm mais chance de continuar.

Isso acontece no arquivo [ga_montar_roleta.py](</e:/Estudos/Sistemas de Informação/IFMG_Sistema-de-Informacao/7 Periodo/ga_montar_roleta.py:1>) e em [ga_selecao_natural.py](</e:/Estudos/Sistemas de Informação/IFMG_Sistema-de-Informacao/7 Periodo/ga_selecao_natural.py:1>).

### Como funciona a roleta

A função `montar_roleta(populacao)` cria uma seleção probabilística.

Ideia:

- indivíduos com mais pontos têm mais chance de serem escolhidos;
- indivíduos com menos pontos ainda podem ser escolhidos, mas com menor chance.

Isso é importante porque:

- mantém pressão para melhorar a população;
- evita que apenas um único tipo de solução domine cedo demais.

### Como funciona a seleção natural

A função `selecao_natural(populacao, num_sobreviventes, roleta)` usa essa roleta para escolher os sobreviventes.

Esses sobreviventes serão usados para gerar os filhos da próxima geração.

---

## Etapa 5: crossover

Depois da seleção, o programa precisa preencher a nova população.
Para isso, ele combina partes de dois pais.

Isso acontece no arquivo [ga_crossover.py](</e:/Estudos/Sistemas de Informação/IFMG_Sistema-de-Informacao/7 Periodo/ga_crossover.py:1>).

### Ideia do crossover

Cada pai possui uma lista de ações.
O programa:

1. escolhe um ponto em um dos pais;
2. escolhe um ponto no outro pai;
3. junta uma parte da lista de ações do primeiro com uma parte da lista do segundo.

O resultado é um novo indivíduo, chamado de filho.

Exemplo conceitual:

Pai 1:
`["R-5", "F-2", "F-1"]`

Pai 2:
`["T-1", "R-10", "F-3"]`

Filho:
`["R-5", "F-2", "R-10", "F-3"]`

O crossover é importante porque mistura características que deram certo em indivíduos diferentes.

---

## Etapa 6: mutação

Mesmo com crossover, a população pode ficar muito parecida entre si.
Por isso existe a mutação.

Isso acontece no arquivo [ga_mutacoes.py](</e:/Estudos/Sistemas de Informação/IFMG_Sistema-de-Informacao/7 Periodo/ga_mutacoes.py:1>).

### Ideia da mutação

Com certa probabilidade, o programa altera uma ação de um indivíduo.

Exemplo:

- antes: `F-1`
- depois: `R-12`

Essa alteração aleatória ajuda a:

- introduzir novas possibilidades;
- evitar que a população fique presa em soluções ruins;
- aumentar a diversidade.

---

## Etapa 7: nova geração

Depois de:

- selecionar os melhores;
- gerar filhos com crossover;
- aplicar mutações;

o programa forma uma nova população.

Isso acontece no método `aplicar_iteracao`.

Em seguida, os bots são reiniciados na arena com:

- `vivo = True`
- `pontos = 0`
- nova posição

Depois disso, a simulação continua e uma nova rodada de avaliação começa.

---

## Fluxo completo do programa

O fluxo geral pode ser entendido assim:

1. o programa abre a janela;
2. ao clicar, cria a população inicial;
3. os bots começam a executar suas ações;
4. os ataques são verificados;
5. cada bot acumula pontos;
6. após vários ciclos, o algoritmo genético é executado;
7. uma nova geração é criada;
8. a população reinicia;
9. o processo se repete.

---

## Relação entre os arquivos

### `ga_battle.py`

É o arquivo principal.
Controla:

- a janela;
- a arena;
- os bots;
- o loop da simulação;
- o momento de chamar o algoritmo genético.

### `ga_montar_roleta.py`

Cria a roleta de probabilidades para a seleção.

### `ga_selecao_natural.py`

Escolhe os indivíduos que sobrevivem para gerar a próxima geração.

### `ga_crossover.py`

Mistura partes de dois pais para criar um filho.

### `ga_mutacoes.py`

Aplica alterações aleatórias em alguns indivíduos.

---

## Resumo da lógica do algoritmo genético

O algoritmo genético deste projeto segue a sequência clássica:

1. inicialização da população;
2. avaliação;
3. seleção;
4. cruzamento;
5. mutação;
6. nova geração.

Em palavras simples:

- o programa cria vários bots aleatórios;
- observa quais se saem melhor;
- aproveita os melhores para gerar novos bots;
- faz pequenas mudanças aleatórias;
- repete isso para tentar melhorar o comportamento ao longo do tempo.

---

## Intuição final

O mais importante é entender que o algoritmo genético não "sabe" a melhor solução desde o começo.
Ele tenta encontrar soluções melhores aos poucos, usando tentativa, avaliação e recombinação.

Neste projeto, a solução que está sendo evoluída é:

- a sequência de ações dos bots.

Ou seja, o programa está tentando descobrir quais combinações de movimentos geram melhores resultados dentro da arena.
