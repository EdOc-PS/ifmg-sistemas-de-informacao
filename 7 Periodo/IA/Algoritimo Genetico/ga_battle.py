"""
Tradução comentada do exemplo em Java para Python.

O programa cria uma pequena arena onde "bots" se movimentam, giram,
atacam outros bots e, depois de alguns ciclos, uma nova geração é
criada usando um algoritmo genético simples.

Principais diferenças em relação ao original:
- Em vez de Swing, usamos tkinter, que já vem com o Python.
- As partes do algoritmo genético que estavam vazias no Java foram
  implementadas para o programa realmente evoluir a população.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import math
import random
import tkinter as tk

from ga_crossover import crossover
from ga_montar_roleta import montar_roleta
from ga_mutacoes import mutacoes
from ga_selecao_natural import selecao_natural


LARGURA_JANELA = 600
ALTURA_JANELA = 600
TAMANHO_BOT = 20
NUMERO_INDIVIDUOS = 60
TEMPO_LOOP_MS = 10
MAX_GAME_LOOPS = 10_000
LOOPS_POR_GERACAO = 1_000


def gerar_cor_aleatoria() -> str:
    """Gera uma cor em formato hexadecimal aceito pelo tkinter."""
    return f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"


@dataclass
class Individuo:
    # Identificação visual do bot.
    nome: str
    cor: str

    # Posição do canto superior esquerdo do quadrado.
    x: int
    y: int
    tlado: int

    # Lista de ações "compactas", por exemplo: ["R-10", "F-2"].
    acoes: list[str] = field(default_factory=list)

    # Estado do indivíduo ao longo da simulação.
    vivo: bool = True
    pontos: int = 0
    contador_acao: int = 0
    angulo: float = 0.0

    # Lista expandida de ações, onde "R-15" vira vários "R".
    acoes_formatadas: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.reposicionar(self.x, self.y)

    def reposicionar(self, nx: int, ny: int) -> None:
        """Reposiciona o bot e recalcula centro e arma."""
        self.x = nx
        self.y = ny
        self.centro_x = self.x + self.tlado // 2
        self.centro_y = self.y + self.tlado // 2
        self.atualizar_arma()

    def atualizar_arma(self) -> None:
        """
        Calcula a ponta da arma com base no ângulo atual.

        A arma nasce apontando para a direita e gira em torno do centro.
        """
        rad = math.radians(self.angulo)
        alcance = self.tlado // 2 + 5
        self.x_arma = int(self.centro_x + math.cos(rad) * alcance)
        self.y_arma = int(self.centro_y + math.sin(rad) * alcance)

    def construir_acoes_formatadas(self) -> None:
        """
        Converte ações compactas em uma sequência mais detalhada.

        Exemplo:
        - "R-15" vira ['R', 'R', 'R']
        - "F-2" adiciona esperas e depois um movimento para frente
        """
        self.acoes_formatadas.clear()
        for comando_bruto in self.acoes:
            tipo, valor_texto = comando_bruto.split("-")
            valor = int(valor_texto)

            if tipo == "R":
                acumulado = 0
                while acumulado <= valor:
                    self.acoes_formatadas.append("R")
                    acumulado += 5
            else:
                velocidade = 3 - valor
                for _ in range(velocidade + 1):
                    self.acoes_formatadas.append("E")
                self.acoes_formatadas.append(tipo)

        if not self.acoes_formatadas:
            self.acoes_formatadas.append("E")

    def proxima_acao(self) -> str:
        """Retorna a próxima ação, repetindo o ciclo ao chegar no final."""
        if not self.acoes_formatadas:
            return "E"

        if self.contador_acao >= len(self.acoes_formatadas) - 1:
            self.contador_acao = 0
        else:
            self.contador_acao += 1
        return self.acoes_formatadas[self.contador_acao]

    def rotacionar(self, angulo: float) -> None:
        """Rotaciona o bot no sentido horário."""
        self.angulo = (self.angulo + angulo) % 360
        self.atualizar_arma()

    def _vetor_movimento(self) -> tuple[int, int]:
        """
        Aproxima o deslocamento do Java original.

        O código-fonte original usava intervalos de ângulo com vetores
        discretos. Aqui mantemos essa ideia para ficar parecido.
        """
        intervalos_ini = [0, 5, 30, 80, 100, 135, 170, 190, 260, 280]
        intervalos_fim = [5, 30, 60, 100, 135, 170, 190, 260, 280, 360]
        vetor_x = [1, 2, 2, 1, 0, -1, 0, -2, 0, 2]
        vetor_y = [0, 1, 2, 2, 1, 2, 2, -2, -2, -2]

        for inicio, fim, dx, dy in zip(intervalos_ini, intervalos_fim, vetor_x, vetor_y):
            if inicio <= self.angulo < fim:
                return dx, dy
        return 1, 0

    def move(self) -> None:
        """Move o bot para frente, respeitando o ângulo atual."""
        dx, dy = self._vetor_movimento()
        self.x += dx
        self.y += dy
        self.centro_x += dx
        self.centro_y += dy
        self.atualizar_arma()

    def move_reverso(self) -> None:
        """Move o bot para trás."""
        dx, dy = self._vetor_movimento()
        self.x -= dx
        self.y -= dy
        self.centro_x -= dx
        self.centro_y -= dy
        self.atualizar_arma()

    def copiar(self) -> "Individuo":
        """Cria uma cópia do indivíduo para cruzamento/mutação."""
        clone = Individuo(
            nome=self.nome,
            cor=self.cor,
            x=self.x,
            y=self.y,
            tlado=self.tlado,
            acoes=list(self.acoes),
        )
        clone.angulo = self.angulo
        clone.construir_acoes_formatadas()
        return clone


class AlgoritmoGenetico:
    @staticmethod
    def gera_populacao(quantidade: int) -> list[Individuo]:
        """Cria a população inicial com comandos aleatórios."""
        individuos: list[Individuo] = []

        for _ in range(quantidade):
            individuo = Individuo(
                nome=f"Id:{random.randint(0, 600)};",
                cor=gerar_cor_aleatoria(),
                x=random.randint(0, LARGURA_JANELA - TAMANHO_BOT),
                y=random.randint(0, ALTURA_JANELA - TAMANHO_BOT),
                tlado=TAMANHO_BOT,
            )

            numero_comandos = random.randint(5, 29)
            for _ in range(numero_comandos):
                sorteio = random.randint(1, 3)
                if sorteio == 1:
                    individuo.acoes.append(f"R-{random.randint(1, 18)}")
                elif sorteio == 2:
                    individuo.acoes.append(f"F-{random.randint(1, 3)}")
                else:
                    individuo.acoes.append(f"T-{random.randint(1, 3)}")

            individuo.construir_acoes_formatadas()
            individuos.append(individuo)

        return individuos

    @staticmethod
    def print_dados_populacao(populacao: list[Individuo]) -> None:
        """Exibe os dados da população no terminal para depuração."""
        print("-" * 26)
        print("Dados da população:")
        for bot in populacao:
            scomandos = ",".join(bot.acoes)
            print(f"{bot.nome}; {bot.pontos}; {scomandos}")
        print("-" * 26)

    @staticmethod
    def aplicar_iteracao(populacao: list[Individuo]) -> list[Individuo]:
        """
        Executa um ciclo do algoritmo genético:
        seleção, cruzamento e mutação.
        """
        print("antes da roleta")
        AlgoritmoGenetico.print_dados_populacao(populacao)

        roleta = montar_roleta(populacao)
        selecionados = selecao_natural(populacao, len(populacao) // 2, roleta)

        while len(selecionados) < len(populacao):
            pai1 = random.choice(selecionados)
            pai2 = random.choice(selecionados)
            while pai1 is pai2:
                pai2 = random.choice(selecionados)
            selecionados.append(
                crossover(pai1, pai2, LARGURA_JANELA, TAMANHO_BOT, Individuo)
            )

        mutacoes(selecionados, 0.3)
        print("depois das mutações")
        AlgoritmoGenetico.print_dados_populacao(selecionados)
        return selecionados


class GABattle:
    """
    Janela principal da simulação.

    O Java usava um JPanel e uma Thread separada. Em tkinter, a forma
    mais natural é usar um Canvas e agendar o próximo loop com `after`.
    """

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("GA Battle")

        self.canvas = tk.Canvas(self.root, width=LARGURA_JANELA, height=ALTURA_JANELA, bg="white")
        self.canvas.pack()

        self.individuos: list[Individuo] = []
        self.gameloops = 0

        # O clique inicia a população, assim como no código Java.
        self.canvas.bind("<Button-1>", self.iniciar_populacao)

    def iniciar_populacao(self, _evento: tk.Event) -> None:
        """Cria a população quando o usuário clica pela primeira vez."""
        if not self.individuos:
            self.individuos = AlgoritmoGenetico.gera_populacao(NUMERO_INDIVIDUOS)

    def reiniciar_populacao(self, individuos: list[Individuo]) -> None:
        """Prepara os bots para a próxima rodada."""
        for bot in individuos:
            bot.vivo = True
            bot.pontos = 0
            bot.angulo = 0
            bot.reposicionar(
                random.randint(0, LARGURA_JANELA - TAMANHO_BOT),
                random.randint(0, ALTURA_JANELA - TAMANHO_BOT),
            )

    @staticmethod
    def check_ataque2(i1: Individuo, i2: Individuo) -> bool:
        """Verifica se a ponta da arma do i1 entrou na área do i2."""
        limite_inf_x = i2.centro_x - i2.tlado / 2
        limite_sup_x = i2.centro_x + i2.tlado / 2
        limite_inf_y = i2.centro_y - i2.tlado / 2
        limite_sup_y = i2.centro_y + i2.tlado / 2
        return (
            limite_inf_x < i1.x_arma < limite_sup_x
            and limite_inf_y < i1.y_arma < limite_sup_y
        )

    def verifica_ataques(self, individuos: list[Individuo]) -> None:
        """Percorre todos os pares e marca eliminações."""
        for i, atacante in enumerate(individuos):
            if not atacante.vivo:
                continue
            for j, alvo in enumerate(individuos):
                if i == j or not alvo.vivo:
                    continue
                if self.check_ataque2(atacante, alvo):
                    atacante.pontos += 1
                    alvo.vivo = False

    def desenhar_individuo(self, bot: Individuo) -> None:
        """Desenha o corpo, a arma e a legenda do bot."""
        self.canvas.create_rectangle(
            bot.x,
            bot.y,
            bot.x + bot.tlado,
            bot.y + bot.tlado,
            fill=bot.cor,
            outline=bot.cor,
        )
        self.canvas.create_oval(
            bot.x_arma - 2,
            bot.y_arma - 2,
            bot.x_arma + 2,
            bot.y_arma + 2,
            fill="red",
            outline="red",
        )
        self.canvas.create_text(
            bot.centro_x,
            bot.centro_y - 12,
            text=f"{bot.nome}{bot.pontos}",
            fill="black",
            font=("Arial", 7),
        )

    def desenha(self) -> None:
        """Executa um frame da simulação e agenda o próximo."""
        if self.gameloops >= MAX_GAME_LOOPS:
            return

        self.canvas.delete("all")

        for bot in self.individuos:
            if not bot.vivo:
                continue

            cod_comando = bot.proxima_acao()
            if cod_comando == "R":
                bot.rotacionar(5)
            elif cod_comando == "F":
                bot.move()
            elif cod_comando == "T":
                bot.move_reverso()

            if bot.centro_x < 0 or bot.centro_x > LARGURA_JANELA:
                bot.reposicionar(0, 0)
            elif bot.centro_y < 0 or bot.centro_y > ALTURA_JANELA:
                bot.reposicionar(0, 0)

            self.desenhar_individuo(bot)

        self.verifica_ataques(self.individuos)

        if self.gameloops > 0 and self.gameloops % LOOPS_POR_GERACAO == 0:
            print("alterando população")
            self.individuos = AlgoritmoGenetico.aplicar_iteracao(self.individuos)
            self.reiniciar_populacao(self.individuos)

        self.gameloops += 1
        self.root.after(TEMPO_LOOP_MS, self.desenha)

    def executar(self) -> None:
        """Inicia o loop da interface."""
        self.desenha()
        self.root.mainloop()


if __name__ == "__main__":
    print("main...")
    GABattle().executar()
