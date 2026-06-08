import pygame
import random
import pyttsx3
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador
from recursos.trabalho import top3
import math

limpar_tela()
inicializarBancoDeDados()
nome_maior, maior_pontos, dataJogada = maior_pontuador()
pygame.init()

try:
    voz = pyttsx3.init()
except Exception as erro:
    print("Erro ao iniciar voz:", erro)
    voz = None

while True:
    nome = input("Qual o seu nome marinheiro?: ") 
    if len(nome) > 0: 
        break
    else:
        print("Nome Inválido!")
        
tamanho = (1000,700)
pygame.display.set_caption("STORM RAIDERS")
icone  = pygame.image.load("bases/navio.png")

pygame.display.set_icon(icone)
relogio = pygame.time.Clock()

tela = pygame.display.set_mode( tamanho) 

branco = (255, 255, 255)

preto = (0, 0, 0)

fundo = pygame.image.load("bases/ceu.png")
fundo = pygame.transform.scale(fundo, (2500, 700))


fundoDead = pygame.image.load("bases/game_over.png")
fundoDead = pygame.transform.scale(fundoDead, (1000,700))

fundoStart = pygame.image.load("bases/telaStart.png")
fundoStart = pygame.transform.scale(fundoStart, (1000,700))

navio = pygame.image.load("bases/navio.png")
navio = pygame.transform.scale(navio, (116,51))

bala = pygame.image.load("bases/bala_de_canhao.png")
bala = pygame.transform.scale(bala, (90,25))

nuvem = pygame.image.load("bases/nuvem.png")
nuvem = pygame.transform.scale(nuvem, (120, 60))

balaDecanhao = pygame.mixer.Sound("bases/bala_de_canhao_som.mp3")
derrotaSom = pygame.mixer.Sound("bases/derrota.mp3")
pygame.mixer.music.load("bases/somPirata.mp3")
fonteRanking = pygame.font.SysFont("arial",14)
fonteMenu = pygame.font.SysFont("comicsans",18)

x_nome = 770
x_data = 785

def jogar():

    posicaoXPersona = 50
    posicaoYPersona = 60

    movimentoYPersona = 0
    velocidadeMovPersona = 5

    posicaoXMissel = 720
    posicaoYMissel = 1000
    velocidadeMissel = 4

    posicaoXNuvem =random.randint(0, 900)
    posicaoYNuvem = random.randint(20, 650)
    velocidadeNuvem = random.randint(1, 3)

    fundoX = 0

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
            tela.blit(fundo, (fundoX, 0))

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

            posicaoXMissel = 1000

            pygame.mixer.Sound.play(balaDecanhao)

            pontos += 1

            velocidadeMissel += 3

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

        fundoX -= 1

        if fundoX <= -1500:
            fundoX = 0

        pygame.draw.circle(tela,(255, 215, 0),(900, 90),int(raioBussola + 8))

        pygame.draw.circle(tela,(180, 140, 0),(900, 90),int(raioBussola))

        pygame.draw.circle(tela,branco,(900, 90),5)

        angulo += 2
        x_agulha = 900 + math.cos(math.radians(angulo)) * 25
        y_agulha = 90 + math.sin(math.radians(angulo)) * 25

        pygame.draw.line(tela,(255, 0, 0),(900, 90),(x_agulha, y_agulha),4)


        tela.blit(nuvem, (posicaoXNuvem, posicaoYNuvem))
        
        tela.blit(navio, (posicaoXPersona, posicaoYPersona))

        tela.blit(bala, (posicaoXMissel, posicaoYMissel))

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
    

    falou_game_over = False

    while True:
        startButton = pygame.Rect(328, 495, 339, 65)
        menuButton = pygame.Rect(328, 573, 339, 67)
        
        pygame.draw.rect(tela, (255,0,0), startButton, 2)
        pygame.draw.rect(tela, (0,255,0), menuButton, 2)

        if not falou_game_over:

            pygame.mixer.stop()
            pygame.mixer.music.stop()

            pygame.time.delay(50)

            if voz:
                try:
                    voz.say("Game Over")
                    voz.runAndWait()
                except:
                    pass

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


        ranking = top3()

        x_nome = 770
        x_data = 785
        y = 100

        for posicao, (nomeJogador, pontosJogador, dataJogador, horaJogador) in enumerate(ranking, start=1):

            textoRanking = fonteRanking.render(f"{posicao}º {nomeJogador} = {pontosJogador}",True,branco)
            tela.blit(textoRanking, (x_nome, y))

            y += 12

            textoDataHora = fonteRanking.render(f"{dataJogador} {horaJogador}",True,branco)

            tela.blit(textoDataHora, (x_data, y))

            y += 14

        pygame.display.update()
        relogio.tick(60)


def start():

    falou_boas_vindas = False

    startY = 460

    while True:

        if voz:
            try:
                voz.say(f"Bem vindo ao Storm Raiders, {nome}")
                voz.runAndWait()
            except:
                pass

        ranking = top3()

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

        y = 100

        if len(ranking) == 0:

            textoRanking = fonteMenu.render("Sem pontuacoes",True,branco)

            tela.blit(textoRanking, (780, y))

        else:

            for posicao, (nomeJogador, pontosJogador, dataJogador, horaJogador) in enumerate(ranking, start=1):

                textoRanking = fonteRanking.render(f"{posicao}º {nomeJogador[:6]}",True,branco)
                textoPontos = fonteRanking.render(f"= {pontosJogador} pts",True,branco)

                tela.blit(textoPontos, (850, y))

                tela.blit(textoRanking, (760, y))

                y += 16

                textoDataHora = fonteRanking.render(f"{dataJogador} {horaJogador}",True,branco)

                tela.blit(textoDataHora, (x_data, y))

                y += 11

        textoJogador = fonteMenu.render(f"Bem-vindo, {nome}!",True,branco)

        tela.blit(textoJogador, (400, 390))

        pause = fonteMenu.render("Press Space to Pause Game",True,branco)

        tela.blit(pause, (20, 660))

        pygame.display.update()

        relogio.tick(60)
           
start()