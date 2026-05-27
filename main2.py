import pygame
import random
import pyttsx3
from recursos.funcoes import (
    inicializarBancoDeDados,
    limpar_tela,
    escreverDados,
    maior_pontuador
)

limpar_tela()
inicializarBancoDeDados()

nome_maior, maior_pontos, dataJogada = maior_pontuador()

pygame.init()

engine = pyttsx3.init()

while True:
    nome = input("Digite seu nome marinheiro: ")

    if len(nome) > 0:
        break
    else:
        print("Nome inválido!")

engine.say(f"Bem vindo {nome}")
engine.runAndWait()

tamanho = (1000, 700)

tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Pirata dos Céus")

icone = pygame.image.load("bases/navio.png")
pygame.display.set_icon(icone)

relogio = pygame.time.Clock()

branco = (255, 255, 255)
preto = (0, 0, 0)
amarelo = (255, 255, 0)

fonteMenu = pygame.font.SysFont("comicsans", 18)
fonteGrande = pygame.font.SysFont("comicsans", 50)

ceu = pygame.image.load("bases/ceu.png")
fundo = pygame.transform.scale(ceu, (1000, 700))

fundoDead = pygame.image.load("bases/game_over.png")
fundoDead = pygame.transform.scale(fundoDead, (1000, 700))

fundoStart = pygame.image.load("bases/telaStart.png")
fundoStart = pygame.transform.scale(fundoStart, (1000, 700))

canhao = pygame.image.load("bases/canhao.png")
canhao = pygame.transform.scale(canhao, (116, 51))

balaCanhao = pygame.image.load("bases/bala_de_canhao.png")
balaCanhao = pygame.transform.scale(balaCanhao, (125, 25))

nuvem = pygame.image.load("bases/nuvem.png")
nuvem = pygame.transform.scale(nuvem, (120, 70))

def jogar():

    fundoMov1 = 0
    fundoMov2 = 1000

    posicaoXPersona = 50
    posicaoYPersona = 300

    movimentoYPersona = 0
    velocidadeMovPersona = 5

    posicaoXMissel = 1000
    posicaoYMissel = 100

    velocidadeMissel = 7

    pontos = 0

    dificuldade = 20

    pausado = False

    raioSol = 40
    aumentando = True

    nuvemX = random.randint(0, 1000)
    nuvemY = random.randint(0, 200)

    while True:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pass

            elif evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()


                if evento.key == pygame.K_SPACE:
                    pausado = not pausado

                if evento.key == pygame.K_UP:
                    movimentoYPersona = -velocidadeMovPersona

                if evento.key == pygame.K_DOWN:
                    movimentoYPersona = velocidadeMovPersona

            elif evento.type == pygame.KEYUP:

                if evento.key == pygame.K_UP:
                    movimentoYPersona = 0

                if evento.key == pygame.K_DOWN:
                    movimentoYPersona = 0

        if pausado:
            tela.blit(fundo, (0, 0))

            textoPause = fonteGrande.render("PAUSE", True, branco)
            tela.blit(textoPause, (400, 320))

            pygame.display.update()
            relogio.tick(60)
            continue

        posicaoYPersona += movimentoYPersona

        if posicaoYPersona < 0:
            posicaoYPersona = 0

        elif posicaoYPersona > 600:
            posicaoYPersona = 600

        posicaoXMissel -= velocidadeMissel

        if posicaoXMissel < -125:

            pontos += 1

            velocidadeMissel += 1

            posicaoXMissel = 1000
            posicaoYMissel = random.randint(0, 650)

        fundoMov1 -= 1
        fundoMov2 -= 1

        if fundoMov1 <= -1000:
            fundoMov1 = 1000

        if fundoMov2 <= -1000:
            fundoMov2 = 1000

        nuvemX -= 2

        if nuvemX < -150:
            nuvemX = 1000
            nuvemY = random.randint(0, 200)

        # -----------------------------
        # SOL PULSANDO
        # -----------------------------

        if aumentando:
            raioSol += 0.2

            if raioSol >= 50:
                aumentando = False

        else:
            raioSol -= 0.2

            if raioSol <= 40:
                aumentando = True
                
        tela.fill(branco)

        tela.blit(fundo, (fundoMov1, 0))
        tela.blit(fundo, (fundoMov2, 0))

        pygame.draw.circle(tela, amarelo, (920, 80), int(raioSol))

        tela.blit(nuvem, (nuvemX, nuvemY))

        tela.blit(canhao, (posicaoXPersona, posicaoYPersona))

        tela.blit(balaCanhao, (posicaoXMissel, posicaoYMissel))

        texto = fonteMenu.render(f"Pontos: {pontos}", True, branco)
        tela.blit(texto, (820, 15))

        textoPauseInfo = fonteMenu.render(
            "Press Space to Pause Game",
            True,
            branco
        )

        tela.blit(textoPauseInfo, (10, 670))

        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona + 116))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona + 51))

        pixelsMisselX = list(range(posicaoXMissel, posicaoXMissel + 125))
        pixelsMisselY = list(range(posicaoYMissel, posicaoYMissel + 25))

        if len(list(set(pixelsMisselY).intersection(set(pixelsPersonaY)))) > dificuldade:

            if len(list(set(pixelsMisselX).intersection(set(pixelsPersonaX)))) > dificuldade:

                escreverDados(nome, pontos)
                dead()

        pygame.display.update()
        relogio.tick(60)


