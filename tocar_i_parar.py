import numpy as np
import random
import pygame
import sys
import math

#   INICIALITZACIO DE VARIABLES

BLUE = (0,0,255)     # Defincio del color blau
BLACK = (0,0,0)      # Defincio del color negre
RED = (255,0,0)      # Defincio del color vermell
YELLOW = (255,255,0) # Defincio del color groc
GREY = (220,220,220) # Defincio del color gris
GREEN = (0,128,0)    # Defincio del color verd

ROW_COUNT = 6        # Numero de files del tauler
COLUMN_COUNT = 7     # Numero de columnes del tauler

PLAYER = 0           # Codi del jugador huma
AI = 1               # Codi del jugador AI

EMPTY = 0            # Codi posicio lliure
PLAYER_PIECE = 1     # Codi posicio jugador huma
AI_PIECE = 2         # Codi posicio jugador AI
BURNED_PIECE = 3     # Codi posicio "cremada"
WINNER_PIECE = 4     # Codi posicio guanyadora
DEPH_LEVEL = ROW_COUNT * COLUMN_COUNT # Limit de profunditat de l'arbre
DEPTH_LEVEL = 5 #ficar la profunditat de l'arbre

# DEFINICIO DE MODULS

def crear_tauler():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def moure_fitxa(board, row, col, piece):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == piece:
                board[r][c] = BURNED_PIECE
    board[row][col] = piece

def es_posicio_valida(board, row, col, player):
    valid = 0
    if (board[row][col] == player) or (board[row][col] == BURNED_PIECE): # Propi o ja cremat invalida
        valid = 0
    elif ((row < ROW_COUNT-1) and (board[row+1][col] == player)) or ((row > 0) and (board[row-1][col] == player)): # Mateixa columna, fila anterior o posterior
        valid = 1
    elif ((col < COLUMN_COUNT-1) and (board[row][col+1] == player)) or ((col > 0) and (board[row][col-1] == player)): # Mateixa columna, fila anterior o posterior
        valid = 1
    return valid

def mostra_tauler(board):
    print(np.flip(board, 0))

def jugada_guanyadora(board, player):
    winning = True  # Verifica posicions guanyadores
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if (player == PLAYER_PIECE and board[r][c] == AI_PIECE) or (player == AI_PIECE and board[r][c] == PLAYER_PIECE):
                    winning = False
    return winning
  
def es_node_terminal(board):
    return jugada_guanyadora(board, PLAYER_PIECE) or jugada_guanyadora(board, AI_PIECE) or len(recupera_posicions_valides(board, PLAYER_PIECE)) == 0 or len(recupera_posicions_valides(board, AI_PIECE)) == 0

def avalua_estat(board, piece): #per calcular la puntuacio i la heuristica
    score = 0
    # Aquest modul caldria ser programat per avaluar cada estat
    # Us deixo un funcio d exemple, pero l'heu de modificar/millorar
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if (board[r][c] == PLAYER_PIECE):
                break
    for a in range(COLUMN_COUNT):
        for b in range(ROW_COUNT):
            if (board[b][a] == AI_PIECE):
                break
    return score # Retorna puntuacio de l'estat

