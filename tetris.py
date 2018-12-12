#!/usr/bin/python
# -*- coding: utf-8 -*-

# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, time, pygame, sys
from pygame.locals import *

FPS = 60.0988 
WINDOWWIDTH = 800
WINDOWHEIGHT = 680
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'

MOVESIDEWAYSFREQ = 0.1
MOVEDOWNFREQ = 0.1

XMARGIN = 171
TOPMARGIN = 189

#               R    G    B
WHITE       = (255, 255, 255)
BLACK       = (  0,   0,   0)
RED         = (236,  17,  11)
GREEN       = ( 29, 242,  10)
YELLOW      = (253, 228, 129)

BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = BLACK

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

# Peça S
S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

# Peça Z
Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

# Peça I
I_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....'],
                    ['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....']]

# Peça O
O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

# Peça J
J_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....']]

# Peça L
L_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....']]

# Peça T
T_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....']]

# Dict com as peças
PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

# Plano de Fundo
BACKGROUND = pygame.image.load('Sprites/Background/background.png')

# Sprites dos blocos
BLOCKS = [[pygame.image.load('Sprites/Blocks/1A.png'), pygame.image.load('Sprites/Blocks/1B.png'), pygame.image.load('Sprites/Blocks/1C.png')],
          [pygame.image.load('Sprites/Blocks/2A.png'), pygame.image.load('Sprites/Blocks/2B.png'), pygame.image.load('Sprites/Blocks/2C.png')],
          [pygame.image.load('Sprites/Blocks/3A.png'), pygame.image.load('Sprites/Blocks/3B.png'), pygame.image.load('Sprites/Blocks/3C.png')],
          [pygame.image.load('Sprites/Blocks/4A.png'), pygame.image.load('Sprites/Blocks/4B.png'), pygame.image.load('Sprites/Blocks/4C.png')],
          [pygame.image.load('Sprites/Blocks/5A.png'), pygame.image.load('Sprites/Blocks/5B.png'), pygame.image.load('Sprites/Blocks/5C.png')],
          [pygame.image.load('Sprites/Blocks/6A.png'), pygame.image.load('Sprites/Blocks/6B.png'), pygame.image.load('Sprites/Blocks/6C.png')],
          [pygame.image.load('Sprites/Blocks/7A.png'), pygame.image.load('Sprites/Blocks/7B.png'), pygame.image.load('Sprites/Blocks/7C.png')],
          [pygame.image.load('Sprites/Blocks/8A.png'), pygame.image.load('Sprites/Blocks/8B.png'), pygame.image.load('Sprites/Blocks/8C.png')],
          [pygame.image.load('Sprites/Blocks/9A.png'), pygame.image.load('Sprites/Blocks/9B.png'), pygame.image.load('Sprites/Blocks/9C.png')],
          [pygame.image.load('Sprites/Blocks/10A.png'), pygame.image.load('Sprites/Blocks/10B.png'), pygame.image.load('Sprites/Blocks/10C.png')]]

# Sprites dos Rounds
ROUNDS = [pygame.image.load('Sprites/Rounds/0.png'),
          pygame.image.load('Sprites/Rounds/1.png'),
          pygame.image.load('Sprites/Rounds/2.png'),
          pygame.image.load('Sprites/Rounds/3.png')]

