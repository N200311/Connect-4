#importing libraries
import numpy as np
import pygame 
import sys
import math
import random

#colors
Light = (255,248,220)
Grey = (139,136,120)
Aqua = (102,205,170)
Crimson = (220,20,60)

#Global variables
NUM_ROW = 6
NUM_COL = 7
HUMAN_PLAYER = 0
AI_PLAYER = 1
HUMAN_PIECE = 1
AI_PIECE = 2
EMPTY_SPACE = 0
PATTERN_LENGTH = 4

#to create a matrix full of zeros with dimensions 6 NUM_ROW and 7 NUM_COL
def BOARD_MATRIX(): 
      board = np.zeros((NUM_ROW,NUM_COL)) 
      return board

#to determine if the location in this column is legitimate or not; if it is, we will drop the piece here; if not, it's  invalid.
def EMPTY_COLUMN(board,COL): 
      return board[NUM_ROW-1][COL] == 0

#to determine if the location in this row is legitimate or not; if it is, we will drop the piece here; if not,  it's invalid.
def EMPTY_ROW(board, COL): 
      for i in range(NUM_ROW):
            if board[i][COL] == 0:
                  return i

#in this function we release the piece in the place the player chose.
def RELEASE_PIECE(board, ROW, COL, piece): 
      board[ROW][COL] = piece
      return piece
       
# start the playing from the bottom of the board not the top
def FLIP_MATRIX(board): 
      print(np.flip(board, 0))

# check the winning move or piece in horizontal, vertical, negative and positive slope 
def win(board,piece): 
      #horizontal WIN
      for c in range(NUM_COL-3):
            for r in range(NUM_ROW):
                  if board[r][c]==piece and board[r][c+1]==piece and board[r][c+2]==piece and board[r][c+3]==piece:
                        return True
      #vitical WIN
      for c in range(NUM_COL):
            for r in range(NUM_ROW-3):
                  if board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece:
                        return True
      #positive diagonal
      for c in range(NUM_COL-3):
            for r in range(NUM_ROW-3):
                  if board[r][c]==piece and board[r+1][c+1]==piece and board[r+2][c+2]==piece and board[r+3][c+3]==piece:
                        return True
      #negative diagonal
      for c in range(NUM_COL-3):
            for r in range(3,NUM_ROW):
                  if board[r][c]==piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and board[r-3][c+3]==piece:
                        return True

#Calculates the score througout the game 
def CHECK_PATTERN_SCORE(PATTERN, piece): 
      SCORE = 0
      RIVAL_PIECE = HUMAN_PIECE
      if piece == HUMAN_PIECE:
            RIVAL_PIECE = AI_PIECE

      if PATTERN.count(piece) == 4:
            SCORE = SCORE + 100
      elif PATTERN.count(piece) == 3 and PATTERN.count(EMPTY_SPACE) == 1:
            SCORE = SCORE + 5
      elif PATTERN.count(piece) == 2 and PATTERN.count(EMPTY_SPACE) == 2:
            SCORE = SCORE + 2

      if PATTERN.count(RIVAL_PIECE) == 3 and PATTERN.count(EMPTY_SPACE) == 1:
            SCORE = SCORE - 4
      
      return SCORE