# -----------------------------
# TELA GAME OVER
# -----------------------------

def dead():

    larguraButtonStart = 180
    alturaButtonStart = 45

    while True:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pass

            elif evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:

                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 170
                    alturaButtonStart = 40

            elif evento.type == pygame.MOUSEBUTTONUP:

                if startButton.collidepoint(evento.pos):
                    jogar()

        tela.fill(branco)
        tela.blit(fundoDead, (0, 0))

        # BOTÃO
        startButton = pygame.draw.rect(
            tela,
            branco,
            (20, 20, larguraButtonStart, alturaButtonStart),
            border_radius=15
        )

        startTexto = fonteMenu.render("Jogar Novamente", True, preto)
        tela.blit(startTexto, (40, 32))

        # MAIOR PONTUADOR
        textoRecorde = fonteMenu.render(
            f"Recorde: {nome_maior} - {maior_pontos}",
            True,
            branco
        )

        tela.blit(textoRecorde, (340, 20))

        pygame.display.update()
        relogio.tick(60)


# -----------------------------
# TELA START
# -----------------------------

def start():

    larguraButtonStart = 180
    alturaButtonStart = 45

    while True:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:

                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 170
                    alturaButtonStart = 40

            elif evento.type == pygame.MOUSEBUTTONUP:

                if startButton.collidepoint(evento.pos):
                    jogar()

        tela.fill(branco)
        tela.blit(fundoStart, (0, 0))

        startButton = pygame.draw.rect(
            tela,
            branco,
            (20, 20, larguraButtonStart, alturaButtonStart),
            border_radius=15
        )

        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (45, 32))

        # NOME
        textoNome = fonteMenu.render(
            f"Bem vindo {nome}",
            True,
            branco
        )

        tela.blit(textoNome, (350, 180))

        textoExplicacao1 = fonteMenu.render(
            "Desvie das balas de canhao e sobreviva o maximo possivel.",
            True,
            branco
        )

        textoExplicacao2 = fonteMenu.render(
            "Use as setas para mover e ESPACO para pausar.",
            True,
            branco
        )

        tela.blit(textoExplicacao1, (250, 240))
        tela.blit(textoExplicacao2, (280, 280))

        textoRecorde = fonteMenu.render(
            f"The Best - {nome_maior} - {maior_pontos} - {dataJogada}",
            True,
            branco
        )

        tela.blit(textoRecorde, (320, 20))

        pygame.display.update()
        relogio.tick(60)

start()