'''
Função main.
'''
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT, SCOREFONT, POINTSFONT
    global LINESFONT, NAME, WINNERFONT
    
    # Inicializa o pygame
    pygame.init()
    # Tempo entre os FPS
    FPSCLOCK = pygame.time.Clock()
    # Seta o tamanho da tela
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    # Fonte para letras pequenas
    BASICFONT = pygame.font.Font('Fonts/Pixel_NES.otf', 18)
    # Fonte para letras grandes
    BIGFONT = pygame.font.Font('Fonts/Pixel_NES.otf', 100)
    # Fonte para o SCORE
    SCOREFONT = pygame.font.Font('Fonts/Pixel_NES.otf', 24)
    # Fonte para os Pontos
    POINTSFONT = pygame.font.Font('Fonts/Pixel_NES.otf', 28)
    # Fonte para as linhas
    LINESFONT = pygame.font.Font('Fonts/Pixel_NES.otf', 26)
    # Fonte para a tela de vitoria
    WINNERFONT = pygame.font.Font('Fonts/Pixel_NES.otf', 50)
    # Nome do Player 1
    NAME = 'JUAN'

    # Seta o nome da Janela
    pygame.display.set_caption('Classic Tetris Multiplayer')

    # Inicializa a tela inicial
    showTextScreen('TETRIS')

    # Loop do jogo
    while True:
        # Roda o jogo
        runGame()
        # Dá o nome do vencedor
        showWinnerScreen('FELIPE')

'''
Função que mostra um texto grande no meio.
da tela
'''
def showTextScreen(text):
    # Desenha a sombra do texto
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Desenha o texto
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Desenha a mensagem de apertar a tecla
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    # Espera até alguma tecla ser apertada
    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

'''
Função que immprime o vencedor na tela
'''
def showWinnerScreen(text):

    position = 100

    # Desenha a sombra do texto
    titleSurf, titleRect = makeTextObjs(text, WINNERFONT, BLACK)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Desenha o texto
    titleSurf, titleRect = makeTextObjs(text, WINNERFONT, YELLOW)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Desenha a sombra da String WINS THE ROUND
    titleSurf, titleRect = makeTextObjs('WON THE ROUND!',WINNERFONT, BLACK)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + position - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Desenha a string WINS THE ROUND
    titleSurf, titleRect = makeTextObjs('WON THE ROUND!', WINNERFONT, YELLOW)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) + position)
    DISPLAYSURF.blit(titleSurf, titleRect)

    t = time.time()
    x = t;

    # Espera até alguma tecla ser apertada
    while x - t < 3:
        x = time.time()
        pygame.display.update()
        FPSCLOCK.tick()


'''
Função que cria um objeto com o texto.
'''
def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

'''
Função que retorna um evento se uma peça
foi pressionada
'''
def checkForKeyPress():
    
    # Verifica se ouve algum evento de saida do jogo
    checkForQuit()

    # Passa por todos eventos
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        # Retorna o evento
        return event.key

    # Não passou por nenhum evento
    return None

'''
Função que verifica se o jogar saiu do jogo
'''
def checkForQuit():
    # Se tiver evento de saida, termina o jogo
    for event in pygame.event.get(QUIT): 
        terminate() 

    # Pega todas as teclas apertadas
    for event in pygame.event.get(KEYUP):
        
        # Se ESC foi apertado, sai do jogo 
        if event.key == K_ESCAPE:
            terminate() 

        # Recoloca as teclas apertadas 
        pygame.event.post(event) 

'''
Função que finaliza o pygame
'''
def terminate():
    # Sai do pygame
    pygame.quit()
    # Termina o programa
    sys.exit()