def minimax(board, depth, alpha, beta, maximizingPlayer):
    # Aquest modul caldria ser programat per avaluar cada estat
    # Us deixo un funcio d exemple, pero l'heu de modificar/millorar
    if maximizingPlayer:
        posicions_valides = recupera_posicions_valides(board, AI_PIECE)
    else:
        posicions_valides = recupera_posicions_valides(board, PLAYER_PIECE)

    es_terminal = es_node_terminal(board)
    if depth == 0 or es_terminal: # La profunditat es decreixent (resta un)
        if es_terminal:
            if jugada_guanyadora(board, AI_PIECE):
                return (None,None, 0)
            elif jugada_guanyadora(board, PLAYER_PIECE):
                return (None,None, 0)
            else: # Joc acabat, no hi ha mes moviments valids pendents (ofegat)
                return (None,None, 0) 
        else: # Maxim nivell de produnditat, no terminal
            return (None, None, 0)

    if maximizingPlayer: # Poda alpha beta jugador MAX
        value = 0
        position = random.choice(posicions_valides) # Trio una posicio a l'atzar per comencar
        for pos in posicions_valides: # Recorro totes les posicions valides
            b_copy = board.copy()     # Preparo nou tauler
            moure_fitxa(b_copy, ROW_COUNT-pos[0]-1, pos[1], AI_PIECE)   # Mou a nova posicio valida, dins del nou tauler
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[2] 
        return position[0], position[1], value
    else: # Poda alpha beta del jugador MIN
        value = 0
        position = random.choice(posicions_valides)
        for pos in posicions_valides:
            b_copy = board.copy()
            moure_fitxa(b_copy, ROW_COUNT-pos[0]-1, pos[1], PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[2] # retorna la posicio score de (None, None, 0)
        return position[0], position[1], value

def recupera_posicions_valides(board, player):
    posicions_valides = []
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if es_posicio_valida(board, row, col, player):
                posicions_valides.append([ROW_COUNT-row-1,col])
    return posicions_valides

def dibuixa_tauler(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
    	for r in range(ROW_COUNT):		
    		if board[r][c] == PLAYER_PIECE:
    			pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    		elif board[r][c] == AI_PIECE: 
    			pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    		elif board[r][c] == BURNED_PIECE: 
    			pygame.draw.circle(screen, GREY, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    		elif board[r][c] == WINNER_PIECE: 
    			pygame.draw.circle(screen, GREEN, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()
    
#idjugada unica en cada partida i en cada jugada

"""
********************************
*     JOC DEL TOCAR I PARAR     *
********************************
"""
board = crear_tauler()
mostra_tauler(board)
game_over = False

pygame.init()
SQUARESIZE = 100 # Quadrats de 100 pixels quadrats

width = COLUMN_COUNT * SQUARESIZE
height = ROW_COUNT * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5) # Radi fitxa

myfont = pygame.font.SysFont("monospace", 75)
turn = PLAYER # Obligo a comencar a jugador huma, es pot canvar (random)
start = [0,0]
#
# Cal millorar la situacio inicial de les fitxes, canviar el random perue no surtin les fitxes al mateix lloc
#
start[0] = random.randint(0, ROW_COUNT-1)
start[1] = random.randint(0, COLUMN_COUNT-1)
moure_fitxa(board, start[0], start[1], PLAYER_PIECE) # Fitxa humana

start[0] = random.randint(0, ROW_COUNT-1)
start[1] = random.randint(0, COLUMN_COUNT-1)
moure_fitxa(board, start[0], start[1], AI_PIECE) # Fitxa IA

screen = pygame.display.set_mode(size)
dibuixa_tauler(board)
pygame.display.update()

mostra_tauler(board)

while not game_over: # Mentre hi ha partida
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if turn == PLAYER:      # Pregunta a jugador huma la seva jugada
                posx = event.pos[0] # Recupera posicio lick columna 
                posy = event.pos[1] # Recupera posicio click columna

                row = int(math.floor((ROW_COUNT*SQUARESIZE-posy)/SQUARESIZE)) # Cal invertir el calcul y!
                col = int(math.floor(posx/SQUARESIZE))
                
                if es_posicio_valida(board, row, col, PLAYER_PIECE):
                    moure_fitxa(board, row, col, PLAYER_PIECE)

                    if jugada_guanyadora(board, PLAYER_PIECE):
                        moure_fitxa(board, row, col, WINNER_PIECE)
                        mostra_tauler(board)
                        dibuixa_tauler(board)
                        
                        label = myfont.render("Guanya huma!", 1, RED)
                        screen.blit(label, (40,10))
                        pygame.display.flip() # la matriu esta al reves dels pixels, per aixo flip
                        
                        game_over = True
                    else:
                        mostra_tauler(board)
                        dibuixa_tauler(board)
                    turn += 1
                    turn = turn % 2 # canviar el torn del jugador

    if turn == AI and not game_over: # Demana a jugador IA la seva jugada
        if not es_node_terminal(board): # Comprovo si hi ha jugava viable, o si ja es taules per ofegament
            row, col, minimax_score = minimax(board, DEPH_LEVEL, 0, 0, True) # 40 mov max. (no imp), els nivell van al reves, comencem a max i acabem a 0, canviar valor alpha beta (0,0), comença max.
            if es_posicio_valida(board, ROW_COUNT-row-1, col, AI_PIECE): # per rebaixar el nivell de complexitat
                pygame.time.wait(500)
                moure_fitxa(board, ROW_COUNT-row-1, col, AI_PIECE)

                if jugada_guanyadora(board, AI_PIECE):
                    moure_fitxa(board, ROW_COUNT-row-1, col, WINNER_PIECE)
                    mostra_tauler(board)
                    dibuixa_tauler(board)

                    label = myfont.render("Guanya IA!", 1, YELLOW)
                    screen.blit(label, (40,10))
                    pygame.display.flip()

                    game_over = True
                else:
                    mostra_tauler(board)
                    dibuixa_tauler(board)
                turn += 1
                turn = turn % 2
        else:
            label = myfont.render("Taules!", 1, GREEN)
            screen.blit(label, (40,10))
            pygame.display.flip()

            game_over = True
    if game_over:
        pygame.time.wait(3000)
