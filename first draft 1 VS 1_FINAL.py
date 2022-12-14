#importing libraries
import numpy as np
import pygame 
import sys
import math

#colors
Light = (255,248,220)
Grey = (139,136,120)
Aqua = (102,205,170)
Crimson = (220,20,60)

#Global variables
NUM_ROW=6
NUM_COL=7

#to create a matrix full of zeros with dimensions 6 NUM_ROW and 7
def BOARD_MATRIX(): 
      board = np.zeros((NUM_ROW,NUM_COL)) 
      return board

# to see if the location is valid or not ,if true : we will drop the piece here ,if not this mean the col is not valid
def EMPTY_COLUMN(board,COL):
      return board[NUM_ROW-1][COL]==0

#to get next to the next open row
def EMPTY_ROW(board, COL): 
      for i in range(NUM_ROW):
            if board[i][COL]==0:
                  return i

# to make the piece released in the row that the player chooses
def RELEASE_PIECE(board, ROW, COL, piece): 
      board[ROW][COL] = piece
      return piece
       
#to reverse the order of array elements by keeping the shape of the array along a specified axis"np.flip"
def FLIP_MATRIX(board): 
      print(np.flip(board, 0))

# check the winning move or piece in horizontal, vertical, negative and positive slope 
def win(board,piece): 
      #horizontal
      for c in range(NUM_COL-3):
            for r in range(NUM_ROW):
                  if board[r][c]==piece and board[r][c+1]==piece and board[r][c+2]==piece and board[r][c+3]==piece:
                        return True
      #virtical
      for c in range(NUM_COL):
            for r in range(NUM_ROW-3):
                  if board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece:
                        return True
      #positive line
      for c in range(NUM_COL-3):
            for r in range(NUM_ROW-3):
                  if board[r][c]==piece and board[r+1][c+1]==piece and board[r+2][c+2]==piece and board[r+3][c+3]==piece:
                        return True
      #negative line
      for c in range(NUM_COL-3):
            for r in range(3,NUM_ROW):
                  if board[r][c]==piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and board[r-3][c+3]==piece:
                        return True

#In this function, we create the board's geometry as well as the shapes of the circles for each player's piece.
def DESIGN_BOARD(board): 
      for c in range(NUM_COL):
            for r in range(NUM_ROW):
                  pygame.draw.rect(SCREEN, Light, (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                  pygame.draw.circle(SCREEN, Grey, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)),RADIUS)
      
      for col in range(NUM_COL):
            for row in range(NUM_ROW):
                  if board[row][col]==1:
                        pygame.draw.circle(SCREEN,
                        Aqua, (int(col*SQUARE_SIZE+SQUARE_SIZE/2), HEIGHT-int(row*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
                  if board[row][col]==2:
                        pygame.draw.circle(SCREEN, Crimson, (int(col*SQUARE_SIZE+SQUARE_SIZE/2), HEIGHT-int(row*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
      pygame.display.update()

#Returns a list of Empty columns
def CHECK_EMPTY(board): 
      FREE_SPACE  = []

      for col in range(NUM_COL):
            if EMPTY_COLUMN(board, col):
                  FREE_SPACE.append(col)

      return FREE_SPACE

board = BOARD_MATRIX()
FLIP_MATRIX(board)
GAME_OVER= False
YOUR_MOVE=0

#initiliazing pygame 
pygame.init()

SQUARE_SIZE=100 

WIDTH = NUM_COL*SQUARE_SIZE
HEIGHT = (NUM_ROW+1) * SQUARE_SIZE

SIZE = (WIDTH,HEIGHT)

RADIUS = int(SQUARE_SIZE/2 - 5)

SCREEN = pygame.display.set_mode(SIZE)
DESIGN_BOARD(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 70)


while not GAME_OVER:

      for event in pygame.event.get():
            if event.type == pygame.QUIT:
                  sys.exit()

            if event.type == pygame.MOUSEMOTION:
                  pygame.draw.rect(SCREEN, Grey,(0,0,WIDTH,SQUARE_SIZE))
                  XPOS= event.pos[0]

                  if YOUR_MOVE==0:
                        pygame.draw.circle(SCREEN,
                        Aqua,(XPOS,int(SQUARE_SIZE/2)),RADIUS)

                  else:
                        pygame.draw.circle(SCREEN, Crimson,(XPOS,int(SQUARE_SIZE/2)),RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                  pygame.draw.rect(SCREEN, Grey,(0,0,WIDTH,SQUARE_SIZE))
                  
                  if YOUR_MOVE==0:
                        XPOS = event.pos[0]
                        COL = int(math.floor(XPOS/SQUARE_SIZE))

                        if EMPTY_COLUMN(board, COL):
                              ROW = EMPTY_ROW(board, COL)
                              RELEASE_PIECE(board,ROW,COL,1)

                              if win(board,1):
                                    label = myfont.render("Player One Wins!", 1,
                                    Aqua)
                                    SCREEN.blit(label,(20,10))
                                    GAME_OVER=True
                       
                  
                  else:
                        XPOS = event.pos[0]
                        COL = int(math.floor(XPOS/SQUARE_SIZE))

                        if EMPTY_COLUMN(board, COL):
                              ROW = EMPTY_ROW(board, COL)
                              RELEASE_PIECE(board,ROW,COL,2)

                              if win(board,2):
                                    label= myfont.render("Player Two Wins!", 2, Crimson)
                                    SCREEN.blit(label,(20,10))
                                    GAME_OVER=True
                        

                  FLIP_MATRIX(board)
                  DESIGN_BOARD(board)

                  YOUR_MOVE=YOUR_MOVE+1
                  YOUR_MOVE=YOUR_MOVE%2

                  if GAME_OVER:
                        pygame.time.wait(3000)