'''
Função utilizada para rodar o jogo.
'''
def runGame():
    global level
    # Inicializa o jogo
    board = getBlankBoard()

    # Inicializa os tempos de movimentação
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()

    # Inicializa as variaveis de movimento
    movingDown = False 
    movingLeft = False
    movingRight = False

    # Inicializa a pontuação
    score = 0

    # Quantidade de linhas cortadas
    clearLines = 0


    # Calcula o nivel e a frequência de queda
    level, fallFreq = calculateLevelAndFallFreq(clearLines)

    # Inicializa a peça que vai cair
    fallingPiece = getNewPiece()

    # Inicializa a peça que vai ser a seguinte
    nextPiece = getNewPiece()

    # Loop da partida
    while True:

        # Confere se nenhuma peça está caindo
        if fallingPiece == None:
            
            # Peça caindo é a peça seguinte
            fallingPiece = nextPiece
            # Gera uma nova peça seguinte
            nextPiece = getNewPiece()

            # Reseta o tempo da ultima caida
            lastFallTime = time.time() 

            # Se a peça não está em uma posição valida, você perdeu
            if not isValidPosition(board, fallingPiece):
                return

        # Verifica se teve algum evento de saida do jogo
        checkForQuit()

        # Loop pegando todos os eventos
        for event in pygame.event.get(): # event handling loop
            
            # Se uma tecla foi solta
            if event.type == KEYUP:

                # Se a tecla P foi solta, pausa o jogo
                if (event.key == K_p):

                    # Pinta a tecla com a cor do fundo
                    DISPLAYSURF.fill(BGCOLOR)
                    # Mostra a tela de pausa até apertar alguma peça
                    showTextScreen('PAUSED') 
                    
                    # Atualiza o tempo das peças
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()

                # Se a tecla LEFT ou A foi solta, para de andar pra esquerda
                elif (event.key == K_LEFT or event.key == K_a):
                    movingLeft = False
                # Se a tecla RIGHT ou D foi solta, para de andar pra direita
                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                # Se a tecla DOWN ou S foi solta, para de andar pra baixo
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = False

            # Se uma tecla foi pressionada
            elif event.type == KEYDOWN:
                
                # Se a tecla LEFT ou A foi apertada E a peça vai estar numa posição válida,
                # pode ir pra esquerda
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
                    # Atualiza o X uma posição a esquerda
                    fallingPiece['x'] -= 1
                    # Está indo pra esquerda
                    movingLeft = True
                    # Não está indo pra direita
                    movingRight = False
                    # Atualiza o tempo de se movimentar pros lados
                    lastMoveSidewaysTime = time.time()

                # Se a tecla RIGHT ou D foi apertada E a peça vai estar numa posição válida.
                # pode ir pra direita
                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                    # Atualiza o X uma posição a direita
                    fallingPiece['x'] += 1
                    # Está indo pra direita
                    movingRight = True
                    # Não está indo pra esquerda
                    movingLeft = False
                    # Atualiza o tempo de se movimentar pros lados
                    lastMoveSidewaysTime = time.time()

                # Se a tecla UP ou W foi apertada, rotaciona a peça pra direita
                elif (event.key == K_UP or event.key == K_w):
                    # Rotação para direita
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    
                    # Se a rotação fez a peça ficar inválida, desfaz rotação
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                
                # Se a tecla Q foi apertada, rotaciona a peça pra esquerda
                elif (event.key == K_q):
                    # Rotação para esquerda
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    
                    # Se a rotação fez a peça ficar inválida, desfaz a rotação
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])

                # Se a tecla DOWN ou S foi apertada, desce a peça
                elif (event.key == K_DOWN or event.key == K_s):
                    # Peça esta indo pra baixo
                    movingDown = True
                    # Confere se a posição é válida
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1

                    # Atualiza o tempo de se movimentar pra baixo
                    lastMoveDownTime = time.time()

        # Se estiver movendo pra esquerda ou pra direita E 
        # O tempo da ultima movimentação pros lados for maior que a frequência de movimentação
        # Faz o movimento pro lado
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            
            # Se movimentou pra esquerda E a posição é valida
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                # Atualiza o x da peça pra esquerda
                fallingPiece['x'] -= 1

            # Se movimentou pra direita E a posição é valdia
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                # Atualiza o x da peça pra direita
                fallingPiece['x'] += 1

            # Atualiza o tempo da ultima movimentação pros lados
            lastMoveSidewaysTime = time.time()

        # Se estiver movendo para baixo E
        # o tempo da ultima movimentação pra baixo for maior que a frequência de movimentação E
        # ir para uma posição válida
        # Faz o movimento pra baixo
        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            # Atualiza o valor de y pra baixo
            fallingPiece['y'] += 1

            # Atualiza o tempo da ultima movimentação pra baixo
            lastMoveDownTime = time.time()

        # Se o tempo da ultima queda for maior que a frequência de queda,
        # Move pra baixo
        if time.time() - lastFallTime > fallFreq:
            
            # Se a peça chegou numa posição não válida,
            # Adiciona ela no tabuleiro
            if not isValidPosition(board, fallingPiece, adjY=1):
                
                # Adiciona a peça ao tabuleiro
                addToBoard(board, fallingPiece)
                
                # Remove as peças completadas recebendo uma tupla 
                # contendo a (pontuação, linhasEliminadas)
                x = removeCompleteLines(board)

                # Somou os pontos
                score += x[0]
                # Somou as linhas
                clearLines += x[1]

                # Calcula o novo nivel e frequência de queda
                level, fallFreq = calculateLevelAndFallFreq(clearLines)
                # Não tem nenhuma peça caindo
                fallingPiece = None

            # A peça não chegou numa posição não válida
            # desce a peça uma posição pra baixo
            else:
                
                # Aumenta uma posição pra baixo
                fallingPiece['y'] += 1
                # Atualiza o ultimo tempo de queda
                lastFallTime = time.time()


        # Limita o score máximo
        if score > 999999:
            score = 999999

        # Pinta o fundo de preto
        DISPLAYSURF.fill(BGCOLOR)
        # Pinta o background
        DISPLAYSURF.blit(BACKGROUND, (0, 0))

        '''
        Display do Player
        '''
        # Desenha o campo
        drawBoard(board)
        # Desenha a pontuação e o nivel
        drawStatus(score, level, clearLines)
        # Desenha a próxima peça
        drawNextPiece(nextPiece)

        # Se tiver uma peça caindo
        if fallingPiece != None:
            # Desenha a peça caindo
            drawPiece(fallingPiece)

        # Desenha o display do inimigo
        drawDisplayEnemy(board, score, level, clearLines, nextPiece, fallingPiece, "FELIPE")
       
        # Atualiza o displa
        pygame.display.update()

        # Espera o tempo do próximo Frame
        FPSCLOCK.tick(FPS)

