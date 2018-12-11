#!/usr/bin/python
# -*- coding: utf-8 -*-

# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, time, pygame, sys
from pygame.locals import *

FPS = 60
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = BLACK
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color

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
I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

# Peça O
O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

# Peça J
J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

# Peça L
L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

# Peça T
T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
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

'''
Função main.
'''
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    
    # Inicializa o pygame
    pygame.init()
    # Tempo entre os FPS
    FPSCLOCK = pygame.time.Clock()
    # Seta o tamanho da tela
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    # Fonte para letras pequenas
    BASICFONT = pygame.font.Font('Fonts/ARCADECLASSIC.TTF', 18)
    # Fonte para letras grandes
    BIGFONT = pygame.font.Font('Fonts/ARCADECLASSIC.TTF', 100)
    # Seta o nome da Janela
    pygame.display.set_caption('Classic Tetris Multiplayer')

    # Inicializa a tela inicial
    showTextScreen('TETRIS')

    # Loop do jogo
    while True:
        # Roda o jogo
        runGame()
        # Morreu, dá a tela de GAME OVER
        showTextScreen('GAME OVER')

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

    # Calcula o nivel e a frequência de queda
    level, fallFreq = calculateLevelAndFallFreq(score)

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
                # Remove as peças completadas adicionando a pontuação
                score += removeCompleteLines(board)
                # Calcula o novo nivel e frequência de queda
                level, fallFreq = calculateLevelAndFallFreq(score)
                # Não tem nenhuma peça caindo
                fallingPiece = None

            # A peça não chegou numa posição não válida
            # desce a peça uma posição pra baixo
            else:
                
                # Aumenta uma posição pra baixo
                fallingPiece['y'] += 1
                # Atualiza o ultimo tempo de queda
                lastFallTime = time.time()

        # Desenha o fundo na tela
        DISPLAYSURF.fill(BGCOLOR)
        # Desenha o campo
        drawBoard(board)
        # Desenha a pontuação e o nivel
        drawStatus(score, level)
        # Desemja a próxima peça
        drawNextPiece(nextPiece)

        # Se tiver uma peça caindo
        if fallingPiece != None:
            # Desenha a peça caindo
            drawPiece(fallingPiece)

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
def calculateLevelAndFallFreq(score):
    
    # Cálculo do nivel
    level = int(score / 10) + 1
    # Cálculo do tempo de queda da peça
    fallFreq = 0.27 - (level * 0.02)

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
                'rotation': random.randint(0, len(PIECES[shape]) - 1), # Rotação
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2), # Posição de x no campo
                'y': -2, # Posição de y no campo
                'color': random.randint(0, len(COLORS)-1)} # Cor aleatória

    # Retorna a nova peça
    return newPiece

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

    # Retorna o número de linhas removidas
    return numLinesRemoved

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
    
    # Desenha a borda em volta do campo
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

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

    # Desenha o retângulo com sua cor
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    # Desenha o retângulo com sua cor clara
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

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
def drawStatus(score, level):
    
    # Pinta a string SCORE com a sua pontuação
    scoreSurf = BASICFONT.render('SCORE %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    # Pinta a string LEVEL com seu nível
    levelSurf = BASICFONT.render('LEVEL %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(levelSurf, levelRect)

'''
Função que desenha a próxima peça
'''
def drawNextPiece(piece):
    
    # Pinta a string NEXT na tela
    nextSurf = BASICFONT.render('NEXT', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)

    # Pinta a próxima peça
    drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)

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


