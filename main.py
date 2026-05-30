import pygame
import random
import pyttsx3
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador
import math

limpar_tela()
inicializarBancoDeDados()
nome_maior, maior_pontos, dataJogada = maior_pontuador()
pygame.init()
voz = pyttsx3.init()

while True:
    nome = input("Qual o seu nome marinheiro?: ")
    if len(nome) > 0: 
        break
    else:
        print("Nome Inválido!")
        
tamanho = (1000,700)
pygame.display.set_caption("pensamento computacional")
icone  = pygame.image.load("bases/navio.png")

pygame.display.set_icon(icone)
relogio = pygame.time.Clock()

tela = pygame.display.set_mode( tamanho ) 

branco = (255, 255, 255)

preto = (0, 0, 0)

fundo = pygame.image.load("bases/ceu.png")
fundo = pygame.transform.scale(fundo, (2500, 700))
fundoX = 0

fundoDead = pygame.image.load("bases/game_over.png")
fundoDead = pygame.transform.scale(fundoDead, (1000,700))

fundoStart = pygame.image.load("bases/telaStart.png")
fundoStart = pygame.transform.scale(fundoStart, (1000,700))

iron = pygame.image.load("bases/navio.png")
iron = pygame.transform.scale(iron, (116,51))

missel = pygame.image.load("bases/bala_de_canhao.png")
missel = pygame.transform.scale(missel, (125,25))

nuvem = pygame.image.load("bases/nuvem.png")
nuvem = pygame.transform.scale(nuvem, (120, 60))

balaDecanhao = pygame.mixer.Sound("bases/bala_de_canhao_som.mp3")
derrotaSom = pygame.mixer.Sound("bases/derrota.mp3")
pygame.mixer.music.load("bases/somPirata.mp3")
fonteMenu = pygame.font.SysFont("comicsans",18)

def jogar():

    posicaoXPersona = 50
    posicaoYPersona = 60

    movimentoYPersona = 0
    velocidadeMovPersona = 5

    posicaoXMissel = 800
    posicaoYMissel = 1000
    velocidadeMissel = 4

    posicaoXNuvem = random.randint(0, 900)
    posicaoYNuvem = random.randint(20, 650)
    velocidadeNuvem = random.randint(1, 3)

    pontos = 0
    pausado = False

    pygame.mixer.Sound.play(balaDecanhao)
    pygame.mixer.music.play(-1)

    dificuldade = 20

    raioBussola = 35
    crescendo = True
    angulo = 0

    while True:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                quit()

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP:
                movimentoYPersona = -velocidadeMovPersona

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN:
                movimentoYPersona = velocidadeMovPersona

            elif evento.type == pygame.KEYUP and evento.key == pygame.K_UP:
                movimentoYPersona = 0

            elif evento.type == pygame.KEYUP and evento.key == pygame.K_DOWN:
                movimentoYPersona = 0

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausado = not pausado
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()


        if pausado:
            tela.blit(fundo, (0, 0))

            fontePause = pygame.font.SysFont("comicsans", 80)

            textoPause = fontePause.render("PAUSE",True,branco)

            tela.blit(textoPause, (330, 280))

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

            pygame.mixer.Sound.play(balaDecanhao)

            posicaoXMissel = 1000

            pontos += 1

            velocidadeMissel += 2

            posicaoYMissel = random.randint(0, 600)


        posicaoXNuvem -= velocidadeNuvem

        if posicaoXNuvem < -220:

            posicaoXNuvem = 1000

            posicaoYNuvem = random.randint(20, 650)

            velocidadeNuvem = random.randint(1, 3)

        if crescendo:
            raioBussola += 0.5
        else:
            raioBussola -= 0.5

        if raioBussola >= 40:
            crescendo = False

        if raioBussola <= 35:
            crescendo = True
    
        tela.fill(branco)

        tela.blit(fundo, (fundoX, 0))

        fundoMov1 -= 2
        fundoMov2 -= 2

        pygame.draw.circle(tela,(255, 215, 0),(900, 90),int(raioBussola + 8))

        pygame.draw.circle(tela,(180, 140, 0),(900, 90),int(raioBussola))

        pygame.draw.circle(tela,branco,(900, 90),5)
     
        x_agulha = 900 + math.cos(math.radians(angulo)) * 25
        y_agulha = 90 + math.sin(math.radians(angulo)) * 25

        pygame.draw.line(tela,(255, 0, 0),(900, 90),(x_agulha, y_agulha),4)

        fundoX -= 1

        if fundoX <= -1000:
            fundoX = 0

        tela.blit(nuvem, (posicaoXNuvem, posicaoYNuvem))
        
        tela.blit(iron, (posicaoXPersona, posicaoYPersona))

        tela.blit(missel, (posicaoXMissel, posicaoYMissel))

        texto = fonteMenu.render("Pontos: " + str(pontos),True,branco)

        tela.blit(texto, (850, 15))

        fontePequena = pygame.font.SysFont("arial", 16)

        textoPauseInfo = fontePequena.render("Press Space to Pause Game",True,branco)

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

def dead():

    startY = 525
    menuY = 625

    falou_game_over = False

    while True:

        startButton = pygame.Rect(355,startY,335,70)

        menuButton = pygame.Rect(355,menuY,335,70)

        if not falou_game_over:

            pygame.mixer.stop()
            pygame.mixer.music.stop()

            pygame.time.delay(50)

            voz.say("Game Over")
            voz.runAndWait()

            derrotaSom.play()

            falou_game_over = True

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:

                if startButton.collidepoint(evento.pos):
                    startY = 530

                if menuButton.collidepoint(evento.pos):
                    menuY = 630

            elif evento.type == pygame.MOUSEBUTTONUP:

                if startButton.collidepoint(evento.pos):

                    startY = 505

                    jogar()

                if menuButton.collidepoint(evento.pos):

                    menuY = 610

                    start()

        tela.fill(branco)

        tela.blit(fundoDead, (0, 0))

        textoRecorde = fonteMenu.render(f"{nome_maior} - {maior_pontos} pontos",True,branco)


        tela.blit(textoRecorde, (790, 120))
        pygame.display.update()
        relogio.tick(60)


def start():

    startY = 460

    while True:

        startButton = pygame.Rect(370,startY,260,70)

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:

                if startButton.collidepoint(evento.pos):

                    startY = 465

            elif evento.type == pygame.MOUSEBUTTONUP:

                if startButton.collidepoint(evento.pos):

                    startY = 460

                    jogar()

        tela.fill(branco)

        tela.blit(fundoStart, (0, 0))

        startTexto = fonteMenu.render("",True,preto)

        tela.blit(startTexto, (445, startY + 20))

        textoJogador = fonteMenu.render(f"Bem-vindo, {nome}!",True,branco)

        tela.blit(textoJogador, (400, 390))

        pause = fonteMenu.render("Press Space to Pause Game",True,branco)

        tela.blit(pause, (20, 660))

        pygame.display.update()

        relogio.tick(60)
           
start()