'''
Função que retorna o campo do jogo.
'''
def getBlankBoard():
    
    # Inicializa o campo
    board = []

    # Inicializa o campo sem peças
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)

    # Retorna o campo
    return board

'''
Função que retorna o nivel que o jogador e
e o tempo para cair a próxima peça.
'''
def calculateLevelAndFallFreq(clearLines):
    
    #level = int(clearLines/10);
    level = 99

    if (level >= 0 and level <= 8):
        fallFreq = (48 - 5*level)/FPS
    elif (level == 9):
        fallFreq = 6/FPS
    elif (level >= 10 and level <= 12):
        fallFreq = 5/FPS
    elif (level >= 13 and level <= 15):
        fallFreq = 4/FPS
    elif (level >= 16 and level <= 18):
        fallFreq = 3/FPS
    elif (level >= 19 and level <= 28):
        fallFreq = 2/FPS
    elif (level >= 29):
        fallFreq = 1/FPS

    return level, fallFreq

'''
Função que retorna uma nova peça
'''
def getNewPiece():

    # Atualiza para uma nova seed
    random.seed()
    # Retorna uma das formas das peças
    shape = random.choice(list(PIECES.keys()))

    # Nova peça é um dict:
    newPiece = {'shape': shape, # Com formato
                'rotation': 0, # Rotação
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2), # Posição de x no campo
                'y': -2, # Posição de y no campo
                'color': getColor(shape)} # Cor aleatória

    # Retorna a nova peça
    return newPiece

'''
Função que retorna a cor da peça
'''
def getColor(shape):
    
    # Se for a peça T, O ou I, retorna a cor 'A'
    if shape == 'T' or shape == 'O' or shape == 'I':
        return 0

    # Se for a peça J ou S, retorna a cor 'B' 
    if shape == 'J' or shape == 'S':
        return 1

    # É a peça Z ou L, retorna a cor 'C'
    return 2

