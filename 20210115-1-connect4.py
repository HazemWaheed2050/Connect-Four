# FCAI – Programming 1 – 2022 - Assignment 1
# Program Name: 20210115_connectfour
# Program Description: Connect4 with GUI
# Author1 and ID and Group: Hazem Waheed - 20210115 - Group A
# Last Modification Date: 14/3/2022
# Teaching Assistant: Professor Mohammad El-Ramly
# Version 1.0

import numpy as np
import pygame
import math
import sys

board = [['_' for i in range(7)] for j in range(6)]
rows = 6
columns = 7

WHITE = (255,255,255)
BLACK = (0, 0, 0)
BLUE = (20,75,159)
RED = (141,27,31)

# WILL FLIP THE BOARD TO MAKE THE BIASING START FROM THE BOTTOM LEFT NOT UPPER LEFT
def display_board(board):
    board = np.flip(board,0)
    for row in board:
        print("|" , *row , "|", sep = "  " )
    print()
    print(" " , *[1, 2, 3, 4, 5, 6, 7] , sep = "  ")

def which_row(board , col):     # to see which empty row the coin will drop
    for r in range(rows):
        if board[r][col - 1] == '_':
            return r

def empty_column(board,col):    # checks if the column is full or no
    if board[rows - 1][col - 1] == '_':
        return True
    return False

def update_board(board,row,col,choice): # choice is either 'x' or 'o' 
    board[row][col - 1] = choice

# GUI BOARD WINDOW
def graphics_board(board):
    for col in range(columns):
        for row in range(rows):
            pygame.draw.rect(visual, BLACK, (col*sq_size , row*sq_size + sq_size, sq_size, sq_size), 0) # Will draw rectangles
            pygame.draw.circle(visual, WHITE, (col * sq_size + sq_size // 2 , row*sq_size + sq_size + sq_size // 2), radius) # then making a hollow white circle in them which is the slots 
    for col in range(columns):
        for row in range(rows):
            if board[row][col] == "x":
                pygame.draw.circle(visual, RED, (col * sq_size + sq_size // 2 , game_height - (row*sq_size + sq_size // 2)), radius) # coin of player 1 == red     
            elif board[row][col] == "o":
                pygame.draw.circle(visual, BLUE, (col * sq_size + sq_size // 2 , game_height - (row*sq_size + sq_size // 2)), radius) # coin of player 2 == blue
    pygame.display.update()

def win_situation(board,choice):
    
    # Horizontally checking
    for c in range(columns-3):
        for r in range(rows):
            if board[r][c] == choice and board[r][c+1] == choice and board[r][c+2] == choice and board[r][c+3] == choice:
                return True
    
    # Vertically checking
    for c in range(columns):
        for r in range(rows-3):
            if board[r][c] == choice and board[r+1][c] == choice and board[r+2][c] == choice and board[r+3][c] == choice:
                return True    

    # right diagonal /
    for c in range(columns-3):
        for r in range(rows-3):
            if board[r][c] == choice and board[r+1][c+1] == choice and board[r+2][c+2] == choice and board[r+3][c+3] == choice:
                return True 

    # left diagonal \
    for c in range(columns-3):
        for r in range(3, rows):
            if board[r][c] == choice and board[r-1][c+1] == choice and board[r-2][c+2] == choice and board[r-3][c+3] == choice:
                return True


pygame.init()

sq_size = 100
game_width = columns * sq_size
game_height = (rows + 1) * sq_size
size = (game_width,game_height)
radius = int(sq_size/2 - 3)
visual = pygame.display.set_mode(size)

graphics_board(board)
pygame.display.update()

# FONT FOR THE WINNING MESSAGE
font_name = pygame.font.SysFont("Segoe UI", 75)
done = False

turn = 0
while not done:
    for motion in pygame.event.get():
        # CHECKS IF THE GAME STATE IS QUITTING (GAME ENDED)
        if motion.type == pygame.QUIT:
            sys.exit()
        
        # TRACK THE MOUSE MOTION AND MAKE THE PLAYER'S COIN FOLLOW IT
        if motion.type == pygame.MOUSEMOTION: 
            pygame.draw.rect(visual, WHITE, (0,0, game_width, sq_size))
            x_pos = motion.pos[0]
            if turn == 0:
                pygame.draw.circle(visual, RED, (x_pos, int(sq_size / 2)), radius)
            elif turn == 1:
                pygame.draw.circle(visual, BLUE, (x_pos, int(sq_size / 2)), radius)

        pygame.display.update()

        # WHEN PRESSED THE COIN WILL FALL IN IT'S RIGHT SLOT
        if motion.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(visual, WHITE, (0,0, game_width, sq_size))
            
            if turn == 0:
                x_pos = motion.pos[0]
                p1 = (x_pos // 100) + 1


                if empty_column(board, p1):
                    row = which_row(board, p1)
                    update_board(board, row, p1, "x")
                    
                    if win_situation(board,"x"):
                        win_message = font_name.render("Player 1 won !", 1, RED)
                        visual.blit(win_message, (125, -1))
                        done = True
            else:
                x_pos = motion.pos[0]
                p2 = (x_pos // 100) + 1
                print(motion.pos)

                if empty_column(board, p2):
                    row = which_row(board, p2)
                    update_board(board, row, p2, "o")
                    
                    if win_situation(board,"o"):
                        win_message = font_name.render("Player 2 won !", 1, BLUE)

                        visual.blit(win_message, (125, -1))
                        done = True
                
            display_board(board)
            graphics_board(board)
            
            # ALTERNATING PLAYERS TURNS
            turn += 1
            turn = turn % 2

            if done:
                pygame.time.wait(2500)