#Checks who wins through their pattern in the game 
def CHECK_WINNING_PATTERN(board, piece): 
      SCORE = 0
      #center column
      CENTER_LIST = [int(i) for i in list(board[:,NUM_COL//2])]
      CENTER_PIECE = CENTER_LIST.count(piece)
      SCORE = SCORE + CENTER_PIECE * 3

      #horizontal
      for row in range(NUM_ROW):
            ROW_LIST = [int(i) for i in list(board[row,:])]
            for col in range(NUM_COL-3):
                  PATTERN = ROW_LIST[col:col+PATTERN_LENGTH]
                  SCORE = SCORE + CHECK_PATTERN_SCORE(PATTERN, piece)
      
      #vertical
      for col in range(NUM_COL):
            COL_LIST = [int(i) for i in list(board[:,col])]
            for row in range(NUM_ROW-3):
                  PATTERN = COL_LIST[row:row+PATTERN_LENGTH]
                  SCORE = SCORE + CHECK_PATTERN_SCORE(PATTERN, piece)

      #positive diagonal
      for row in range(NUM_ROW-3):
            for col in range(NUM_COL-3):
                  PATTERN = [board[row+i][col+i] for i in range(PATTERN_LENGTH)]
                  SCORE = SCORE + CHECK_PATTERN_SCORE(PATTERN, piece)
      
      #negative diagonal
      for row in range(NUM_ROW-3):
            for col in range(NUM_COL-3):
                  PATTERN = [board[row+3-i][col+i] for i in range(PATTERN_LENGTH)]
                  SCORE = SCORE + CHECK_PATTERN_SCORE(PATTERN, piece)
      return SCORE

#in this function we check if the node is terminal for the minimax and in our game it's terminal if one the players won or if the board is full and there is no more moves to make.
def CHECK_IF_TERMINAL(board): 
      return win(board, AI_PIECE) or win(board, HUMAN_PIECE) or len(CHECK_EMPTY(board)) == 0

#this the minimax algorithm function, in it AI calculates the best move to make and how far in depth it looks to speculate the human player's moves.
def MINIMAX(board, depth, alpha, beta, MaximizingPlayer): 
      FREE_SPACE = CHECK_EMPTY(board)
      terminal = CHECK_IF_TERMINAL(board)
      if depth == 0 or terminal:
            if terminal:
                  if win(board, AI_PIECE):
                        return (None, 100000000000000)
                  elif win(board, HUMAN_PIECE):
                        return (None, -100000000000000)
                  else:
                        return (None, 0)
            else:
                  return (None, CHECK_WINNING_PATTERN(board, AI_PIECE))

      if MaximizingPlayer:

            VALUE = -math.inf
            column = random.choice(FREE_SPACE)
            for col in FREE_SPACE:
                  row = EMPTY_ROW(board, col)
                  NEW_BOARD = board.copy()
                  RELEASE_PIECE(NEW_BOARD, row, col, AI_PIECE)
                  NEW_SCORE = MINIMAX(NEW_BOARD, depth-1, alpha, beta, False)[1]

                  if NEW_SCORE > VALUE:
                        VALUE = NEW_SCORE
                        column = col
                  alpha = max(alpha, VALUE)

                  if alpha >= beta:
                        break

            return column,VALUE

      else:
            
            VALUE = math.inf
            column = random.choice(FREE_SPACE)
            for col in FREE_SPACE:
                  row = EMPTY_ROW(board, col)
                  NEW_BOARD = board.copy()
                  RELEASE_PIECE(NEW_BOARD, row, col, HUMAN_PIECE)
                  NEW_SCORE = MINIMAX(NEW_BOARD, depth-1, alpha, beta, True)[1]

                  if NEW_SCORE < VALUE:
                        VALUE = NEW_SCORE
                        column = col
                  beta = min(beta, VALUE)

                  if alpha >= beta:
                        break

            return column,VALUE

#Rerurns a list of Empty columns
def CHECK_EMPTY(board): 
      FREE_SPACE  = []
      for col in range(NUM_COL):
            if EMPTY_COLUMN(board, col):
                  FREE_SPACE.append(col)
      return FREE_SPACE

#picks a random column from the empty columns and checks each row of that column, then checks the highest score of each place and picks the highest score.
def BEST_MOVE(board, piece): 
      FREE_SPACE = CHECK_EMPTY(board)
      BEST_SCORE = -10000
      BEST_COL = random.choice(FREE_SPACE)
      for col in FREE_SPACE:
            row = EMPTY_ROW(board, col)
            NEW_BOARD = board.copy()
            RELEASE_PIECE(NEW_BOARD, row, col, piece)
            SCORE = CHECK_WINNING_PATTERN(NEW_BOARD, piece)
            if SCORE > BEST_SCORE:
                  BEST_SCORE = SCORE
                  BEST_COL = col            
      return BEST_COL

#in this function we design the shape of the board and the shape of the circles for each player's piece
def DESIGN_BOARD(board): 
      for c in range(NUM_COL):
            for r in range(NUM_ROW):
                  pygame.draw.rect(SCREEN, Light, (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                  pygame.draw.circle(SCREEN, Grey, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)),RADIUS)
      
      for col in range(NUM_COL):
            for row in range(NUM_ROW):
                  if board[row][col] == HUMAN_PIECE:
                        pygame.draw.circle(SCREEN, Aqua, (int(col*SQUARE_SIZE+SQUARE_SIZE/2), HEIGHT-int(row*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
                  if board[row][col]==AI_PIECE:
                        pygame.draw.circle(SCREEN, Crimson, (int(col*SQUARE_SIZE+SQUARE_SIZE/2), HEIGHT-int(row*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
      pygame.display.update()


board = BOARD_MATRIX()
FLIP_MATRIX(board)
GAME_OVER = False
YOUR_MOVE = random.randint(HUMAN_PLAYER,AI_PLAYER)

#initiliazing pygame 
pygame.init()

SQUARE_SIZE = 90 

WIDTH = NUM_COL * SQUARE_SIZE
HEIGHT = (NUM_ROW+1) * SQUARE_SIZE

SIZE = (WIDTH,HEIGHT)

RADIUS = int(SQUARE_SIZE/2 - 5)

SCREEN = pygame.display.set_mode(SIZE)
DESIGN_BOARD(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 64)


while not GAME_OVER:

      for event in pygame.event.get():
            if event.type == pygame.QUIT:
                  sys.exit()
            if event.type == pygame.MOUSEMOTION:
                  pygame.draw.rect(SCREEN, Grey,(0,0,WIDTH,SQUARE_SIZE))
                  XPOS = event.pos[0]
                  if YOUR_MOVE == HUMAN_PLAYER:
                        pygame.draw.circle(SCREEN,Aqua,(XPOS,int(SQUARE_SIZE/2)),RADIUS)
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                  pygame.draw.rect(SCREEN, Grey,(0,0,WIDTH,SQUARE_SIZE))
                  if YOUR_MOVE == HUMAN_PLAYER:
                        XPOS = event.pos[0]
                        COL = int(math.floor(XPOS/SQUARE_SIZE))
                        if EMPTY_COLUMN(board, COL):
                              ROW = EMPTY_ROW(board, COL)
                              RELEASE_PIECE(board,ROW,COL,HUMAN_PIECE)
                              if win(board,HUMAN_PIECE):
                                    label = myfont.render("Player One Wins!", 1, Aqua)
                                    SCREEN.blit(label,(20,10))
                                    GAME_OVER = True
                              YOUR_MOVE = YOUR_MOVE + 1
                              YOUR_MOVE = YOUR_MOVE % 2
                              FLIP_MATRIX(board)
                              DESIGN_BOARD(board)
                              if GAME_OVER:
                                pygame.time.wait(3000)
      if YOUR_MOVE == AI_PLAYER and not GAME_OVER:
            
            COL, MINIMAX_SCORE = MINIMAX(board, 4, -math.inf, math.inf, True)
            if EMPTY_COLUMN(board, COL):
                  ROW = EMPTY_ROW(board, COL)
                  RELEASE_PIECE(board,ROW,COL,AI_PIECE)
                  if win(board,AI_PIECE):
                        label = myfont.render("Player Two Wins!", 2,Crimson)
                        SCREEN.blit(label,(20,10))
                        GAME_OVER = True
                  YOUR_MOVE = YOUR_MOVE + 1
                  YOUR_MOVE = YOUR_MOVE % 2
                  FLIP_MATRIX(board)
                  DESIGN_BOARD(board)
      if GAME_OVER:
            pygame.time.wait(3000)