'''
Função que verifica se a peça está em uma posição valida
'''
def isValidPosition(board, piece, adjX=0, adjY=0):
    
    # Percorre todas as posições do tabuleiro
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):

            # Confere se a peça está a cima do campo
            isAboveBoard = y + piece['y'] + adjY < 0

            # Se a peça estiver a cima do campo ou estiver em uma posição livre, pula pra proxima iteração
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue

            # Se a peça não estiver no campo, retorna falso
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False

            # Se a peça estiver estiver em uma posição não livre, retorna falso
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False

    # Se passou em todos testes, a posição é valida
    return True

'''
Função que verifica se a peça está no campo
'''
def isOnBoard(x, y):
    # x tem que se ser maior ou igual a 0
    # x tem que ser menor a largura do campo
    # y tem que ser menor que a altura do campo
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT

'''
Função que adiciona a peça ao tabuleiro
'''
def addToBoard(board, piece):
    
    # Passa por todas as posições do TEMPLATE da peça
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            # Se o template não for vazio, pinta a peça
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']

'''
Função que remove as linhas completadas, movendo todo o campo
a cima das linhas pra baixo e retornando a quantidade de linhas
'''
def removeCompleteLines(board):
    
    # Número de linhas removidas = 0
    numLinesRemoved = 0

    # Inicializa do fundo do campo
    y = BOARDHEIGHT - 1 

    # Enquanto não chega no topo
    while y >= 0:

        # Verifica se a linha está completa
        if isCompleteLine(board, y):
            
            # Loop da linha atual até todos de cima
            for pullDownY in range(y, 0, -1):

                # Passa as linhas um andar abaixo
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]

            # A linha mais alta é apagada
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            
            # Aumenta o número de linhas removidas
            numLinesRemoved += 1
        
        # Se a linha não está completa
        else:
            # Sobre uma posição
            y -= 1 

    # Pontuação pelas linhas eliminadas
    score = 0
    if numLinesRemoved == 1:
        score = 40 * (level + 1)
    elif numLinesRemoved == 2:
        score = 100 * (level + 1)
    elif numLinesRemoved == 3:
        score = 300 * (level + 1)
    elif numLinesRemoved == 4:
        score = 1200 * (level + 1)

    # Retorna uma tupla com os pontos e a 
    # quantidade de linhas removidas
    return (score, numLinesRemoved)

'''
Função que verifica se uma linha está completa
'''
def isCompleteLine(board, y):
    
    # Passa por toda a linha
    for x in range(BOARDWIDTH):

        # Se alguma for vazia, não está completa
        if board[x][y] == BLANK:
            return False

    # Se passou nos testes, está completa
    return True

'''
Função que desenha o campo do jogo
'''
def drawBoard(board):
    
    # Preenche o interior do campo com a cor do fundo
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))

    # Pinta cada quadrado separadamente
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])

'''
Função que pinta um quadrado da peça
'''
def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    
    # Se a cor for vazio, nao pinta
    if color == BLANK:
        return

    # Se pixelx e pixely não foi especificado,
    # retorna a posição correta no tabuleiro
    if pixelx == None and pixely == None:
        # Converte a posição do campo para a posição dos Pixels
        pixelx, pixely = convertToPixelCoords(boxx, boxy)

    # Pinta o quadrado com a textura correta
    DISPLAYSURF.blit(BLOCKS[level % 10][color], (pixelx + 1, pixely + 1))

'''
Função que converte a Posição do campo
para a posição do Pixel na tela
'''
def convertToPixelCoords(boxx, boxy):
    # Retorna a posição do Pixel
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

