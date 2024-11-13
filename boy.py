import tkinter as tk
import random

# Configurações do jogo
LARGURA = 400
ALTURA = 400
TAMANHO_PERSONAGEM = 20
VELOCIDADE_ATUALIZACAO = 100  # Milissegundos
VELOCIDADE_GOLEIRA = 5  # Velocidade inicial da goleira
VELOCIDADE_BOLA = 10  # Velocidade da bola ao ser chutada

# Classe principal do jogo
class JogoChuteGoleira:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo de Chute a Goleira")
        self.canvas = tk.Canvas(root, width=LARGURA, height=ALTURA, bg="green")
        self.canvas.pack()

        # Inicializa os elementos do jogo
        self.personagem_pos = [200, 300]  # Posição inicial do personagem
        self.bola_pos = [LARGURA // 2, ALTURA // 2]  # Posição inicial da bola
        self.goleira_x = random.randint(50, LARGURA - 150)
        self.goleira_y = 50
        self.direcao = None
        self.pontos = 0
        self.bola_em_movimento = False
        self.velocidade_goleira = VELOCIDADE_GOLEIRA
        self.direcao_goleira = 1
        self.movimento_habilitado = True  # Controle do movimento do personagem

        # Liga os controles do teclado
        self.root.bind("<Left>", lambda _: self.mudar_direcao("esquerda"))
        self.root.bind("<Right>", lambda _: self.mudar_direcao("direita"))
        self.root.bind("<Up>", lambda _: self.mudar_direcao("cima"))
        self.root.bind("<Down>", lambda _: self.mudar_direcao("baixo"))

        # Atualiza o jogo
        self.atualizar_jogo()

    def mudar_direcao(self, nova_direcao):
        if self.movimento_habilitado:  # Só permite mudar a direção se o movimento estiver habilitado
            self.direcao = nova_direcao

    def mover_personagem(self):
        x, y = self.personagem_pos
        bx, by = self.bola_pos

        # Movimenta o personagem com restrição para não ultrapassar a linha horizontal da bola
        if self.direcao == "direita" and x + TAMANHO_PERSONAGEM < LARGURA:
            x += TAMANHO_PERSONAGEM
        elif self.direcao == "esquerda" and x > 0:
            x -= TAMANHO_PERSONAGEM
        elif self.direcao == "cima" and y > by:
            y -= TAMANHO_PERSONAGEM
        elif self.direcao == "baixo" and y + TAMANHO_PERSONAGEM < ALTURA:
            y += TAMANHO_PERSONAGEM

        self.personagem_pos = [x, y]

    def verificar_colisao_bola(self):
        px, py = self.personagem_pos
        bx, by = self.bola_pos
        return abs(px - bx) < TAMANHO_PERSONAGEM and abs(py - by) < TAMANHO_PERSONAGEM

    def verificar_gol(self):
        bola_x, bola_y = self.bola_pos
        return (self.goleira_y <= bola_y <= self.goleira_y + 20) and (self.goleira_x <= bola_x <= self.goleira_x + 100)

    def atualizar_jogo(self):
        # Movimenta o personagem
        if self.direcao and self.movimento_habilitado:
            self.mover_personagem()

        # Movimenta a goleira
        self.goleira_x += self.velocidade_goleira * self.direcao_goleira
        if self.goleira_x <= 0 or self.goleira_x + 100 >= LARGURA:
            self.direcao_goleira *= -1  # Inverte a direção da goleira

        # Verifica se o personagem colide com a bola
        if not self.bola_em_movimento and self.verificar_colisao_bola():
            self.bola_em_movimento = True  # A bola é "chutada" em direção à goleira
            self.movimento_habilitado = False  # Desabilita o movimento do personagem

        # Movimenta a bola se estiver em movimento
        if self.bola_em_movimento:
            self.bola_pos[1] -= VELOCIDADE_BOLA
            # Verifica se a bola faz o gol
            if self.verificar_gol():
                self.pontos += 1
                self.velocidade_goleira += 1  # Aumenta a velocidade da goleira
                self.reset_posicoes()  # Reseta as posições após o gol
            elif self.bola_pos[1] <= 0:  # Se a bola sai da tela sem marcar
                self.reset_posicoes()

        # Desenha os elementos do jogo
        self.desenhar_elementos()
        self.root.after(VELOCIDADE_ATUALIZACAO, self.atualizar_jogo)

    def reset_posicoes(self):
        # Reposiciona o personagem e a bola no centro do campo
        self.personagem_pos = [200, 300]
        self.bola_pos = [LARGURA // 2, ALTURA // 2]
        self.bola_em_movimento = False
        self.movimento_habilitado = True  # Reabilita o movimento do personagem
        self.goleira_x = random.randint(50, LARGURA - 150)

    def desenhar_elementos(self):
        self.canvas.delete("all")

        # Desenha o personagem com cabeça, corpo, braços e pernas
        x, y = self.personagem_pos
        self.canvas.create_rectangle(x, y, x + TAMANHO_PERSONAGEM, y + TAMANHO_PERSONAGEM, fill="blue")  # Corpo
        self.canvas.create_oval(x + 5, y - 10, x + 15, y, fill="pink")  # Cabeça
        self.canvas.create_line(x, y + 5, x - 5, y + 15, fill="blue", width=2)  # Braço esquerdo
        self.canvas.create_line(x + TAMANHO_PERSONAGEM, y + 5, x + TAMANHO_PERSONAGEM + 5, y + 15, fill="blue", width=2)  # Braço direito
        self.canvas.create_line(x + 5, y + TAMANHO_PERSONAGEM, x, y + TAMANHO_PERSONAGEM + 10, fill="blue", width=2)  # Perna esquerda
        self.canvas.create_line(x + 15, y + TAMANHO_PERSONAGEM, x + 20, y + TAMANHO_PERSONAGEM + 10, fill="blue", width=2)  # Perna direita
        self.canvas.create_rectangle(x + 3, y - 12, x + 17, y - 10, fill="red")  # Chapéu

        # Desenha a bola
        bola_x, bola_y = self.bola_pos
        self.canvas.create_oval(bola_x - 5, bola_y - 5, bola_x + 5, bola_y + 5, fill="white")

        # Desenha a goleira
        self.canvas.create_rectangle(self.goleira_x, self.goleira_y, self.goleira_x + 100, self.goleira_y + 20, fill="white")

        # Exibe pontuação
        self.canvas.create_text(50, 10, text=f"Pontos: {self.pontos}", fill="white", font=("Arial", 12))

# Cria a janela e executa o jogo
root = tk.Tk()
jogo = JogoChuteGoleira(root)
root.mainloop()