'''
Função que desenha o Status do jogo
contendo a Pontuação e o Nível
'''
def drawStatus(score, level, lines):
    

    pointSurf = ''

    # DIFERENÇA DE PONTUAÇAO
    diff = 0
    if diff < 0:
        diff = '-' + format(abs(diff), '06d')
        pointSurf = POINTSFONT.render('%s' %diff, False, RED)
    else:
        diff = '+' + format(abs(diff), '06d')
        pointSurf = POINTSFONT.render('%s' %diff, False, GREEN)
    pointRect = pointSurf.get_rect()
    pointRect.bottomright = (348, 105)
    DISPLAYSURF.blit(pointSurf, pointRect)

    # PONTUAÇÃO
    point2Surf = POINTSFONT.render('%s' %format(score, '06d'), False, WHITE)
    point2Rect = point2Surf.get_rect()
    point2Rect.bottomright = (348, 80)
    DISPLAYSURF.blit(point2Surf, point2Rect)

    # Pinta a string SCORE 
    scoreSurf = SCOREFONT.render('SCORE', False, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (232, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    # Pinta a string LINE
    linesSurf = LINESFONT.render('LINE', False, WHITE)
    linesRect = linesSurf.get_rect()
    linesRect.topleft = (180, 117)
    DISPLAYSURF.blit(linesSurf, linesRect)

    # Pinta a quantidade de Linhas
    qtLinesSurf = SCOREFONT.render('%s' %format(lines, '03d'), False, WHITE)
    qtLinesRect = qtLinesSurf.get_rect()
    qtLinesRect.topleft = (190, 140)
    DISPLAYSURF.blit(qtLinesSurf, qtLinesRect)

    # Pinta a string LEVEL
    levelSurf = LINESFONT.render('LVL', False, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (92,602)
    DISPLAYSURF.blit(levelSurf, levelRect)

    # Pinta o Nível
    levelSurf = LINESFONT.render('%s' %format(level, '02d'), False, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.center = (120,640)
    DISPLAYSURF.blit(levelSurf, levelRect)

    # Pinta os Rounds
    DISPLAYSURF.blit(ROUNDS[0], (235, 632))    

    # Pinta o nome
    levelSurf = LINESFONT.render('%s' %NAME, False, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.center = (XMARGIN + 100,619)
    DISPLAYSURF.blit(levelSurf, levelRect)

'''
Função que desenha a próxima peça
'''
def drawNextPiece(piece):
    
    # Pinta a próxima peça
    drawPiece(piece, pixelx=280, pixely=85)

'''
Função que desenha uma peça na Tela
'''
def drawPiece(piece, pixelx=None, pixely=None):
    
    # Qual peça precisa ser pintada
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    
    # Se a posição não foi especificada
    if pixelx == None and pixely == None:
        # Pega a posição armazenada na peça
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # Percorre por todo o template da peça
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            # Se a posição não for vazia
            if shapeToDraw[y][x] != BLANK:
                # Pinta a peça na tela
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

#######################################################################################

'''
Função que faz o processo de desenho do Display do adversário
'''
def drawDisplayEnemy(board, score, level, clearLines, nextPiece, fallingPiece, name):
    # Desenha o campo inimigo
    drawBoardEnemy(board)
    # Desenha a pontuação e o nivel do inimigo
    drawStatusEnemy(score, level, clearLines, name)
    # Desenha a próxima peça do inimigo 
    drawNextPieceEnemy(nextPiece)

    # Se tiver uma peça caindo do inimigo
    if fallingPiece != None:
        # Desenha a peça caindo do inimigo
        drawPieceEnemy(fallingPiece)    

'''
Função que desenha o campo do inimigo
'''
def drawBoardEnemy(board):
    
    # Preenche o interior do campo com a cor do fundo
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (WINDOWWIDTH -XMARGIN - 200, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))

    # Pinta cada quadrado separadamente
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBoxEnemy(x, y, board[x][y])

'''
Função que desenha os Status do inimigo
'''
def drawStatusEnemy(score, level, lines, name):
    
    # DIFERENÇA DE PONTUAÇAO

    pointSurf = ''

    # DIFERENÇA DE PONTUAÇAO
    diff = 0
    if diff < 0:
        diff = '-' + format(abs(diff), '06d')
        pointSurf = POINTSFONT.render('%s' %diff, False, RED)
    else:
        diff = '+' + format(abs(diff), '06d')
        pointSurf = POINTSFONT.render('%s' %diff, False, GREEN)
    pointRect = pointSurf.get_rect()
    pointRect.bottomright = (WINDOWWIDTH - XMARGIN - 23, 105)
    DISPLAYSURF.blit(pointSurf, pointRect)

    # PONTUAÇÃO
    point2Surf = POINTSFONT.render('%s' %format(score, '06d'), False, WHITE)
    point2Rect = point2Surf.get_rect()
    point2Rect.bottomright= (WINDOWWIDTH - XMARGIN - 23, 80)
    DISPLAYSURF.blit(point2Surf, point2Rect)

    # Pinta a string SCORE 
    scoreSurf = SCOREFONT.render('SCORE', False, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topright = (WINDOWWIDTH - 213, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    # Pinta a string LINE
    linesSurf = LINESFONT.render('LINE', False, WHITE)
    linesRect = linesSurf.get_rect()
    linesRect.topright = (WINDOWWIDTH - 285, 117)
    DISPLAYSURF.blit(linesSurf, linesRect)

    # Pinta a quantidade de Linhas
    qtLinesSurf = SCOREFONT.render('%s' %format(lines, '03d'), False, WHITE)
    qtLinesRect = qtLinesSurf.get_rect()
    qtLinesRect.topright = (WINDOWWIDTH -  295, 140)
    DISPLAYSURF.blit(qtLinesSurf, qtLinesRect)

    # Pinta a string LEVEL
    levelSurf = LINESFONT.render('LVL', False, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topright = (WINDOWWIDTH - 89,602)
    DISPLAYSURF.blit(levelSurf, levelRect)

    # Pinta o Nível
    levelSurf = LINESFONT.render('%s' %format(level, '02d'), False, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.center = (WINDOWWIDTH - 117,640)
    DISPLAYSURF.blit(levelSurf, levelRect)

    # Pinta os Rounds
    DISPLAYSURF.blit(ROUNDS[0], (WINDOWWIDTH - 300, 632))    

    # Pinta o nome
    levelSurf = LINESFONT.render('%s' %name, False, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.center = (WINDOWWIDTH -XMARGIN - 100,619)
    DISPLAYSURF.blit(levelSurf, levelRect)

'''
Função que desenha a próxima peça do inimigo
'''
def drawNextPieceEnemy(piece):

    # Pinta a próxima peça
    drawPiece(piece, pixelx=WINDOWWIDTH - 260, pixely=85)

'''
Função que desenha a próxima peça do inimigo
'''
def drawPieceEnemy(piece, pixelx=None, pixely=None):
    
   # Qual peça precisa ser pintada
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    
    # Se a posição não foi especificada
    if pixelx == None and pixely == None:
        # Pega a posição armazenada na peça
        pixelx, pixely = convertToPixelCoordsEnemy(piece['x'], piece['y'])

    # Percorre por todo o template da peça
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            # Se a posição não for vazia
            if shapeToDraw[y][x] != BLANK:
                # Pinta a peça na tela
                drawBoxEnemy(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

'''
Função que converte a posição do campo inimigo
para a posição do Pixel na tela
'''
def convertToPixelCoordsEnemy(boxx, boxy):
    # Retorna a posição do Pixel
    return (WINDOWWIDTH - XMARGIN - 200 + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

'''
Função que desenha um quadrado das peças do inimigo
'''
def drawBoxEnemy(boxx, boxy, color, pixelx=None, pixely=None):
    
    # Se a cor for vazio, nao pinta
    if color == BLANK:
        return

    # Se pixelx e pixely não foi especificado,
    # retorna a posição correta no tabuleiro
    if pixelx == None and pixely == None:
        # Converte a posição do campo para a posição dos Pixels
        pixelx, pixely = convertToPixelCoordsEnemy(boxx, boxy)

    # Pinta o quadrado com a textura correta
    DISPLAYSURF.blit(BLOCKS[level % 10][color], (pixelx + 1, pixely + 1))